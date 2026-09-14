# N.E.E.B.L.E.S. OS

Repositorio de configuración, bootstrap, build y recursos remotos propios de N.E.E.B.L.E.S. OS.

Este repositorio contiene tanto piezas integradas en la build del sistema como recursos que deben poder actualizarse de forma remota sin recompilar la ISO completa.

## Bootstrap

La ISO de N.E.E.B.L.E.S. contiene únicamente un loader mínimo y estable.

Flujo:

```text
Start N.E.E.B.L.E.S.
        ↓
loader incluido en la ISO
        ↓
bootstrap/manifest.json
        ↓
bootstrap/neebles-bootstrap
        ↓
N.E.E.B.L.E.S. Boss
```

El loader incluido en la ISO no conoce la estructura interna de Boss ni sus assets.

`bootstrap/manifest.json` describe la versión actual del inyector remoto y su SHA-256.

`bootstrap/neebles-bootstrap` contiene la lógica mutable encargada de resolver, descargar, verificar e iniciar N.E.E.B.L.E.S. Boss.

## Calamares

N.E.E.B.L.E.S. OS usa Calamares como framework de instalación y mantiene sus modificaciones de código fuente de forma separada en:

https://github.com/krockzs/neebles-calamares

Este repositorio contiene la integración de esas modificaciones dentro de la build del OS y los recursos remotos utilizados por el instalador.

## Slideshow remoto de Calamares

N.E.E.B.L.E.S. incorpora un sistema propio para alimentar progresivamente el slideshow de Calamares con imágenes y vídeos almacenados en este repositorio.

Los recursos remotos viven en:

```text
calamares/slides/
```

El runtime incluido en la ISO se encuentra en:

```text
config/includes.chroot/usr/lib/neebles/neebles-calamares-slides
```

### Fuente remota

El runtime consulta directamente:

```text
https://raw.githubusercontent.com/krockzs/neebles-os/main/calamares/slides
```

Esto permite actualizar el contenido visual del instalador sin reconstruir la ISO.

### Slots

Los recursos usan una convención numérica de slots:

```text
1.png
2.jpg
3.mp4
4.png
...
20.png
```

El sistema soporta un máximo de **20 slots**.

Para cada slot se buscan, en orden, formatos soportados de imagen o vídeo.

Formatos admitidos:

- `png`
- `jpg`
- `jpeg`
- `mp4`

### Preparación progresiva

Los recursos no necesitan descargarse todos antes de mostrar el instalador.

N.E.E.B.L.E.S. los prepara progresivamente durante la ejecución de Calamares.

Flujo conceptual:

```text
Calamares inicia
      ↓
slideshow local disponible inmediatamente
      ↓
runtime N.E.E.B.L.E.S. consulta slots remotos
      ↓
descarga un recurso válido
      ↓
lo prepara en /run/neebles/calamares/slides
      ↓
el slideshow puede utilizar el recurso preparado
      ↓
se continúa preparando el siguiente slot disponible
```

### Protección del slot activo

El runtime mantiene conocimiento del slot que se está reproduciendo mediante:

```text
/run/neebles/calamares/active-slot
```

Un slot activo no se reemplaza mientras está siendo reproducido.

Antes y después de consultar un recurso remoto, el runtime vuelve a comprobar el slot activo para evitar una sustitución durante una carrera entre descarga y reproducción.

Si un slot no puede utilizarse, el sistema continúa buscando otro disponible dentro del límite de 20 slots.

### Reemplazo seguro

Cada recurso se descarga primero a un archivo temporal:

```text
.<slot>.<extension>.tmp
```

Sólo después de completar correctamente la descarga se reemplaza el recurso mediante una operación atómica (`os.replace`).

Esto evita que Calamares encuentre un archivo parcialmente descargado.

Cuando cambia el tipo de medio asociado a un slot, se eliminan las extensiones antiguas del mismo número para que exista una única versión activa del slot.

### Límites de descarga

El runtime impone límites explícitos:

```text
Imagen: 4 MiB máximo
Vídeo:  100 MiB máximo
```

Las descargas que exceden estos límites se descartan.

### Runtime local

El servicio del slideshow expone una interfaz HTTP exclusivamente local en:

```text
127.0.0.1:28765
```

Endpoints actuales:

```text
/state
/active/<slot>
/prepare
```

Estos endpoints permiten consultar el estado, indicar qué slot está activo y solicitar la preparación del siguiente recurso.

No se expone el servicio a interfaces externas.

### Fallback sin red

El slideshow no depende obligatoriamente de Internet.

Si no existe conectividad o no hay un recurso remoto válido, N.E.E.B.L.E.S. conserva el contenido local incluido en la ISO.

Los recursos remotos funcionan como sustituciones progresivas y actualizables; el instalador mantiene un fallback local para poder funcionar offline.

### Reintentos

Si al iniciar no se consigue preparar ningún recurso remoto, el runtime vuelve a intentarlo periódicamente.

Esto permite que el instalador comience de inmediato aunque la conectividad tarde algunos segundos en estar disponible.

## Build de N.E.E.B.L.E.S. OS

La configuración reproducible de la build se encuentra principalmente bajo:

```text
config/
assets/
```

Los artefactos generados por `live-build`, la ISO terminada, `chroot/`, `binary/` y las caches de paquetes no forman parte del historial Git normal.

Los módulos Calamares compilados requeridos por la build actual están integrados en `config/includes.chroot/`, mientras que su código fuente modificado se mantiene en `neebles-calamares`.

## Ownership

N.E.E.B.L.E.S. OS es responsable de:

- bootstrap e inyector del sistema;
- integración de Calamares dentro del OS;
- slideshow remoto de imágenes y vídeo;
- recursos y configuración propios de Calamares;
- branding y assets propios del OS;
- configuración y build reproducible del sistema operativo.

El código original de Calamares pertenece al proyecto Calamares y sus contribuidores. Las modificaciones de N.E.E.B.L.E.S. se mantienen separadas y trazables en `neebles-calamares`.

N.E.E.B.L.E.S. Boss mantiene de forma independiente su runtime, releases, manifiestos y catálogo de módulos.
