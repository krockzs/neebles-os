# N.E.E.B.L.E.S. OS

**Current integration status (2026-10-04):** canonical platform-authority source updated for the generic module runtime path; next integrated image not yet rebuilt; Fresh Live acceptance pending.

N.E.E.B.L.E.S. OS is the operating-system-side source of bootstrap resources, platform authority semantics and platform boundary providers for the N.E.E.B.L.E.S. ecosystem.

The current OS is based on Debian Trixie and KDE Plasma.

> **OS defines platform authority. BUILD materializes it. Boss authenticates and consumes it. CUSTOM supplies domestic material.**

---

# Responsibilities

N.E.E.B.L.E.S. OS owns:

- platform authority descriptors;
- AuthoritySupply source truth;
- platform boundary providers;
- desktop-session provider;
- Boss bootstrap entry material;
- OS-side installation resources.

OS does not own:

- module technology;
- module Construction semantics;
- module package membership;
- domestic runtime material;
- Boss state;
- BUILD image assembly.

---

# Bootstrap

The bootstrap entrypoint retrieves the latest published Boss bootstrap metadata and invokes the governed Boss installation path.

Current bootstrap source uses the latest Boss release bootstrap.

This means the image does not need a hardcoded Boss patch version merely to fetch the latest certified Boss release.

However, OS platform authority/providers that physically ship in the ISO still require a rebuilt image when their source changes.

---

# Platform AuthoritySupply

Canonical authority definitions live under:

```text
platform/authority/
```

Current authority set includes:

```text
platform.filesystem_boundary
platform.desktop_session_interface
system.dns_resolver_config
boss.modules.install_staging
boss.modules.update_staging
neebles.domestic_workspace
boss.modules.ipc
boss.runtime
modules.runtime
modules.installed_runtime
```

The canonical catalog is:

```text
platform/authority/authority-supply.json
```

Physical existence of these files does not itself grant permission.

Boss authenticates the supplied catalog and creates explicit grants.

---

# Writable authorities

Current writable authorities include:

```text
boss.modules.install_staging
boss.modules.update_staging
neebles.domestic_workspace
```

The domestic workspace root is:

```text
/opt/neebles-build
```

Boss consumes these only through the supplied authority contract.

---

# Runtime-manifest authorities

OS now supplies explicit read-only runtime-manifest authority descriptors.

Current identities:

```text
boss.runtime
modules.runtime
```

These point consumers at runtime manifests without making OS the semantic owner of the worlds described by those manifests.

CUSTOM remains the material/world owner.

---

# Installed module runtime authority

OS also supplies:

```text
modules.installed_runtime
```

This authority exposes the installed module territory needed for strict dynamic read-only projections.

Boss may request a validated subpath for a module runtime without hardcoding that module in the platform provider.

---

# Module IPC authority

OS supplies:

```text
boss.modules.ipc
```

with exact source/destination:

```text
/run/neebles/modules.sock
```

The authority exposes only the module socket, not the whole `/run` tree.

This permits a sandboxed module runtime to communicate with Boss while keeping the boundary narrow.

---

# Filesystem boundary provider

Canonical provider:

```text
platform/bin/neebles-boundary-provider
```

The provider translates authenticated Boss boundary requests into Bubblewrap execution.

Supported projections include:

- domestic rootfs;
- readonly data;
- writable data;
- nested mount destinations;
- proc/dev/tmp;
- explicit environment;
- working directory;
- command.

The boundary provider clears the inherited environment and reconstructs only explicitly supplied environment values.

---

## Nested mount destinations

The provider creates required destination directories generically before applying bind mounts.

It does not contain module-specific mountpoint paths.

---

## Overlay rule

When an authorized external file must be inserted below an existing domestic top-level, the provider uses Bubblewrap overlay composition rather than copying the entire domestic directory.

This avoids traversing unrelated root-only domestic material.

Authority is established by mount composition, not domestic-tree duplication.

---

# Desktop-session provider

Canonical provider:

```text
platform/bin/neebles-desktop-session-provider
```

It validates the desktop-session resources required for graphical module execution.

Current certified fields include:

```text
XDG_RUNTIME_DIR
DBUS_SESSION_BUS_ADDRESS
DISPLAY
WAYLAND_DISPLAY
XAUTHORITY
```

The provider also validates physical resources such as:

- Wayland socket ownership;
- Xauthority location/ownership;
- local X11 display socket;
- session bus.

Boss receives a certified desktop-session interface instead of inheriting arbitrary host environment as authority.

---

# Identity boundary

The OS provider exposes session facts.

Boss resolves the authenticated desktop identity and performs the governed identity drop before launching a session-aware workspace command.

OS does not decide module policy.

---

# BUILD relationship

N.E.E.B.L.E.S. BUILD must materialize the complete current platform authority set into the image.

BUILD's sync tooling must not maintain an outdated hardcoded subset.

Current required law:

```text
OS platform/authority
    -> BUILD image-side authority tree

OS platform/bin
    -> BUILD image-side providers
```

Byte parity must be preserved while BUILD normalizes required ownership/modes.

---

# Current image boundary

The previous image predates the new runtime/module authorities.

Therefore a new ISO is required before final system acceptance.

A Boss release update alone is insufficient because these OS-owned files/providers must physically exist in the Live image.

---

# Fresh Live acceptance

The next image must prove:

```text
AuthoritySupply contains the complete current set
    -> boundary provider starts
    -> desktop-session provider resolves the real Plasma session
    -> Boss bootstrap succeeds
    -> Registry discovery succeeds
    -> Test Module install succeeds
    -> runtime authority descriptors resolve
    -> boss.modules.ipc resolves exact socket
    -> module runtime starts under desktop identity
```

Only real Live/installed-system testing closes this boundary.

---

# Ownership law

```text
OS
    -> platform authority semantics and providers

BUILD
    -> image-side materialization

CUSTOM / Esbirro
    -> certified domestic material/worlds/construction

Boss
    -> authentication, grants, governance and execution

Module
    -> declarative consumer + implementation
```

---

# Final principle

N.E.E.B.L.E.S. OS must remain technology-agnostic.

Adding a Python, Rust, Go, Node.js or future module must not require OS to understand that technology.

OS supplies narrow platform capabilities.

Boss consumes them generically.
