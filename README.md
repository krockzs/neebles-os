# N.E.E.B.L.E.S. OS

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

## Point 7 integration

Point 7 introduced the OS-side authority required by generic domestic construction without teaching the OS module technology.

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

## Ownership rule

OS describes platform authority.

BUILD materializes it.

Boss consumes it.

CUSTOM supplies certified domestic runtime and construction material.

Lifecycle does not own domestic construction or Esbirro certification.
