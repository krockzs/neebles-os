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

Current authority families include:

```text
platform.filesystem_boundary
platform.desktop_session_interface
system.dns_resolver_config
boss.modules.install_staging
boss.modules.update_staging
```

The platform boundary provider lives below:

```text
platform/bin/
```

These definitions are materialized into N.E.E.B.L.E.S. BUILD for image construction.

## Ownership rule

OS describes platform authority.

BUILD materializes it.

Boss consumes it.

CUSTOM supplies certified domestic runtime material.
