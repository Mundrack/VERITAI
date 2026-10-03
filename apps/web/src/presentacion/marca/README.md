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
en `src/extension/iconos/`.

Estado (2026-10-03): la carpeta está preparada y los dos SVG **todavía no
están en el repositorio**.
