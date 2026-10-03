# Marca

Aquí van los SVG del símbolo de VERITAI. Es la única carpeta de recursos
gráficos de la interfaz; la regla completa está en
`docs/ARQUITECTURA-VISUAL.md` §2.1.

| Fichero | Qué es | Cuándo se usa |
|---|---|---|
| `veritai-simbolo.svg` | el símbolo con órbita, con su color propio | a partir de 48 px |
| `veritai-simbolo-min.svg` | solo la estrella, `fill="currentColor"`, sin color propio | por debajo de 48 px; hereda el color del texto |

Los dos tienen que tener `viewBox` cuadrado. Los PNG de icono de la extensión
**no se dibujan a mano**: `npm run iconos` los genera desde estos dos ficheros
en `src/extension/iconos/`. Los de 16 y 32 px llevan el color
`--veritai-color-icono-extension` (contraste en las dos barras del navegador,
no el acento de la interfaz: §2.1 del documento).

El arte conceptual de la marca (tableros, recortes de identidad, el mockup y
los iconos exportados a mano) **no está en este repositorio**: vive en la
carpeta hermana `WORK SPACE/VERITAI-marca/`, con su propio repositorio
privado (`Mundrack/VERITAI-marca`). De ahí no se toma ningún recurso para el
producto.

Los dos ficheros llevan un manifiesto C2PA (`<metadata>`) cuyo hash cubre el
fichero: **no se editan**, ni para añadir un `id`. Versionados el 2026-10-03:
`veritai-simbolo.svg` sha256 `ab8c5df2…`, `veritai-simbolo-min.svg` sha256
`10f12528…`.
