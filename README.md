# N.E.E.B.L.E.S. OS

**Current integration status (2026-10-04): Point 8 GREEN / CLOSED; Boss contract CLOSED; post-Live platform-boundary repair committed; next integrated OS image not yet rebuilt.**

N.E.E.B.L.E.S. OS contains the operating-system-side configuration, bootstrap resources and canonical platform authority definitions of the N.E.E.B.L.E.S. ecosystem.

The OS is based on Debian and KDE Plasma.

## Bootstrap

The current bootstrap transports domestic runtime information and platform AuthoritySupply into the Boss installation flow.

## Platform authority

N.E.E.B.L.E.S. OS is the semantic owner of platform authority.

Canonical authority definitions live below:

```text
platform/authority/
```

Current authority identities include:

```text
platform.filesystem_boundary
platform.desktop_session_interface
system.dns_resolver_config
boss.modules.install_staging
boss.modules.update_staging
neebles.domestic_workspace
```

`neebles.domestic_workspace` belongs to the generic writable-data authority family:

```text
neebles-writable-data-authority
```

Its canonical writable root is:

```text
/opt/neebles-build
```

The authority is supplied through the canonical AuthoritySupply catalog and is consumed by Boss only after normal platform-controlled authentication, registration and explicit grant construction.

The platform boundary provider lives below:

```text
platform/bin/
```

These definitions are materialized into N.E.E.B.L.E.S. BUILD for image construction.

## Point 7 / Point 8 continuity

Point 7 introduced the OS-side authority required by generic domestic construction without teaching the OS module technology.

Point 8 globally recertified the Boss contract without requiring source changes in N.E.E.B.L.E.S. OS. The platform-authority model established before Point 8 remains the canonical OS contract.

The ownership law is:

```text
OS
  -> defines platform authority semantics

BUILD
  -> materializes the authority into the image

Boss
  -> authenticates, registers, grants and consumes it

CUSTOM
  -> owns certified domestic material and construction declarations
```

The OS does not discover host capabilities for Boss and does not derive permission from filesystem presence.

Stage 8 host independence remains permanent.

Point 8 did not add a new OS authority or provider. `platform.desktop_session_interface`, `platform.filesystem_boundary`, `neebles.domestic_workspace` and the rest of the canonical AuthoritySupply remain owned by OS and consumed by Boss through explicit authenticated grants.

The final Point 8 gate is a pre-VM Boss closure. Full installed-system acceptance in a virtual machine remains a later phase and does not change OS ownership by itself.

## Ownership rule

OS describes platform authority.

BUILD materializes it.

Boss consumes it.

CUSTOM supplies certified domestic runtime and construction material.

Lifecycle does not own domestic construction or Esbirro certification.


## Current handoff

```text
POINT 7 CUSTOM V2            GREEN / CLOSED
POINT 8 BOSS FINAL GATE      GREEN / CLOSED
BOSS CONTRACT                CLOSED
OS SOURCE CHANGE IN POINT 8  NONE REQUIRED
TEST MODULE                  NEXT: POINT 9 ADAPTATION
```

With the Boss contract closed, Test Module may be adapted when Point 9 begins. Test Module remains a consumer of the closed Boss/OS authority contract and does not define platform authority semantics.


## Post-Live platform-boundary repair — 2026-10-04

Live testing exposed a real provider defect in the OS-owned filesystem boundary implementation. The old provider path attempted to copy an entire domestic top-level such as `rootfs/etc` when an external destination had to be introduced. As an ordinary user this could traverse root-only domestic files and fail before the requested boundary was established.

The canonical OS provider was repaired so the domestic root remains read-only and an existing top-level is used as the lower layer of a Bubblewrap temporary overlay. The external file is then bound into that overlay. No byte-copy staging, privilege escalation or traversal of unrelated root-only material is required.

Canonical source repair:

```text
neebles-os commit b3bd0896cdf5b03ee79f485ebdbe39b49362ed43
platform/bin/neebles-boundary-provider
```

This repair was manually materialized into the Live session and validated as a normal user. With explicit AuthoritySupply, `modules available` then reached the N.E.E.B.L.E.S. Registry successfully and exposed Test Module.

### Remaining entrypoint issue

The platform supply itself is valid, but the ordinary direct `neebles` CLI entrypoint still does not automatically transport `--authority-supply`. The system runtime service does receive it. This is a Boss entrypoint-transport issue, not a reason to move platform-authority ownership out of OS.

The next OS image must carry the committed provider repair. No new ISO is claimed by this README checkpoint.
