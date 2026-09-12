# N.E.E.B.L.E.S. OS

Repositorio de configuración, bootstrap y recursos remotos propios de N.E.E.B.L.E.S. OS.

Este repositorio contiene piezas que pertenecen al sistema operativo pero que deben poder actualizarse sin recompilar la ISO completa.

## Bootstrap

La ISO de N.E.E.B.L.E.S. contiene únicamente un loader mínimo y estable.

Flujo:

    Start N.E.E.B.L.E.S.
            ↓
    loader incluido en la ISO
            ↓
    bootstrap/manifest.json
            ↓
    bootstrap/neebles-bootstrap
            ↓
    N.E.E.B.L.E.S. Boss

El loader incluido en la ISO no conoce la estructura interna de Boss ni sus assets.

bootstrap/manifest.json describe la versión actual del inyector remoto y su SHA-256.

bootstrap/neebles-bootstrap contiene la lógica mutable encargada de resolver, descargar, verificar e iniciar N.E.E.B.L.E.S. Boss.

## Calamares

El directorio:

    calamares/slides/

contiene los recursos remotos utilizados por el slideshow personalizado del instalador de N.E.E.B.L.E.S. OS.

Los recursos utilizan slots numéricos:

    1.png
    2.png
    3.mp4
    ...

Se admiten:

- png
- jpg
- jpeg
- mp4

El sistema soporta un máximo de 20 slots.

Los recursos pueden actualizarse independientemente de la ISO.

## Ownership

N.E.E.B.L.E.S. OS es responsable de:

- bootstrap e inyector del sistema
- recursos y configuración propios de Calamares
- branding y assets propios del OS
- configuración remota propia del sistema operativo

N.E.E.B.L.E.S. Boss mantiene de forma independiente su runtime, releases, manifiestos y catálogo de módulos.
