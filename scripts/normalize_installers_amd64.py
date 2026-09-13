#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "config" / "installers" / "instaladores_amd64.json"

ALLOWED_KINDS = {
    "subcommand",
    "flag",
    "option",
    "operand",
    "operand_list",
    "literal",
    "separator",
}
ALLOWED_ROOT_MODES = {"required", "not_required", "contextual"}
ALLOWED_EXPECT_KEYS = {"stdout_equals"}


def is_scalar(value):
    return isinstance(value, (str, int, float, bool)) and value is not None


def likely_subcommand_candidate(item):
    if item.get("kind") != "literal":
        return False
    value = item.get("value")
    return isinstance(value, str) and value and not value.startswith("-") and value != "--"


def canonicalize_flow(flow):
    # Preserve argv exactly. This only improves semantic metadata.
    # The first fixed word before any dynamic operand is treated as a subcommand.
    saw_dynamic = False
    converted = False
    for item in flow:
        kind = item.get("kind")
        if kind in {"operand", "operand_list", "option"} and "source" in item:
            saw_dynamic = True
        if not converted and not saw_dynamic and likely_subcommand_candidate(item):
            item["kind"] = "subcommand"
            converted = True


def infer_variables(flow):
    variables = {}
    for item in flow:
        source = item.get("source")
        if not source:
            continue
        kind = item.get("kind")
        expected = "array" if kind == "operand_list" else "scalar"
        current = variables.get(source)
        if current and current["type"] != expected:
            current["type"] = "scalar_or_array"
        else:
            variables[source] = {"type": expected, "required": True}
    return dict(sorted(variables.items()))


def fixed_probe_is_read_only(flow):
    if not flow:
        return True
    for item in flow:
        if item.get("source"):
            return False
        value = item.get("value")
        if not isinstance(value, str):
            return False
        if value not in {"--version", "-V", "-v", "version", "--help", "-h", "help"}:
            return False
    return True


def apply_known_safe_semantics(distribution):
    installers = distribution.get("installers", {})

    # dpkg accepts multiple .deb/package operands; read-only probe/list do not need root.
    dpkg = installers.get("dpkg")
    if isinstance(dpkg, dict):
        operations = dpkg.get("operations", {})
        if "probe" in operations:
            operations["probe"]["root_mode"] = "not_required"
        if "list" in operations:
            operations["list"]["root_mode"] = "not_required"
        for op_name, source_name in (("install_file", "files"), ("remove", "packages"), ("purge", "packages")):
            op = operations.get(op_name)
            if not isinstance(op, dict):
                continue
            flow = op.get("flow", [])
            for item in flow:
                if item.get("kind") == "operand" and item.get("source") in {"file", "package"}:
                    item["kind"] = "operand_list"
                    item["source"] = source_name


def validate_operation(distribution_id, installer_id, operation_id, operation):
    prefix = f"{distribution_id}:{installer_id}:{operation_id}"
    if not isinstance(operation, dict):
        raise ValueError(f"{prefix}: operation must be an object")

    command = operation.get("command")
    if not isinstance(command, str) or not command:
        raise ValueError(f"{prefix}: missing command")

    root_mode = operation.get("root_mode")
    if root_mode not in ALLOWED_ROOT_MODES:
        raise ValueError(f"{prefix}: invalid root_mode {root_mode!r}")

    flow = operation.get("flow")
    if not isinstance(flow, list):
        raise ValueError(f"{prefix}: flow must be an array")

    for index, item in enumerate(flow):
        if not isinstance(item, dict):
            raise ValueError(f"{prefix}: flow[{index}] must be an object")
        kind = item.get("kind")
        if kind not in ALLOWED_KINDS:
            raise ValueError(f"{prefix}: unsupported flow kind {kind!r}")

        if kind in {"subcommand", "flag", "literal", "separator"}:
            if "value" not in item or not is_scalar(item["value"]):
                raise ValueError(f"{prefix}: {kind} requires scalar value")
        elif kind == "operand_list":
            if not isinstance(item.get("source"), str) or not item["source"]:
                raise ValueError(f"{prefix}: operand_list requires source")
        elif kind in {"operand", "option"}:
            has_value = "value" in item
            has_source = isinstance(item.get("source"), str) and bool(item.get("source"))
            if has_value == has_source:
                raise ValueError(f"{prefix}: {kind} requires exactly one of value/source")
            if has_value and not is_scalar(item["value"]):
                raise ValueError(f"{prefix}: {kind}.value must be scalar")
            if kind == "option" and (not isinstance(item.get("name"), str) or not item["name"]):
                raise ValueError(f"{prefix}: option requires name")

    expect = operation.get("expect")
    if expect is not None:
        if not isinstance(expect, dict):
            raise ValueError(f"{prefix}: expect must be an object")
        unsupported = set(expect) - ALLOWED_EXPECT_KEYS
        if unsupported:
            raise ValueError(f"{prefix}: unsupported expect keys {sorted(unsupported)}")


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))

    if data.get("architecture") != "amd64":
        raise SystemExit("Dictionary architecture must be amd64")

    data["schema"] = 4
    data["version"] = max(int(data.get("version", 0)), 4)

    rules = data.setdefault("design_rules", [])
    for rule in [
        "Cada operación declara explícitamente sus variables requeridas y su tipo inferido desde flow.",
        "La normalización semántica nunca cambia el argv efectivo: sólo clasifica mejor cada pieza del flow.",
        "Todo probe puramente de versión/ayuda es no privilegiado.",
        "El diccionario completo debe pasar validación estructural antes de publicarse.",
    ]:
        if rule not in rules:
            rules.append(rule)

    data["variable_contract"] = {
        "description": "Las variables se declaran por operación. scalar acepta string/number/bool; array expande una posición argv por elemento.",
        "scalar_types": ["string", "number", "boolean"],
        "array_item_types": ["string", "number", "boolean"],
        "missing_required_variable": "error",
        "silent_fallbacks": False,
    }

    distributions = data.get("distributions")
    if not isinstance(distributions, dict) or not distributions:
        raise SystemExit("Dictionary must contain distributions")

    stats = Counter()
    root_modes = Counter()
    kinds = Counter()
    variable_sources = Counter()

    for distribution_id, distribution in distributions.items():
        if not isinstance(distribution, dict):
            raise ValueError(f"{distribution_id}: distribution must be an object")
        stats["distributions"] += 1
        apply_known_safe_semantics(distribution)

        installers = distribution.get("installers")
        if not isinstance(installers, dict):
            raise ValueError(f"{distribution_id}: installers must be an object")

        for installer_id, installer in installers.items():
            if not isinstance(installer, dict):
                raise ValueError(f"{distribution_id}:{installer_id}: installer must be an object")
            stats["installers"] += 1

            operations = installer.get("operations")
            if not isinstance(operations, dict) or not operations:
                raise ValueError(f"{distribution_id}:{installer_id}: operations must be a non-empty object")

            operation_commands = {
                op.get("command")
                for op in operations.values()
                if isinstance(op, dict) and isinstance(op.get("command"), str)
            }
            if not installer.get("command") and len(operation_commands) == 1:
                installer["command"] = next(iter(operation_commands))

            for operation_id, operation in operations.items():
                stats["operations"] += 1
                flow = operation.get("flow", []) if isinstance(operation, dict) else []
                canonicalize_flow(flow)

                if operation_id == "probe" and fixed_probe_is_read_only(flow):
                    operation["root_mode"] = "not_required"

                if isinstance(operation, dict):
                    variables = infer_variables(flow)
                    if variables:
                        operation["variables"] = variables
                    else:
                        operation.pop("variables", None)

                validate_operation(distribution_id, installer_id, operation_id, operation)

                root_modes[operation["root_mode"]] += 1
                for item in operation["flow"]:
                    stats["flow_items"] += 1
                    kinds[item["kind"]] += 1
                    if item.get("source"):
                        variable_sources[item["source"]] += 1

    data["dictionary_stats"] = {
        "distributions": stats["distributions"],
        "installers": stats["installers"],
        "operations": stats["operations"],
        "flow_items": stats["flow_items"],
        "root_modes": dict(sorted(root_modes.items())),
        "flow_kinds": dict(sorted(kinds.items())),
        "variable_sources": dict(sorted(variable_sources.items())),
    }

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data["dictionary_stats"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
