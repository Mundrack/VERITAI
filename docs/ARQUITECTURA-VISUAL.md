# Arquitectura visual de VERITAI

**Qué gobierna.** Todo el código de interfaz del proyecto: el panel web de
`apps/web/`, la extensión MV3 que se empaquetará desde ese mismo código, y
cualquier cosa que VERITAI pinte dentro de una página de terceros. No gobierna
la API ni la lógica de verificación, que tienen su documento en
[`ARQUITECTURA.md`](ARQUITECTURA.md).

**Estado.** Propuesto el 2026-10-03 a petición de Mateo, antes de escribir el
primer componente. Describe el proyecto real a esa fecha (§0 y §9) y fija las
reglas para lo que venga después (§1–§8). Las reglas se escriben como
dependencias permitidas y como pruebas que fallan, no como intenciones. Una
regla de aquí no se relaja por rapidez; se cambia por decisión (DEC) y se
anota.

**Las dos reglas que resumen el documento.**

> La lógica de verificación no conoce la interfaz, y la interfaz no calcula
> veredictos. La interfaz recibe un veredicto ya decidido, con cada número
> acompañado de su `raw_value_span`, y lo muestra.

> VERITAI lee páginas de terceros que cambian su HTML sin avisar. Cuando no
> encuentra lo que busca, no muestra nada y lo registra. Nunca adivina.

---

## 0. Lo que había (foto del 2026-10-03, antes de la reestructuración)

Esto es lo que existía en `apps/web/` cuando se escribió el documento. El
mismo día se movió `main.ts` a las capas de §1 y §2 sin cambiar lo que se ve;
lo que queda por hacer está en §9. La foto se conserva porque explica de dónde
vienen las reglas.

| Qué | Cómo está | Dónde |
|---|---|---|
| Framework | **Ninguno.** TypeScript estricto compilado con Vite 6. Decisión del paquete de documentación: "JS vanilla, MV3" (`04-...-R02` §5) | `apps/web/package.json`, `tsconfig.json` |
| Entrada | Un único módulo que pide `GET /health` a la API y pinta una tabla de estado. No muestra veredictos | `apps/web/src/main.ts` (115 líneas) |
| Estilos | Un único fichero. Variables CSS en `:root` con tema claro y oscuro por `prefers-color-scheme`; clases sin prefijo (`.panel`, `.ok`, `.mal`, `.aviso`); selectores de elemento globales (`body`, `h1`, `table`, `button`) | `apps/web/src/estilos.css` (110 líneas) |
| i18n | Catálogos `es.json` y `en.json` con 16 claves; función `t(clave, parametros)` que sustituye `{nombre}`; al cambiar de idioma se vuelve a pintar desde las plantillas. Es la regla de `CLAUDE.md` §10 hecha código | `apps/web/src/i18n/` |
| Escapado | `escapar()` con `textContent` antes de meter cualquier dato en `innerHTML` | `main.ts` |
| Red | `fetch` con `AbortController` y 4 segundos de tope; la URL de la API viene de `VITE_API_BASE_URL` | `main.ts` |
| Servido | Contenedor `veritai-web` (Vite dev, puerto publicado solo en `127.0.0.1:5173`); `src/` montado en solo lectura | `docker-compose.yml`, `docker-compose.override.yml` |
| Tests | **Ninguno.** No hay runner, ni `npm test`, ni lint ni formateador para TypeScript (la API tiene `ruff`, `ruff format` y una suite de pytest en `apps/api/tests/`) | — |
| Extensión | **No existe.** El Dockerfile y `ESTADO.md` declaran que el panel es el mismo código que se empaquetará como MV3 "más tarde" | — |
| Inyección en páginas de terceros | **No existe** ningún código que lea el DOM de X ni de ningún sitio. La tesis (`02-1`) la define: extensión Chromium que "lee el DOM y muestra el panel de contexto"; alcance de la Fase 0: **X**, texto, español (`03-2`, `00b`) | — |

Lo que la interfaz va a consumir ya existe y está cerrado del lado de la API:
`POST /analisis` devuelve `{veredicto, evidencia, persistido, duracion_ms}`;
el `veredicto` lleva `truth`, `context`, `clase_primaria`, `abstain_reasons`,
`tests`, `comparaciones`, `numeros_usados` (cada uno con `valor`,
`raw_value_span`, `item_id`, `etiqueta`), `explicacion` (texto en español
generado por plantilla en el dominio), `evidencia_al_publicar` y
`evidencia_vigente` (DEC-034), y `bundle_hash`
(`apps/api/veritai/domain/veredicto.py`). Los enums son cerrados y están en
`domain/enums.py` y en [`GLOSARIO.md`](GLOSARIO.md).

Dos cosas que hoy **no** hay entre la página y la API, y que este documento
asume como ausentes: el intérprete del texto de entrada (el claim estructurado
se prepara a mano, DEC-028) y N0/N1. La extensión, cuando exista, localizará
texto en la página; qué pasa con ese texto hasta llegar a `POST /analisis` es
otro documento y otra decisión.

---

## 1. Capas y dependencias permitidas

### 1.1 Las capas

Siete capas dentro de `apps/web/src/`, más la extensión que las monta. Cada
una tiene un trabajo y una lista cerrada de a quién puede importar.

| Capa | Carpeta | Qué hace | Qué no hace |
|---|---|---|---|
| **Contrato** | `contrato/` | Tipos TypeScript del veredicto, del claim y de las respuestas de la API, con sus enums cerrados; validadores que comprueban en tiempo de ejecución que un JSON recibido tiene esa forma. Y el único enum cerrado propio de la interfaz: las fases de la consulta (`fase-consulta.ts`, §1.3) | No toca el DOM, ni la red, ni traduce |
| **Cliente** | `cliente/` | Habla con la API: `fetch` con tiempo máximo, URL base de configuración, errores tipados. Devuelve objetos del contrato ya validados | No pinta nada; no decide nada sobre lo que recibe |
| **Formato** | `formato/` | Presenta valores sin cambiarlos: separadores de miles y decimales por idioma (`Intl.NumberFormat`), fechas por idioma. Funciones puras | **No calcula**: ni porcentajes, ni diferencias, ni redondeos distintos de los del `raw_value_span` |
| **i18n** | `i18n/` | Catálogos `es`/`en` y `t()`. Funciones puras sobre los catálogos | No toca el DOM (hoy sí lo toca: §9) |
| **Presentación** | `presentacion/` | Componentes: funciones que reciben datos del contrato y devuelven un `HTMLElement`; el mapa de enums a estados visuales; los tokens y hojas CSS | No hace `fetch`; no localiza nada en la página de terceros; no calcula |
| **Localización** | `localizacion/` | Encuentra elementos en la página de terceros aplicando, en orden, las estrategias que declara la configuración del sitio; registra los fallos | No contiene ningún selector; no sabe qué es un veredicto; no pinta |
| **Sitios** | `sitios/` | **Solo datos**: un JSON por sitio con sus dominios, sus elementos y las estrategias para encontrarlos, más el esquema que valida a todos | Cero código. Un JSON no puede tener funciones, y eso es a propósito |
| **Aplicación** | `aplicacion/` | Orquesta: pide a `localizacion` el texto, a `cliente` el veredicto, a `presentacion` el componente, y lo monta. Es la única capa que conoce a todas | No tiene reglas de negocio ni estilos ni selectores |
| **Extensión** | `extension/` | `manifest.json` (MV3), *content script*, *service worker*, *popup*. Solo adapta la plataforma y llama a `aplicacion` | Nada más: toda la lógica vive debajo |
| **Entrada web** | `main.ts` | Arranque del panel suelto (`index.html`) para desarrollo. Llama a `aplicacion` | Hoy lo hace todo (§9) |

### 1.2 Matriz de dependencias permitidas

Una fila puede importar de las columnas marcadas con **sí**. Todo lo demás
está prohibido. La matriz vive en `apps/web/arquitectura.json` y la comprueba
una prueba (§1.4).

| importa → | contrato | cliente | formato | i18n | presentacion | localizacion | sitios | aplicacion | extension |
|---|---|---|---|---|---|---|---|---|---|
| **contrato** | — | no | no | no | no | no | no | no | no |
| **cliente** | **sí** | — | no | no | no | no | no | no | no |
| **formato** | no | no | — | **sí** | no | no | no | no | no |
| **i18n** | no | no | no | — | no | no | no | no | no |
| **presentacion** | **sí** | no | **sí** | **sí** | — | no | no | no | no |
| **localizacion** | no | no | no | no | no | — | **sí** | no | no |
| **sitios** | no | no | no | no | no | no | — | no | no |
| **aplicacion** | **sí** | **sí** | no | **sí** | **sí** | **sí** | no | — | no |
| **extension** | no | no | no | no | no | no | **sí** (*) | **sí** | — |
| **main.ts** | no | no | no | no | no | no | no | **sí** | no |

(*) La extensión lee `sitios/*.json` solo para generar `host_permissions` del
manifiesto en tiempo de construcción; en tiempo de ejecución va por
`aplicacion`.

Tres lecturas de la matriz que conviene tener a mano:

- **`contrato`, `i18n` y `sitios` no importan nada.** Son hojas. Si una de
  ellas necesita importar algo, la capa está mal cortada.
- **`presentacion` no conoce ni a `cliente` ni a `localizacion`.** Un
  componente recibe un `Veredicto` ya validado y devuelve un elemento; no sabe
  de dónde vino ni dónde se va a montar. Eso es lo que permite probarlo con un
  JSON y un DOM de pruebas, sin API ni página.
- **`localizacion` no conoce a `presentacion`.** Encontrar el texto de una
  publicación y pintar un veredicto son dos trabajos que se juntan solo en
  `aplicacion`.

### 1.3 La regla dura, en términos comprobables

"La lógica de verificación no conoce la interfaz" se cumple por construcción:
la verificación vive en `apps/api/veritai/domain/` (Python) y `apps/web/` no
tiene ningún import de ese árbol ni la API ningún import de `apps/web/`. La
API ya expone la frontera: `POST /analisis` recibe un claim estructurado y
devuelve un veredicto con cada número trazado (`ARQUITECTURA.md` §4).

"La interfaz no calcula veredictos" se descompone en cuatro prohibiciones
que una prueba puede comprobar:

1. **Ningún operador aritmético sobre valores del veredicto o de la
   evidencia** en `presentacion/`, `formato/` ni `aplicacion/`. Se permite
   aritmética de maquetación (posiciones, tamaños) solo en `aplicacion/` y
   `extension/`, y queda marcada en el código con el comentario
   `// aritmetica de maquetacion`.
2. **Los estados visuales son los enums de la API y nada más.** `truth`,
   `context`, `clase_primaria` y `abstain_reasons` se mapean a estilos en
   `presentacion/estados.ts`; un valor que no esté en el enum produce el
   estado `desconocido` y una entrada en el registro. La interfaz nunca
   deduce un estado a partir de números. Tampoco resume los dos ejes en un
   estado único: `truth` y `context` se pintan por separado (§2.2), porque
   resumirlos sería decidir un veredicto. La única excepción a "los enums de
   la API" es `FaseConsulta` (`en_espera`, `analizando`, `error`): el enum
   cerrado propio de la interfaz para cuando todavía no hay veredicto, o no
   llegó a haberlo. Aprobado por Mateo el 2026-10-03; añadirle un valor es
   decisión suya.
3. **Todo número que se pinta sale de `numeros_usados` o del claim** que el
   usuario envió, con el valor literal del `raw_value_span` y, como mucho,
   los separadores del idioma. Es la versión visual del test de trazabilidad
   de la API (`tests/test_trazabilidad.py`): si un dígito aparece en pantalla
   y no está en la evidencia, la prueba falla.
4. **`explicacion` no se traduce ni se edita.** Es texto en español generado
   por plantilla en el dominio. En `es` se puede mostrar tal cual; en `en` la
   interfaz vuelve a componer la explicación con sus propias plantillas
   i18n a partir de los campos estructurados (`truth`, `context`,
   `abstain_reasons`, `numeros_usados`, `evidencia_al_publicar`,
   `evidencia_vigente`). Es lo que `00b` llama "plantillas de explicación
   parametrizadas por idioma" y lo que `CLAUDE.md` §10 prohíbe hacer al
   revés.

### 1.4 Cómo se comprueba

`apps/web/tests/arquitectura/dependencias.test.ts` lee `arquitectura.json`,
recorre todos los `import` de `src/` y falla con el fichero y la línea de
cada import que cruce una casilla **no**. No usa ninguna dependencia: una
expresión regular sobre `import ... from "..."` basta mientras el código no
use imports dinámicos construidos con cadenas, que están prohibidos (§4).
Alternativa descartada: `dependency-cruiser`, que hace lo mismo con más
opciones y una dependencia más; si la prueba casera se queda corta, se cambia
por ella y se anota.

La API tiene exactamente la misma deuda y la declara (`ARQUITECTURA.md` §3:
"sigue sin haber un test que verifique esta regla"). Cuando se escriba la
prueba del lado web, se escribe la del lado Python en el mismo PR.

---

## 2. Dónde vive cada cosa

Estructura objetivo de `apps/web/`. Marcado con **✓** lo que existe hoy, con
**—** lo que no. Una frase por carpeta: qué entra y qué no entra.

```
apps/web/
├─ index.html                 ✓  Página del panel suelto para desarrollo. Solo el <main> raíz y el <script>; nada de contenido ni estilos en línea.
├─ package.json               ✓  Scripts y dependencias. Entra: vite, typescript, vitest, happy-dom, coverage. No entra: ningún framework de UI, ningún cliente HTTP.
├─ tsconfig.json              ✓  TypeScript estricto. No se relaja ninguna opción para que compile un fichero.
├─ vite.config.ts             ✓  Servidor de desarrollo y build. Las constantes del contenedor (host, puerto, polling) viven aquí y solo aquí.
├─ vitest.config.ts           ✓  Runner de pruebas, entorno happy-dom, umbrales de cobertura (§5.3); css: true para que las hojas importadas con ?inline lleguen a las pruebas (§5.1).
├─ arquitectura.json          ✓  La matriz de §1.2 como datos. La lee la prueba de dependencias.
├─ scripts/
│  └─ generar-iconos.mjs      ✓  `npm run iconos`: los PNG de la extensión desde los SVG de la marca (§2.1).
├─ vitrina/                   ✓  `npm run vitrina`: página local para ver los componentes en un navegador de verdad, con su autocomprobación (§5.4). Fuera de src/: no entra en el build ni en la extensión.
├─ Dockerfile                 ✓  Etapas deps / dev / build. No se sirve nada desde aquí; la extensión no corre en un contenedor.
├─ src/
│  ├─ main.ts                 ✓  Arranque del panel suelto. Entra: montar aplicacion en #app. No entra: fetch, HTML, estilos, lógica.
│  ├─ contrato/               ✓  Tipos y validadores de lo que devuelve la API (hoy: salud.ts, el contrato de GET /health; enums.ts y fase-consulta.ts). Entra: enums, Veredicto, NumeroUsado, EvidenciaEdicion, RespuestaAnalisis, RespuestaSalud. No entra: DOM, red, texto de interfaz.
│  │  ├─ enums.ts             ✓  Truth y Context, los dos ejes que pinta la bolita: los mismos valores que domain/enums.py, comprobados por una prueba (§5.2). Clase y AbstainReason llegan con el panel.
│  │  ├─ fase-consulta.ts     ✓  FaseConsulta: en_espera, analizando, error. El único enum propio de la interfaz; no existe en la API (§1.3).
│  │  ├─ veredicto.ts         —  Tipos del veredicto y de la evidencia.
│  │  └─ validar.ts           —  validarVeredicto(json): Veredicto | ErrorContrato. Rechaza lo que no tiene la forma esperada; nunca "arregla" un JSON.
│  ├─ cliente/                ✓  Acceso a la API. Entra: fetch con tiempo máximo, URL base, errores tipados (sin respuesta, tiempo agotado, HTTP n, contrato inválido). No entra: nada visual, nada de página de terceros.
│  │  ├─ api.ts               ✓  consultarSalud(); analizar(claim) todavía no.
│  │  └─ config.ts            ✓  URL base y tiempo máximo leídos de import.meta.env, con nombre y comentario.
│  ├─ formato/                ✓  Presentación de valores sin alterarlos (hoy: fechas.ts). Entra: formatearNumero(valor, span, locale), formatearFecha. No entra: aritmética.
│  ├─ i18n/                   ✓  Catálogos y t(). Entra: es.json, en.json, index.ts. No entra: DOM (fijarLocale deja de tocar document.documentElement: §9), ni textos de dominio generados por la API.
│  ├─ presentacion/           ✓  Lo que se ve (parcial: estado-servicio, bolita, estados.ts, montar.ts y las hojas de estilos/).
│  │  ├─ estados.ts           ✓  Mapa cerrado enum → estado visual (modificador de clase y de token, clave i18n). Un valor fuera del enum → "desconocido".
│  │  ├─ componentes/         ✓  (parcial) Un subdirectorio por componente, con su .ts y su .css. Entra: construir DOM a partir del contrato y de t(). No entra: fetch, selectores de la página, números literales, colores.
│  │  │  ├─ bolita/           ✓  El botón circular sobre la esquina de una publicación (§2.2): la fase de la consulta o los dos ejes del veredicto, en color y en palabras.
│  │  │  ├─ panel-veredicto/  —  El veredicto completo: dos ejes, clase, motivos, números con su origen, evidencia al publicar y vigente.
│  │  │  ├─ marca-eje/        —  Una etiqueta de estado para truth o para context.
│  │  │  ├─ numero-trazado/   —  Un número con su raw_value_span desplegable. Es la unidad que hace visible la trazabilidad.
│  │  │  ├─ motivo-abstencion/—  El motivo de abstención con su texto i18n.
│  │  │  └─ estado-servicio/  ✓  Lo que pintaba main.ts: API y base de datos vivas o no.
│  │  ├─ marca/               ✓  Los dos SVG del símbolo (§2.1): con órbita a partir de 48 px, mínimo por debajo.
│  │  ├─ estilos/
│  │  │  ├─ tokens.css        ✓  Las variables --veritai-* (color, espacio, radio, tipografía, sombra, capa) para tema claro y oscuro. Es el ÚNICO fichero con valores literales de color y tamaño. Se declaran en :root y en .veritai-raiz, la raíz de dentro del shadow root.
│  │  │  ├─ base.css          ✓  Estilos del panel suelto (index.html): body, tipografía base. NUNCA se inyecta en una página de terceros.
│  │  │  └─ raiz.css          ✓  Lo que se aplica dentro del shadow root inyectado: corta la herencia de la página en :host y en .veritai-raiz (all: initial, más direction, que all no cubre). Sin selectores de elemento.
│  │  └─ montar.ts            ✓  crearRaizAislada(): el anfitrión <veritai-raiz> con shadow root cerrado, las hojas adoptadas (tokens + raiz + la de cada componente) y el punto de montaje. No inserta nada en la página: lo coloca aplicacion.
│  ├─ localizacion/           —  El motor que aplica las estrategias de sitios/. Entra: localizar(), tipos de estrategia (enum cerrado), comprobaciones, registro de fallos. No entra: ningún selector literal, nada de veredictos.
│  │  ├─ localizador.ts       —  localizar(raiz, sitio, elemento) → { nodo, estrategia } | null.
│  │  ├─ estrategias.ts       —  Cómo se ejecuta cada tipo de estrategia y en qué orden es admisible.
│  │  └─ registro.ts          —  registrarFallo(sitio, elemento, estrategiasProbadas). Local, sin contenido de la página.
│  ├─ sitios/                 —  Solo datos.
│  │  ├─ esquema.json         —  JSON Schema que todo fichero de sitio debe cumplir.
│  │  ├─ x.json               —  X (x.com, twitter.com). El único sitio del alcance de la tesis (Fase 0).
│  │  └─ <sitio>.json         —  Cualquier otro, con la misma forma. Añadirlo no toca localizacion/.
│  ├─ aplicacion/             ✓  Orquestación. Entra: flujo localizar → analizar → montar, y el estado de la sesión. No entra: reglas de negocio, estilos, selectores.
│  │  └─ flujo.ts             ✓
│  └─ extension/              —  Adaptación a MV3. Entra: manifest (generado), content script, service worker, popup. No entra: lógica fuera de aplicacion.
│     ├─ manifest.base.json   —  Permisos mínimos; host_permissions se generan desde sitios/*.json en el build.
│     ├─ iconos/              ✓  PNG generados por scripts/generar-iconos.mjs desde src/presentacion/marca/. Nunca a mano.
│     ├─ contenido.ts         —  Content script: llama a aplicacion.
│     ├─ fondo.ts             —  Service worker: solo lo que MV3 obliga a hacer ahí.
│     └─ popup/
└─ tests/                     ✓  Espejo de src/ (parcial) más arquitectura/ y fixtures/. Sin pruebas no hay componente (§5).
   ├─ arquitectura/           ✓  dependencias, DOM inseguro y paridad de enums con la API; faltan las generales de prefijos CSS, literales y selectores (las de la bolita van en su propia prueba).
   ├─ contrato/  cliente/  formato/  i18n/  presentacion/  localizacion/  aplicacion/
   └─ fixtures/
      ├─ api/                 —  Respuestas JSON reales de POST /analisis y GET /health, con fecha.
      └─ sitios/
         └─ x/                —  Fragmentos HTML guardados de la página real, con fecha en el nombre y un INDICE.md.
```

Dos aclaraciones sobre el árbol:

- **Los componentes no son clases ni "widgets".** Son funciones puras sobre
  el DOM: `crearPanelVeredicto(veredicto, locale): HTMLElement`. Devuelven un
  elemento suelto; quien lo monta es `aplicacion`. Eso es lo que permite
  probarlos sin navegador real.
- **Los recursos gráficos tienen una sola carpeta,** `src/presentacion/marca/`
  (§2.1).
- **Dentro de una página de terceros todo va en un *shadow root*.** Es la
  única manera de que el CSS de X no deforme el panel y de que el nuestro no
  toque la página. Alternativas descartadas: prefijar clases y confiar
  (las propiedades heredadas y los `!important` del anfitrión entran igual);
  un `iframe` (no se puede anclar al elemento de la publicación, choca con la
  CSP del anfitrión y pesa más). El panel suelto de desarrollo monta los
  mismos componentes en `#app`, sin shadow root, con `base.css`.

**Cómo se monta la raíz aislada** (`presentacion/montar.ts`, desde el
2026-10-03). Cuatro decisiones; cada una cierra una vía de fuga:

1. **El anfitrión es un elemento con nombre propio**, `<veritai-raiz>`, sin
   clase, `id` ni `style`: los selectores de elemento de la página (`div`,
   `span`, `button`) no lo alcanzan. No se registra como *custom element*:
   solo se usa el nombre.
2. **El shadow root es cerrado.** El JavaScript de la página no entra por
   `anfitrion.shadowRoot`.
3. **Los estilos entran como hojas adoptadas** (`adoptedStyleSheets`), no como
   `<style>`: no se añade ningún nodo de estilo ni al documento ni al árbol, y
   todas las raíces comparten las mismas hojas.
4. **Dentro hay un único elemento raíz, `.veritai-raiz`.** Ahí se declaran los
   tokens, y no en `:host`: una regla de la página puede alcanzar al
   anfitrión (`* { ... }`) y ganarle a `:host`, pero nunca a un elemento de
   dentro. Así la página no puede cambiar un token.

**Lo que el shadow root no corta por sí solo**, y cómo se corta:

| Qué cruza la frontera | Cómo se corta | Quién lo comprueba |
|---|---|---|
| La **herencia**: color, fuente, interlineado, `text-transform`... llegan desde el padre del anfitrión | `all: initial` en `:host` y, otra vez, en `.veritai-raiz` (`estilos/raiz.css`) | `montar.test.ts` por estructura; la vitrina, midiendo (§5.4) |
| **`direction`**: `all` no la reinicia (la especificación la excluye, con `unicode-bidi`), y se hereda. Una página de derecha a izquierda nos la pasaba | `direction: ltr` a mano en los dos sitios. La dirección de lo nuestro es la de nuestro idioma de interfaz. **Lo encontró la autocomprobación de la vitrina en Chrome**; happy-dom no podía verlo | `montar.test.ts` y la vitrina |
| **`rem`** y las unidades de ventana: dentro de la página de un tercero, `rem` es el `font-size` del `<html>` de esa página | Lo que se inyecta solo usa tokens en px o sin unidad (§4) | `montar.test.ts`; la vitrina tiene el `<html>` a 22 px a propósito |
| Las **custom properties** de la página: `all` tampoco las toca | Todos los tokens que usa una hoja inyectada están declarados en `.veritai-raiz` | `montar.test.ts` (página hostil que redefine nuestros tokens) |

**Lo que no puede evitar.** El anfitrión es un elemento del DOM de la página:
la página puede moverlo, ocultarlo o recortarlo. Lo que se garantiza es lo de
dentro.


### 2.1 La marca: dónde vive el símbolo y cómo se usa

Los recursos gráficos de la interfaz son dos ficheros SVG y viven en
**`src/presentacion/marca/`**, porque son presentación: los consumen los
componentes y los gobiernan los tokens. No van en `src/marca/` (todo lo que
hay en `src/` pertenece a una capa declarada, §1.4) ni en `public/`.

| Fichero | Qué es | Regla de uso (Mateo, 2026-10-03) |
|---|---|---|
| `veritai-simbolo.svg` | el símbolo con órbita, con su color propio | **a partir de 48 px** |
| `veritai-simbolo-min.svg` | solo la estrella, `fill="currentColor"` | **por debajo de 48 px**; hereda el color del texto que lo rodea, así que **no lleva color propio** y no se le pone ninguno desde CSS |

Los dos tienen `viewBox="0 0 100 100"`, `role="img"` y `aria-label`, y los
dos llevan un manifiesto C2PA en `<metadata>` cuyo hash cubre el fichero: **no
se editan**, ni para añadir un `id`; si el símbolo cambia, se sustituye el
fichero entero. Versionados el 2026-10-03 (sha256 `ab8c5df2…` y
`10f12528…`).

**Cómo los usa un componente.** El símbolo con órbita se pinta con
`<img src=... alt=...>`: tiene color propio y el texto alternativo va en
`alt`, por `t()`; es lo que hace `estado-servicio` en la cabecera del panel,
a 48 px (`--veritai-marca-tamano-cabecera`). El mínimo necesita heredar
`currentColor`, y un `<img>` no hereda nada; como el fichero no expone
ningún `id` (y no se edita), `<use href="...#id">` no sirve. Cuando haga
falta se usará `mask-image: url(...)` con `background-color: currentColor`
sobre un `<span role="img" aria-label>`, que hereda el color y no inyecta
nada en el DOM. Ninguno de los dos se mete por `innerHTML` (§4).

**Iconos de la extensión.** Los PNG que pide Manifest V3 (16, 32, 48 y 128
px) y el de la ficha de la tienda (512) **no se dibujan a mano**:
`npm run iconos` ejecuta `scripts/generar-iconos.mjs`, que los genera desde
los dos SVG en `src/extension/iconos/` con `@resvg/resvg-js` (renderizador
SVG con binario precompilado y sin dependencias del sistema; alternativas
descartadas: `sharp`, que trae todo un pipeline de imagen que no hace falta,
e Inkscape o ImageMagick, que serían dependencias del sistema). Aplica la
regla de arriba: 16 y 32 desde el mínimo, 48, 128 y 512 desde el de órbita.
Como un PNG no tiene texto del que heredar, el mínimo se renderiza con un
color de contexto: el token `--veritai-color-icono-extension` de
`tokens.css`, o `--color=#rrggbb`; sin ninguno de los dos el script se para. Si
el símbolo cambia, se vuelve a ejecutar y los PNG cambian con él; los PNG
generados se versionan junto al script.

**Tokens de acento: medidos, aprobados por Mateo el 2026-10-03.** Los
colores se midieron primero sobre `icono-512.png`, un render del símbolo
hecho a mano, y después se contrastaron con el SVG: el anillo va de
`#8A1F25` a `#D9444C` y la estrella de `#9C2A31` a `#FFF4F4`; el rojo sólido
más frecuente del render es `#98242c`. Ninguno coincide con los dos únicos
rojos que había en `tokens.css`, que son de estado, no de marca:

| Color | Tono | Contraste sobre `#ffffff` | Contraste sobre `#14161a` |
|---|---|---|---|
| anillo del símbolo `#98242c` | 356°, carmesí | 8,00:1 | 2,26:1 |
| extremo claro del símbolo `#ea959a` | 355° | 2,27:1 | 7,99:1 |
| `--veritai-color-mal` claro `#b3261e` | 3°, más cálido | 6,54:1 | 2,77:1 |
| `--veritai-color-mal` oscuro `#ff6b61` | 4° | 2,79:1 | 6,49:1 |
| mockup "Control Center" `--red` `#e63946` | 356° | 4,17:1 | 4,35:1 |

Decisión (Mateo, 2026-10-03), aplicada en `tokens.css`:

- `--veritai-color-acento`: `#98242c` en tema claro y `#ea959a` en tema
  oscuro. Los dos salen del propio símbolo y los dos pasan AA (≥ 4,5:1) como
  texto sobre su fondo. Ningún componente lo aplica a texto todavía, así que
  no hay ningún contraste que haya bajado de AA al aplicarlo; los iconos de
  la extensión no lo usan (abajo).
- `--veritai-color-mal` se queda como está: es el color de "fallo", no el de
  la marca; un servicio caído no puede leerse igual que el logotipo.
- El rojo del mockup (`#e63946`) no pasa AA como texto sobre blanco (4,17:1)
  y no sale del símbolo: no se adopta.

**Color de los iconos de la extensión: decisión de contraste, no de marca
(Mateo, 2026-10-03).** Manifest V3 admite un solo juego de iconos, sin
variante por tema del navegador. El acento claro (`#98242c`) da 8,0:1 sobre
una barra clara pero 2,0:1 sobre la barra oscura de Chrome (`#202124`): el
símbolo desaparecería en la mitad de los navegadores. Por eso el 16 y el 32
llevan `--veritai-color-icono-extension: #d9444c`, el tono intermedio del
propio anillo del símbolo, que se ve en las dos barras (4,3:1 sobre blanco,
3,7:1 sobre `#202124`). El token vive en `tokens.css` con la razón al lado y
solo lo lee `scripts/generar-iconos.mjs`; la interfaz, que sí tiene dos
temas, sigue usando el acento. Los de 48, 128 y 512 no cambian: llevan el
símbolo con órbita y sus propios colores.

**Hallazgo que justifica el script.** De los cinco PNG hechos a mano que
llegaron a la raíz del repositorio, `icono-16.png` es negro puro (48 píxeles
opacos, todos `#000000`): es el símbolo mínimo exportado sin color de
contexto. Es el fallo que el script evita.

### 2.2 La bolita

El botón circular que VERITAI pone sobre la esquina de una publicación, en la
página de un tercero. Vive en `presentacion/componentes/bolita/`. Construida
el 2026-10-03, **sola**: no está conectada a ninguna página ni a la API, y no
hay panel.

```ts
crearBolita(estado, { alPulsar }): HTMLButtonElement
fijarEstadoBolita(bolita, estado): void   // cambia el estado sobre el MISMO nodo: el foco no se pierde

type EstadoBolita = { fase: FaseConsulta } | { truth: string; context: string }
```

```
<button class="veritai-bolita ..." aria-label="...">     la caja fija que se pulsa y se enfoca
  <span class="veritai-bolita__disco">                   lo que se ve: fondo, anillo, sombra. Es lo que crece y encoge
    <span class="veritai-bolita__pulso">                 el halo que late mientras analiza
    <span class="veritai-bolita__simbolo">               el símbolo mínimo, como máscara, con el color del estado
  <span class="veritai-bolita__etiqueta">                el estado en palabras. Fuera del disco: no se escala con él
```

**Dos ejes, dos canales (decisión de Mateo, 2026-10-03).** El veredicto no es
un enum: son dos ejes independientes, `truth` y `context` (DEC-016), y la
bolita no los resume.

| Canal | Eje | Propiedad | Token |
|---|---|---|---|
| el símbolo | `context` | `color` | `--veritai-color-context-<valor>` |
| el anillo | `truth` | `border-color` del disco | `--veritai-color-truth-<valor>` |

Por qué no un solo color. Ningún eje sirve solo: pintando solo `context`, una
afirmación `contradicted` sin divergencia se leería como "sin divergencia
detectada"; pintando solo `truth`, `supported` + `divergence_detected`, que es
el caso que la tesis existe para señalar, se leería como "respaldado". Y un
estado resumen de los dos tendría que decidirlo alguien: si lo decide la
interfaz, calcula un veredicto (§1.3); si lo decide el dominio, hace falta un
enum nuevo en la API con su DEC (los títulos de `SALIDA` en `plantilla.py` son
esa tabla, pero como texto). Alternativa descartada por ahora, no cerrada.

Mientras no hay veredicto, la bolita pinta la **fase de la consulta**
(`FaseConsulta`, §1.3): símbolo y anillo del mismo color y anillo fino. Con
veredicto, el anillo es grueso, porque lleva `truth` y tiene que verse. `error`
lleva además el anillo discontinuo: dice "no se pudo" sin depender del color.
Un valor de `truth` o de `context` que no esté en su enum se pinta como
`desconocido`; el valor que llegó no se escribe en el DOM.

**El estado, en palabras.** El color nunca es la única señal. El estado es el
nombre accesible del botón (`aria-label`) y una etiqueta visible que aparece
al pasar por encima y al enfocar con el teclado, compuestos los dos desde la
misma plantilla i18n: `"VeritAI. Contexto: divergencia detectada. Dato:
respaldado por la fuente."`. Los 33 estados posibles (3 fases, y 6 × 5
combinaciones contando `desconocido`) tienen 33 etiquetas distintas en cada
idioma. Los textos respetan `GLOSARIO.md` §Términos que NO se usan, y una
prueba lo vigila.

**Colores de estado** (valores a 2026-10-03; la fuente de verdad es
`tokens.css`). Entre paréntesis, el contraste contra el disco de la bolita.

| Estado | Tema claro (disco `#ffffff`) | Tema oscuro (disco `#14161a`) |
|---|---|---|
| `fase.en_espera` | el acento de la marca, `#98242c` (8,0) | `#ea959a` (8,0) |
| `fase.analizando` | `#e0575f` (3,7) | `#e5384a` (4,3) |
| `fase.error` | `#475569` (7,6) | `#8aa0cc` (6,9) |
| `truth.supported` | `#1d4ed8` (6,7) | `#7aa2ff` (7,3) |
| `truth.contradicted` | `#b3261e` (6,5) | `#f2695a` (6,0) |
| `truth.mixed` | `#b8860b` (3,3) | `#f7d154` (12,3) |
| `truth.insufficient_evidence` | `#4b5360` (7,8) | `#9aa3b0` (7,1) |
| `truth.not_applicable` | `#8b929c` (3,1) | `#5f6672` (3,1) |
| `context.divergence_detected` | `#c2410c` (5,2) | `#ffa14a` (9,0) |
| `context.no_divergence_detected` | `#1d4ed8` (6,7) | `#7aa2ff` (7,3) |
| `context.undetermined` | `#4b5360` (7,8) | `#9aa3b0` (7,1) |
| `context.not_applicable` | `#8b929c` (3,1) | `#5f6672` (3,1) |
| `desconocido` (los dos ejes) | el color de texto, `#14161a` (18,1) | `#eef1f5` (16,0) |

Las reglas que cumple la paleta, y que comprueba
`tests/presentacion/accesibilidad.test.ts` leyendo `tokens.css`:

1. **Cada color da al menos 3:1 contra el disco.** Son gráficos, no texto: el
   criterio es WCAG 1.4.11, no el 4,5:1 del texto.
2. **No hay ningún verde.** "Respaldado" y "sin divergencia detectada" son
   azules, por dos razones: junto al rojo de "contradicho", un verde es el par
   que no distingue quien no ve el rojo-verde; y "sin divergencia detectada"
   no es dar por bueno (DEC-016), que es lo que un verde diría.
3. **Dentro de un mismo eje, dos estados se separan siempre por claridad
   (≥ 15 en L\*) o por azul-amarillo (≥ 30 en b\*)**, sin contar el eje
   rojo-verde. Por eso "parcial" es un ámbar claro frente al rojo oscuro de
   "contradicho".
4. **`error` es gris pizarra, no rojo.** Un fallo de la API no dice nada de la
   afirmación y no puede leerse como "contradicho".

Honestidad sobre la regla 3: es una **aproximación**, no una simulación de
daltonismo, y los umbrales 15 y 30 son márgenes del proyecto, no de ninguna
norma. Un primer criterio más laxo (distancia ≥ 20 en el plano L\*–b\*) dejaba
pasar un verde junto al rojo, y se descubrió rompiendo la paleta a propósito;
el actual lo rechaza. La simulación de verdad queda pendiente (§9, punto 25).

**Tamaño.** 54 px con ratón y 44 px con dedo, los dos como tokens
(`--veritai-bolita-tamano-escritorio`, `-movil`). "Móvil" es **puntero grueso**
(`pointer: coarse`), no ancho de ventana: una ventana estrecha en un escritorio
sigue teniendo ratón, y lo que pide 44 px es el dedo (WCAG 2.5.5).

**Movimiento.** Al pasar por encima (solo donde hay puntero que pueda hacerlo,
`hover: hover`), el disco crece un poco y se ilumina con un halo del color del
estado; al pulsar, encoge; mientras analiza, un halo late. Con
`prefers-reduced-motion: reduce` nada crece, nada encoge y nada late: el halo
de "analizando" se queda fijo y visible, porque el estado no puede depender de
una animación que el usuario ha pedido no ver. La etiqueta va fuera del disco
a propósito: en una primera versión colgaba del elemento que se escalaba, y el
texto crecía al pasar por encima y encogía al pulsar; se vio en la vitrina.

**Teclado y foco.** Es un `<button>` nativo: el navegador lo pone en el orden
de tabulación y convierte Enter y Espacio en `click`; no hay manejadores de
teclado propios. El foco se ve con un anillo (`:focus-visible`) de un solo
color para los dos temas, `--veritai-color-foco`: se dibuja fuera de la
bolita, sobre la página de un tercero cuyo fondo no se conoce, así que se
eligió uno que da 4,5:1 contra blanco y 4,7:1 contra negro.

**Lo que no hace todavía** está en §9, puntos 19 a 26: no está colocada en
ninguna página, sus eventos no se cortan hacia la página, su tema sigue al
sistema y no a la página, y `desconocido` no se anota en ningún registro.

---

## 3. Convenciones de nombres

Lo que ya fija `CLAUDE.md` §5 se mantiene: código y comentarios en español;
TypeScript con `camelCase` para funciones y variables y `PascalCase` para
tipos; ramas `feat/`, `fix/`, `docs/`, `chore/` en kebab-case. Lo que sigue
lo completa para la interfaz.

| Qué | Regla | Correcto | Incorrecto |
|---|---|---|---|
| Ficheros `.ts` y `.css` | kebab-case, en español, un concepto por fichero | `panel-veredicto.ts`, `numero-trazado.css` | `PanelVeredicto.ts`, `verdictPanel.ts`, `utils.ts` |
| Carpeta de componente | el mismo nombre que su `.ts` y su `.css` | `componentes/panel-veredicto/{panel-veredicto.ts, panel-veredicto.css}` | `componentes/Panel/index.ts` |
| Función que crea un componente | `crear` + nombre en PascalCase; recibe datos del contrato y el `locale`; devuelve `HTMLElement` | `crearPanelVeredicto(veredicto, locale)` | `renderPanel()`, `PanelVeredicto()`, `pintar()` que escribe en `document` |
| Tipos | PascalCase, sin prefijo `I` ni sufijo `Type` | `Veredicto`, `NumeroUsado`, `EstrategiaLocalizacion` | `IVeredicto`, `VeredictoType`, `verdict` |
| Enums del contrato | el **valor** es el de la API, tal cual; el nombre del miembro en PascalCase | `Truth.Supported = "supported"`, `Context.DivergenceDetected = "divergence_detected"` | `Truth.OK`, `"verdadero"`, traducir el valor |
| Clases CSS | prefijo `veritai-`, bloque y elemento separados por `__`, modificador por `--`; el modificador de estado es el valor del enum, con el eje delante cuando el componente pinta más de uno | `.veritai-panel`, `.veritai-panel__titulo`, `.veritai-marca-eje--contradicted`, `.veritai-bolita--truth-contradicted` | `.panel`, `.ok`, `.titulo-rojo`, `.veritai-panel-titulo` |
| Variables CSS (tokens) | prefijo `--veritai-`, grupo y nombre semántico, nunca el valor en el nombre | `--veritai-color-texto`, `--veritai-color-truth-contradicted`, `--veritai-espacio-3`, `--veritai-radio-2` | `--fondo`, `--ok`, `--rojo`, `--veritai-14px` |
| Ganchos del DOM propio | atributo `data-veritai="<nombre>"` para lo que las pruebas o `aplicacion` necesiten localizar en **nuestro** DOM; nunca una clase | `data-veritai="recomprobar"` | `#recomprobar`, `.boton-recomprobar` usado desde código |
| Claves i18n | `seccion.nombre_en_snake`, minúsculas; mismo conjunto de claves y mismos marcadores `{x}` en `es.json` y `en.json` | `veredicto.titulo`, `motivo.PREVIOUS_EDITION_NOT_FOUND` | `VeredictoTitulo`, `titulo2`, una clave que solo existe en `es` |
| Claves i18n de enums | `<eje>.<valor del enum>` tal cual, para que el mapa sea trivial y la prueba de paridad lo compruebe | `truth.supported`, `context.undetermined`, `fase.analizando`, `motivo.EXTRACTION_FAILED` | `truth.ok`, `contexto.sin_divergencia` |
| Ficheros de sitio | `sitios/<sitio>.json`, nombre del sitio en minúsculas sin dominio | `sitios/x.json`, `sitios/instagram.json` | `sitios/x.com.json`, `sitios/X.json`, `sitios/twitter.ts` |
| Fixtures de página | `tests/fixtures/sitios/<sitio>/AAAA-MM-DD-<que-es>.html` | `tests/fixtures/sitios/x/2026-10-03-publicacion-con-cifra.html` | `tweet.html`, `test1.html` |
| Ficheros de prueba | `tests/<capa>/<nombre>.test.ts`, mismo nombre que el módulo probado | `tests/presentacion/panel-veredicto.test.ts` | `panel.spec.js`, `tests/misc.test.ts` |
| Nombres de pruebas | una frase en español que diga qué se comprueba, empezando por el sujeto | `test("el panel muestra el motivo de abstención cuando truth es insufficient_evidence")` | `test("works")`, `test("caso 3")` |
| Constantes | `MAYUSCULAS_CON_GUIONES`, con comentario de por qué ese valor, en un fichero de configuración, nunca en línea | `const TIEMPO_MAXIMO_API_MS = 4000; // el panel no debe colgarse si la API no responde` | `setTimeout(() => control.abort(), 4000)` |
| Textos de interfaz | siempre por `t()`; respetan `GLOSARIO.md` §Términos que NO se usan: nada de "falso", "verdadero", "fake", "engañoso", "el sistema cree" | `t("truth.contradicted")` → "Contradicho por la fuente" | "Noticia falsa", "Fiabilidad: 72 %" |

---

## 4. Qué está prohibido

Cada prohibición lleva la prueba que la hace cumplir (§5). Lo que no tiene
prueba todavía se marca.

| Prohibido | Por qué | Quién lo comprueba |
|---|---|---|
| Un color, tamaño, radio, sombra, duración o `z-index` escrito dentro de un componente, en su `.css` o en su `.ts` | Un valor suelto no se puede cambiar de tema ni auditar. Todo valor vive en `tokens.css` y se usa con `var(--veritai-...)` | `tests/arquitectura/literales-css.test.ts`: cualquier `#hex`, `rgb(`, `hsl(`, número con `px`/`rem`/`em`/`ms`/`s` fuera de `tokens.css` falla. Literales permitidos: `0`, `1` (line-height), `100%`, `auto`, `inherit`, `none`, `transparent`, `currentColor`. Pendiente como prueba general; para `bolita.css` lo comprueba ya `tests/presentacion/bolita.test.ts` |
| Un selector CSS sin prefijo `veritai-` en cualquier hoja que se inyecte en una página de terceros, incluidos los selectores de elemento (`h1`, `table`, `button`) | Se inyecta en el DOM de otro. Aunque el shadow root lo aísle, la regla es doble: ni fuga hacia fuera ni dependencia de que el aislamiento exista | `tests/arquitectura/prefijos-css.test.ts`: en `componentes/**/*.css` y `raiz.css` todo selector empieza por `.veritai-`, `:host` o `[data-veritai`. Pendiente como prueba general; para `raiz.css` y `bolita.css` lo comprueba ya `tests/presentacion/montar.test.ts` |
| `rem`, `vw`, `vh` y cualquier unidad que dependa de la página, en una hoja que se inyecta o en un token que esa hoja use | Dentro de la página de un tercero, `rem` es el `font-size` del `<html>` de esa página: lo nuestro cambiaría de tamaño según dónde se monte | `tests/presentacion/montar.test.ts` |
| Lógica de negocio en la capa visual: calcular una tasa, comparar dos valores, decidir un estado a partir de números, redondear | La interfaz no calcula veredictos (§1.3) | `tests/arquitectura/aritmetica.test.ts`: operadores `+ - * / %` sobre identificadores que vengan del contrato en `presentacion/`, `formato/`; y la prueba de trazabilidad visual de cada componente |
| Cualquier número mágico: tiempos de espera, reintentos, tamaños, límites, índices, el `2` de "2 servicios" | Un número sin nombre no se puede defender ni cambiar con seguridad | `tests/arquitectura/literales-ts.test.ts`: literales numéricos distintos de `0`, `1`, `-1` fuera de `config.ts`, `tokens.css` y los ficheros de prueba fallan |
| Un selector de la página de terceros escrito en código (`document.querySelector("article")`, `[data-testid=tweet]`) en cualquier capa que no sea `localizacion/`, y en `localizacion/` solo si viene de `sitios/*.json` | §7. El HTML de X cambia sin avisar; el selector tiene que estar donde se cambia sin tocar código | `tests/arquitectura/selectores.test.ts`: `querySelector`, `querySelectorAll`, `getElementsBy*`, `closest(` fuera de `localizacion/localizador.ts` y de las pruebas fallan; en `localizador.ts` el argumento tiene que ser una variable, nunca una cadena literal |
| Adivinar la posición de un elemento cuando las estrategias fallan: "el tercer `div`", "el primer bloque con más de 20 caracteres" | §7: cuando todo falla, nada se muestra y se registra | Revisión en el PR y la prueba de fixtures: una estrategia de tipo `estructura` solo puede partir de un ancla ya localizada |
| `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write` con cualquier dato interpolado; `eval`, `new Function`, `import()` con una cadena construida | Seguridad (`CLAUDE.md` §8, START-HERE §23 "Web / extensión") y porque la prueba de dependencias necesita imports estáticos | `tests/arquitectura/dom-inseguro.test.ts`. Los componentes construyen el DOM con `createElement` y `textContent`; `innerHTML` solo con una cadena literal constante, y aun así se prefiere no usarlo |
| Estilos en línea (`style="..."`, `elemento.style.color = ...`) y `!important` | Saltan los tokens y el tema | Prueba de literales; `!important` en cualquier `.css` falla |
| Traducir `explicacion` o cualquier texto ya renderizado; traducir un valor de enum | `CLAUDE.md` §10 | Revisión; la prueba de i18n exige que los textos de estado salgan de claves `truth.*`, `context.*`, `motivo.*` |
| Usar un valor de enum que no esté en `contrato/enums.ts`, o inventar un estado visual nuevo sin su enum | Enums cerrados en todas partes (`CLAUDE.md` §5) | `tests/arquitectura/enums-api.test.ts` y la prueba de `estados.ts` |
| Un componente que haga `fetch`, lea `location`, `chrome.*`, `localStorage` o `window` fuera de lo que recibe por parámetros | Rompe la matriz de §1.2 y la prueba sin navegador | Prueba de dependencias y revisión |
| Guardar o enviar al backend el HTML, el *feed* o el historial del usuario; registrar URLs con parámetros | START-HERE §23: "evitar enviar el feed completo", "no almacenar historial"; `CLAUDE.md` §8 | Revisión del PR; el registro de fallos solo admite `sitio`, `elemento`, `estrategias_probadas`, `version` y fecha (§7.4) |
| Un framework de UI, un cliente HTTP, una librería de CSS, una de i18n | Decisión del paquete (JS vanilla); coste 0; `CLAUDE.md` §7 (nada de dependencias por ahorrar líneas) | Revisión de `package.json` en el PR |

---

## 5. Reglas de pruebas

### 5.1 Herramientas

**Vitest** con entorno **happy-dom** y cobertura **v8**. Vitest porque usa la
misma configuración y el mismo pipeline que Vite, que ya está; happy-dom
porque es más ligero que jsdom y basta para `createElement`, eventos y shadow
root. Alternativas descartadas: Jest (duplica la cadena de compilación de
TypeScript y no entiende `import.meta.env` sin más configuración), Playwright
para todo (lento, necesita navegador real; queda para humo e2e al final, no
para el día a día). Son tres dependencias de desarrollo: `vitest`,
`happy-dom`, `@vitest/coverage-v8`.

`npm test` ejecuta todo; `npm run build` ejecuta `tsc`, `vitest run` y
`vite build`, en ese orden, y falla si falla cualquiera (conectado el
2026-10-03 al quedar las pruebas en verde). Las pruebas corren dentro del contenedor
`veritai-web`, como las de la API corren en el suyo: `tests/`,
`vitest.config.ts` y `arquitectura.json` van montados en solo lectura
(`docker-compose.override.yml`); hace falta reconstruir la imagen para que
tenga Vitest. Las pruebas que solo leen ficheros llevan
`// @vitest-environment node` en la primera línea: bajo happy-dom,
`import.meta.url` no es una URL `file:`.

`vitest.config.ts` lleva `css: true`: sin eso Vitest sustituye por una cadena
vacía las hojas importadas con `?inline`, y `montar.ts` montaría raíces sin
estilos.

**Lo que happy-dom mide y lo que no** (comprobado el 2026-10-03, versión
20.14). Mide bien: el shadow root cerrado, las hojas adoptadas, que los
selectores de la página no entran y los nuestros no salen, las custom
properties con `var()`, y las media queries `prefers-color-scheme`,
`prefers-reduced-motion`, `pointer` y `hover` (`tests/_entorno.ts`; las
preferencias se fijan **antes** de montar, porque guarda los estilos ya
calculados). No mide: `all`, las reglas `:host`, `:hover` y `:focus-visible`,
los pseudo-elementos, las propiedades abreviadas (`animation`, `transition`:
por eso las hojas usan las desglosadas), la maquetación, ni la conversión de
Enter y Espacio en `click` de un `<button>`. Lo que no mide se comprueba por
estructura (la regla está y dice lo que debe) y en un navegador de verdad
(§5.4).

### 5.2 Tipos de prueba y qué cubre cada uno

| Tipo | Qué cubre | Dónde | Ejemplo |
|---|---|---|---|
| **Unitaria pura** | Funciones sin DOM: `t()`, `formatearNumero`, `validarVeredicto`, el mapa de `estados.ts`, cada estrategia de `localizacion/` sobre un fragmento HTML pequeño | `tests/{i18n,formato,contrato,presentacion,localizacion}/` | `formatearNumero("1762936", "es")` devuelve `"1.762.936"` y `formatearNumero("1762936", "en")` devuelve `"1,762,936"`, sin cambiar un dígito |
| **De componente** | Cada componente se renderiza en happy-dom con un veredicto de `fixtures/api/`, **una vez por estado visual** y en los dos idiomas. Se comprueba: los ganchos `data-veritai` presentes; los textos salen de `t()`; **trazabilidad visual**: toda secuencia de dígitos del texto renderizado corresponde a un `valor` de `numeros_usados` o del claim; **escapado**: un `raw_value_span` con `<img onerror=...>` se pinta como texto y no crea ningún elemento | `tests/presentacion/` | `crearPanelVeredicto(fixtureE066, "en")` muestra `evidencia_al_publicar` y `evidencia_vigente` con sus dos fechas y ningún número que no esté en el JSON |
| **De arquitectura** | Dependencias (§1.4); prefijos CSS; literales CSS y TS; selectores fuera de `localizacion`; DOM inseguro; **paridad de enums con la API**: la prueba lee `apps/api/veritai/domain/enums.py` y comprueba que los valores de `contrato/enums.ts` son exactamente los mismos | `tests/arquitectura/` | Si alguien añade `PREVIOUS_EDITION_OUT_OF_MAP` en Python y no en TypeScript, falla |
| **De i18n** | `es.json` y `en.json` tienen el mismo conjunto de claves y los mismos marcadores `{x}`; toda clave usada en `src/` existe; toda clave `truth.*`, `context.*`, `motivo.*`, `clase.*` cubre todos los valores del enum | `tests/i18n/` | Un valor de `AbstainReason` sin texto en `en.json` falla |
| **De contrato** | Las respuestas JSON guardadas de la API real (`fixtures/api/`, con fecha) pasan `validarVeredicto`; un JSON al que le falta `raw_value_span` en un número **no** pasa | `tests/contrato/` | |
| **De sitio (fixtures)** | Para cada `sitios/<sitio>.json` y cada fragmento HTML guardado de ese sitio: cada elemento se localiza, por la estrategia esperada, con el texto esperado; las estrategias están en el orden admisible; el JSON cumple `esquema.json`. Detalle en §7.5 | `tests/localizacion/sitios.test.ts` + `tests/fixtures/sitios/` | |
| **De accesibilidad básica** | Roles y etiquetas en los componentes (`role`, `aria-label`, `<button>` con texto); el **contraste** de cada par texto/fondo de `tokens.css` en tema claro y oscuro es ≥ 4,5:1 (WCAG AA), calculado por la prueba | `tests/presentacion/accesibilidad.test.ts` | Añadir `--veritai-color-estado-mixed` con contraste 3,1:1 sobre el fondo oscuro falla |
| **De humo e2e** (más adelante, no bloquea) | Playwright: el panel suelto carga, pide `/health`, cambia de idioma. Y, cuando exista la extensión, carga en un Chromium con un fixture servido en local | `tests/e2e/` | Declarado, no exigido hasta que exista la extensión |

### 5.3 Cobertura mínima y definición de terminado

- **Cobertura global de `src/`: 80 % de líneas y 80 % de ramas**, umbral en
  `vitest.config.ts`; la construcción falla por debajo.
- **100 % de líneas** en `contrato/`, `formato/`, `presentacion/estados.ts` e
  `i18n/index.ts`, y en `localizacion/`. Son funciones puras: no hay excusa
  para una rama sin probar, y son las que deciden qué se ve.
- Por qué no 100 % global: `aplicacion/`, `extension/` y `montar.ts` tocan
  APIs del navegador que happy-dom no simula entera; se cubren con humo e2e.

**Nada se da por terminado sin prueba.** Un PR de interfaz se puede fusionar
solo si:

1. tiene su prueba (nueva o ampliada) y la lista de qué comprueba;
2. `npm test` pasa con la cobertura en el umbral;
3. `npm run typecheck` pasa sin `any` nuevos ni `// @ts-ignore`;
4. las pruebas de arquitectura pasan sin excepciones añadidas;
5. `docs/BITACORA.md` dice qué se hizo y qué se verificó, como en el resto
   del proyecto.

Lo que no tiene prueba no está hecho; está empezado.

### 5.4 La vitrina y lo que solo mide un navegador de verdad

`npm run vitrina` sirve `apps/web/vitrina/` en `http://127.0.0.1:5174/vitrina/`
y la abre. Es una página local de desarrollo, como `scripts/` y `tests/`: vive
fuera de `src/`, no entra en el build ni en la extensión, y no está conectada
a ninguna página real ni a la API. Solo usa lo que usará `aplicacion`:
`crearRaizAislada` y `crearBolita`.

La página **hace de página de un tercero**: no carga ninguna hoja de VERITAI,
tiene el `<html>` a 22 px para que un `rem` nuestro se note, y tiene una
**zona hostil** que aplica con `!important` reglas de elemento, reglas con
nuestras mismas clases, propiedades heredables y hasta nuestros propios
tokens. Al final lleva una **autocomprobación**: una tabla con lo que el
navegador mide en ese momento (`getComputedStyle`, `getBoundingClientRect`)
frente a lo esperado. Es el sitio donde se comprueba lo que happy-dom no
modela.

El 2026-10-03 se ejecutó en Chrome 154 sin ventana, con un perfil desechable:
las 14 comprobaciones bien, en tema claro, en oscuro y forzando movimiento
reducido. Manejando ese Chrome por su protocolo de depuración se comprobó
además que Tab entra en la bolita y muestra el foco y la etiqueta, que Enter y
Espacio la activan, que el foco no se pierde cuando llega el veredicto y que
con puntero táctil mide 44 × 44 px. Esa comprobación fue **manual y de una
vez**: no hay prueba de humo automatizada en el repositorio (§9, punto 26).

Dos defectos salieron de ahí y no de las pruebas: `direction` se heredaba de la
página (§2) y la etiqueta se escalaba con el disco (§2.2). Los dos tienen ya
su prueba.

---

## 6. Cómo se añade algo nuevo

### 6.1 Un estado visual nuevo

Un estado visual nuevo **solo** puede nacer de un valor nuevo en un enum de la
API. La interfaz no inventa estados.

1. El valor se añade primero en `apps/api/veritai/domain/enums.py` y en
   `docs/GLOSARIO.md`, con su DEC. Si eso no ha pasado, aquí no hay nada que
   hacer.
2. `src/contrato/enums.ts`: el mismo valor. La prueba de paridad
   (`tests/arquitectura/enums-api.test.ts`) deja de fallar.
3. `src/presentacion/estados.ts`: una entrada en el mapa, con su clase
   modificadora (`--<valor>`), su icono si lo lleva y su clave i18n.
4. `src/i18n/es.json` y `en.json`: la clave `<eje>.<valor>`, en los dos.
5. `src/presentacion/estilos/tokens.css`: el token
   `--veritai-color-<eje>-<valor>` (`--veritai-color-truth-<valor>`,
   `--veritai-color-context-<valor>`), en tema claro y oscuro. Tiene que
   pasar `tests/presentacion/accesibilidad.test.ts`: 3:1 contra el disco, no
   ser verde, y separarse de los demás estados de su eje por claridad o por
   azul-amarillo (§2.2).
6. El `.css` del componente que lo pinta: la regla
   `.veritai-<bloque>--<eje>-<valor> { color: var(--veritai-color-<eje>-<valor>); }`.
7. Pruebas: `tests/presentacion/estados.test.ts` (el mapa cubre el enum
   entero); un caso nuevo en la prueba del componente, con un fixture de API
   que tenga ese valor; la de i18n y la de contraste pasan solas o avisan.
8. `docs/GLOSARIO.md` ya lo tenía; `docs/BITACORA.md` lo anota.

Ficheros tocados: `enums.ts`, `estados.ts`, `es.json`, `en.json`,
`tokens.css` (si hace falta), el `.css` del componente, dos pruebas, la
bitácora. Ninguno más.

### 6.2 Un componente nuevo

1. Carpeta `src/presentacion/componentes/<nombre>/` con `<nombre>.ts` y
   `<nombre>.css`.
2. En el `.ts`, una sola función exportada: `crear<Nombre>(datos, locale):
   HTMLElement`. `datos` es un tipo de `contrato/` o un tipo propio definido
   en el mismo fichero a partir de él. Construye el DOM con `createElement` y
   `textContent`; marca con `data-veritai` lo que `aplicacion` o las pruebas
   necesiten encontrar; todo texto por `t()`; todo número por `formato/`.
3. En el `.css`, un bloque `.veritai-<nombre>` con sus elementos y
   modificadores; solo `var(--veritai-...)`.
4. `src/presentacion/montar.ts`: registrar la hoja para que se adjunte al
   shadow root.
5. Claves i18n nuevas en `es.json` y `en.json`.
6. `tests/presentacion/<nombre>.test.ts`: un render por estado visual y por
   idioma; ganchos; trazabilidad visual; escapado.
7. Si el componente necesita un dato que la API no da, **se para**: el dato
   se añade en la API con su DEC, o el componente no se hace. La interfaz no
   lo calcula.

### 6.3 Un color o un tamaño nuevo (un token)

1. ¿De verdad es nuevo? Si un token existente sirve, se usa. Un token por
   significado, no por valor: `--veritai-color-estado-undetermined`, no
   `--veritai-gris-2`.
2. `tokens.css`: el token en `:root` (tema claro) **y** en el bloque de tema
   oscuro. Los dos o ninguno.
3. Si es un color de texto o de fondo: la prueba de contraste lo coge sola;
   si no llega a 4,5:1, se ajusta el valor, no la prueba.
4. Se usa con `var(...)` donde haga falta. Ningún otro fichero cambia.

### 6.4 Un sitio nuevo

1. `src/sitios/<sitio>.json` con la forma de §7.2 (copiar `x.json` y
   cambiar los datos). `esquema.json` lo valida.
2. `tests/fixtures/sitios/<sitio>/AAAA-MM-DD-<que-es>.html`: al menos un
   fragmento real, anonimizado (§7.5), y su entrada en `INDICE.md`.
3. `tests/localizacion/sitios.test.ts` lo recoge solo: recorre todos los
   sitios y todos sus fixtures.
4. El build regenera `host_permissions` del manifiesto desde `sitios/*.json`.
5. **No se toca `localizacion/`, ni `aplicacion/`, ni ningún componente.** Si
   el sitio nuevo necesita un tipo de estrategia que no existe, eso sí es un
   cambio de código en `localizacion/estrategias.ts`, con su prueba y su
   línea en la bitácora, y se hace en un PR aparte, antes.

Hoy el único sitio del alcance es **X** (Fase 0, `03-2`). Instagram o
cualquier otro entra por este camino, sin excepciones.

### 6.5 Un recurso gráfico nuevo o un cambio del símbolo

1. El SVG va a `src/presentacion/marca/`, con `viewBox` cuadrado; si es la
   versión mínima, `fill="currentColor"` y sin ningún color literal.
2. Si cambia el símbolo, `npm run iconos` regenera `src/extension/iconos/`;
   los PNG se versionan con el cambio.
3. Un color nuevo del símbolo que la interfaz necesite como acento entra
   como token (§6.3), nunca como literal en un componente.
4. La prueba de componente del que lo usa comprueba el `alt` o el
   `aria-label` y que el nodo es `<img>` o `<svg><use>`, no `innerHTML`.

### 6.6 Una clave de texto nueva

`es.json` y `en.json` a la vez, mismo nombre, mismos marcadores. La prueba de
paridad falla si falta una. El texto respeta `GLOSARIO.md` §Términos que NO
se usan.

---

## 7. Resistencia al cambio de la página

VERITAI lee páginas de terceros que cambian su HTML sin avisar. X cambia las
clases generadas de sus componentes en cada despliegue; los atributos
`data-testid` duran meses; los roles ARIA y los elementos semánticos (`article`,
`time`) duran años. El diseño asume las tres velocidades.

### 7.1 Las cinco reglas

1. **Toda forma de localizar un elemento vive en `sitios/<sitio>.json`**, un
   fichero de datos separado del código que lo usa. Ningún selector escrito
   dentro de un componente, de `aplicacion/` ni de la extensión. Lo
   comprueba `tests/arquitectura/selectores.test.ts` (§4).
2. **Cada elemento se busca por varias estrategias, ordenadas de más estable
   a más frágil**, y se prueba la siguiente cuando una falla. El orden
   admisible es un enum cerrado (§7.3) y la prueba de sitios falla si un
   fichero lo desordena.
3. **Cuando todas fallan, el sistema no muestra nada y lo registra.** Nunca
   inventa una posición ni adivina. `localizar()` devuelve `null`;
   `aplicacion` no monta nada para ese elemento; `registro.ts` anota el
   fallo.
4. **Un fichero por sitio, con la misma forma.** `esquema.json` es la forma.
   Añadir un sitio no toca el código común (§6.4).
5. **Hay una prueba con HTML guardado de la página real** que comprueba que
   las estrategias encuentran lo que deben (§7.5).

### 7.2 La forma de un fichero de sitio

```json
{
  "sitio": "x",
  "version": 1,
  "verificado_el": "2026-10-03",
  "dominios": ["x.com", "twitter.com"],
  "elementos": {
    "publicacion": {
      "ambito": "documento",
      "obligatorio": true,
      "estrategias": [
        { "tipo": "accesibilidad", "selector": "article[role='article']", "comprobacion": ["texto_minimo"] },
        { "tipo": "semantica",     "selector": "article",                 "comprobacion": ["texto_minimo"] },
        { "tipo": "datos",         "selector": "[data-testid='tweet']",   "comprobacion": ["texto_minimo"] },
        { "tipo": "estructura",    "selector": "main section > div > div", "comprobacion": ["texto_minimo"] },
        { "tipo": "clase",         "selector": ".css-175oi2r.r-1loqt21",  "comprobacion": ["texto_minimo"] }
      ]
    },
    "texto": {
      "ambito": "publicacion",
      "obligatorio": true,
      "estrategias": [
        { "tipo": "accesibilidad", "selector": "[lang]",                    "comprobacion": ["texto_minimo", "unico"] },
        { "tipo": "datos",         "selector": "[data-testid='tweetText']", "comprobacion": ["texto_minimo", "unico"] }
      ]
    },
    "punto_de_anclaje": {
      "ambito": "publicacion",
      "obligatorio": false,
      "estrategias": [
        { "tipo": "accesibilidad", "selector": "[role='group']", "comprobacion": ["unico"] }
      ]
    }
  }
}
```

Los selectores de este ejemplo son ilustrativos: la forma es la regla; los
valores reales se escriben el día que se capture el primer fixture de X, y
se verifican contra él.

Campos, todos obligatorios salvo que se diga:

| Campo | Qué es |
|---|---|
| `sitio` | Nombre corto, igual que el fichero |
| `version` | Entero que sube cada vez que se cambia una estrategia. Va al registro de fallos para saber con qué versión falló |
| `verificado_el` | Fecha del último fixture contra el que se comprobó el fichero |
| `dominios` | Hosts donde aplica; de aquí salen los `host_permissions` del manifiesto |
| `elementos.<nombre>` | Un elemento lógico que la aplicación necesita. Los nombres son un enum cerrado: `publicacion`, `texto`, `punto_de_anclaje`, `autor`, `fecha`. Un nombre nuevo es un cambio de código en `aplicacion/` |
| `ambito` | Desde dónde se busca: `documento` o el nombre de otro elemento ya localizado. `texto` se busca **dentro de** `publicacion`; así un selector frágil nunca recorre toda la página |
| `obligatorio` | Si falla y es obligatorio, no se monta nada para esa publicación. Si no lo es, se monta sin él |
| `estrategias[]` | En orden de prueba. Cada una: `tipo` (§7.3), `selector` (CSS válido), `comprobacion[]` |
| `comprobacion[]` | Enum cerrado de condiciones que el resultado tiene que cumplir para que la estrategia cuente como acierto: `unico` (exactamente un nodo en el ámbito), `texto_minimo` (texto no vacío tras recortar espacios), `visible` (ocupa área en pantalla). Si el selector devuelve nodos pero la comprobación falla, la estrategia **ha fallado** y se pasa a la siguiente |

### 7.3 Tipos de estrategia y su orden

Un enum cerrado, de más estable a más frágil. Dentro de un elemento, los
tipos tienen que aparecer en este orden (se pueden omitir, no desordenar):

| Orden | `tipo` | Qué usa | Por qué está donde está |
|---|---|---|---|
| 1 | `accesibilidad` | `role`, `aria-*`, `lang` | Lo que X mantiene para lectores de pantalla; cambiarlo rompe la accesibilidad de su propio producto |
| 2 | `semantica` | Elementos HTML con significado (`article`, `time[datetime]`, `a[href]` con patrón) | Cambia poco; es la estructura del documento, no su estilo |
| 3 | `datos` | Atributos `data-*` como `data-testid` | Los usan sus propias pruebas automáticas; duran meses, pero no están prometidos a nadie |
| 4 | `estructura` | Posición relativa **a un ancla ya localizada** por un tipo anterior (`ambito`) | Depende de la maquetación; cambia con cada rediseño. Nunca se usa desde `documento` |
| 5 | `clase` | Clases generadas (`.css-175oi2r`, `.r-...`) | Cambian en cada despliegue. Están las últimas porque a veces son lo único que distingue dos nodos iguales; si son la única estrategia, el elemento se considera no localizable y se anota |

`localizacion/estrategias.ts` sabe ejecutar cada tipo. `sitios/*.json` dice
cuál usar. La separación es la que permite arreglar X sin tocar código.

### 7.4 Qué pasa cuando todo falla

`localizar()` devuelve `null`. `aplicacion/flujo.ts`:

- si el elemento es `obligatorio`, no monta nada para esa publicación;
- si no lo es, monta sin él;
- en los dos casos llama a `registrarFallo(...)`.

El registro es **local y sin contenido**: `sitio`, `elemento`, `version` del
fichero de sitio, lista de `tipo`s probados, fecha y hora. **Nunca** la URL
con parámetros, el texto de la publicación, el HTML ni el autor. En el panel
suelto se escribe en consola; en la extensión, en `chrome.storage.local` con
un contador por `(sitio, elemento)` que el *popup* muestra como "no se pudo
localizar la publicación en X (12 veces desde el 3 de octubre)". Eso es lo
que avisa al usuario y a Mateo de que X ha cambiado; nada se envía a la API.

### 7.5 La prueba con HTML real, y cómo se arregla cuando X cambia

**Los fixtures.** `tests/fixtures/sitios/x/AAAA-MM-DD-<que-es>.html` es un
fragmento real de la página (el `article` de una publicación, no la página
entera), capturado desde el navegador del propio usuario, con fecha en el
nombre. Se **anonimiza conservando la estructura**: nombres de usuario, texto
e imágenes se sustituyen por marcadores, los atributos y la jerarquía se
dejan tal cual, porque son lo que se prueba. `INDICE.md` dice de cada fixture
la fecha, el dominio sin parámetros y qué contiene. Esto no es recolección
automatizada ni evade nada (DEC-018): es el DOM que el usuario ya tiene
delante.

**La prueba.** `tests/localizacion/sitios.test.ts`, para cada
`sitios/<sitio>.json`:

1. el fichero cumple `esquema.json`;
2. las estrategias de cada elemento están en el orden de §7.3;
3. ninguna estrategia de tipo `estructura` tiene `ambito: "documento"`;
4. para **cada** fixture del sitio y **cada** elemento obligatorio,
   `localizar()` devuelve un nodo, y `INDICE.md` dice qué tipo de estrategia
   se espera que acierte y qué texto (anonimizado) tiene que contener;
   la prueba comprueba las tres cosas;
5. para cada elemento, si se **quita** la primera estrategia, la segunda
   sigue encontrando el nodo en al menos un fixture: la cadena de respaldo
   existe de verdad, no solo en el papel.

**Cómo se arregla cuando X cambia su HTML.** Hay que decirlo con claridad:
un fixture guardado **no** detecta por sí solo un cambio en la página real,
porque es una foto del pasado. Lo que avisa es, por este orden:

1. **El registro de fallos** (§7.4): el contador de `(x, publicacion)` o
   `(x, texto)` sube y el *popup* lo muestra. Es el único aviso en campo.
2. **Capturar un fixture nuevo**: abrir X, copiar el `outerHTML` del
   `article` afectado, anonimizarlo, guardarlo como
   `tests/fixtures/sitios/x/AAAA-MM-DD-<que-cambio>.html` y añadir su fila a
   `INDICE.md` con la estrategia que debería acertar.
3. **Ejecutar `npm test`**: la prueba de sitios falla en el fixture nuevo y
   dice qué elemento y qué estrategias se probaron. **Esa es la prueba que
   avisa**, y falla antes de que se toque nada.
4. **Tocar un solo fichero: `src/sitios/x.json`.** Añadir la estrategia que
   acierta en su lugar del orden, o corregir la que dejó de acertar. Subir
   `version` y poner `verificado_el`.
5. **Volver a ejecutar**: tienen que pasar **todos** los fixtures de X, los
   viejos y el nuevo. Si una estrategia nueva rompe un fixture viejo, se
   mantiene la vieja antes y la nueva después: así se cubre a los usuarios
   que aún ven el HTML antiguo.
6. Rama `fix/sitio-x-<que-cambio>`, bitácora con la fecha del cambio de X y
   la estrategia que se cayó.

**Qué no se toca** en ese arreglo: `localizacion/`, `aplicacion/`, ningún
componente, ninguna prueba salvo el fixture nuevo y su línea en `INDICE.md`.
Si para arreglarlo hace falta tocar código, es que el tipo de estrategia
necesario no existe, y eso es un cambio aparte (§6.4, punto 5).

---

## 8. Cómo encaja con el resto del proyecto

- **La API es la frontera.** La interfaz consume `POST /analisis` y
  `GET /health` y nada más. Si la interfaz necesita un dato nuevo, el dato
  nace en el dominio con su `raw_value_span` y su DEC; no se calcula en el
  navegador.
- **CORS.** La API ya exige una lista explícita de orígenes sin comodines
  (`CORS_ALLOWED_ORIGINS`, `config.py`). El panel suelto está en esa lista.
  La extensión tendrá su origen `chrome-extension://<id>`, que se añade a la
  lista cuando exista; nunca `*`.
- **Seguridad de la extensión** (START-HERE §23 "Web / extensión" y §25):
  CSP estricta en el manifiesto; sin `eval`; permisos mínimos (`activeTab` y
  los `host_permissions` que salen de `sitios/*.json`, nada global); no se
  envía el *feed* ni se guarda historial; el content script solo lee el
  texto del elemento `texto` localizado, cuando el usuario lo pide. Esto es
  lo que `SEGURIDAD.md` marca hoy como `n/a` y deja de serlo con la primera
  línea de la extensión: se implementa antes, no después.
- **Contenido externo es dato.** Todo lo que viene de la página de terceros
  y todo lo que viene de la API se trata como no confiable en el DOM:
  `textContent` siempre. Un `raw_value_span` con HTML dentro se pinta como
  texto.
- **i18n.** `CLAUDE.md` §10 y `00b` §2: se traduce la plantilla, jamás el
  resultado. La consecuencia concreta está en §1.3, punto 4: la explicación
  en inglés se compone en la interfaz a partir de los campos estructurados,
  no traduciendo `explicacion`.
- **Vocabulario.** Los estados visuales se llaman como los enums del
  `GLOSARIO.md`; los textos respetan su lista de términos que no se usan.
- **Limitación de alcance ya declarada.** El claim estructurado se prepara a
  mano (DEC-028; `TESIS-ENCUADRE.md` §Alcance declarado). La interfaz que
  gobierna este documento muestra veredictos sobre claims ya estructurados;
  el camino desde el texto de la página hasta ese claim no existe y no se
  decide aquí.

---

## 9. Lo que hoy no cumple estas reglas (foto del 2026-10-03; no se arregla en este documento)

Lo que existe se escribió antes de estas reglas y para otra cosa: comprobar
que el entorno levanta. Nada de esto es un error de entonces; es lo que hay
que mover antes del primer componente.

| # | Incumplimiento | Dónde | Regla |
|---|---|---|---|
| 1 | ~~Un solo módulo hace red, orquestación, construcción de HTML y escapado~~ **Hecho el 2026-10-03:** `cliente/api.ts`, `aplicacion/flujo.ts`, `presentacion/componentes/estado-servicio/`, `contrato/salud.ts`; `main.ts` solo arranca | `src/main.ts` | §1.1, §2 |
| 2 | ~~El tipo `RespuestaSalud` está definido en el módulo de arranque~~ **Hecho:** `contrato/salud.ts`, con validador `esRespuestaSalud` | `contrato/salud.ts` | §2 |
| 3 | ~~Número mágico: tiempo máximo `4000` en línea; `total: 2` servicios en línea~~ **Hecho:** `TIEMPO_MAXIMO_API_MS` en `cliente/config.ts`; el total de servicios es la longitud de la lista de servicios vigilados | `cliente/config.ts`, `estado-servicio.ts` | §4 |
| 4 | ~~El HTML se construye con plantillas de cadena e `innerHTML` interpolado~~ **Hecho:** `createElement` y `textContent`; `escapar()` desaparece; la prueba de DOM inseguro pasa | `estado-servicio.ts` | §4 |
| 5 | ~~Ganchos del DOM propio por `id` y clases~~ **Hecho:** `data-veritai="recomprobar"` y `data-veritai="idioma"`; el `<label for>` conserva un `id` con prefijo (`veritai-idioma`) porque la asociación accesible lo exige | `estado-servicio.ts` | §3 |
| 6 | ~~Variables CSS sin prefijo~~ **Hecho:** `tokens.css` con `--veritai-color-*`, `--veritai-espacio-*`, `--veritai-radio-*`, tipografía, pesos y medidas, en tema claro y oscuro | `presentacion/estilos/tokens.css` | §3 |
| 7 | ~~Clases sin prefijo~~ **Hecho:** bloque `.veritai-estado-servicio` con `__elemento` y `--estado`; `.veritai-pagina` y `.veritai-panel` en `base.css` | `estado-servicio.css`, `base.css`, `index.html` | §3, §4 |
| 8 | ~~Selectores de elemento globales~~ **Hecho:** ninguno; el `<body>` del panel suelto lleva `class="veritai-pagina"` y `base.css` solo se carga en `index.html`. `raiz.css` existe desde la bolita y tampoco tiene ninguno | `base.css`, `estado-servicio.css`, `raiz.css`, `bolita.css` | §4 |
| 9 | ~~Tamaños y radios literales fuera de tokens~~ **Hecho:** todos en `tokens.css`; comprobado declaración a declaración que las 57 declaraciones y los 16 colores (claro y oscuro) resuelven a los mismos valores que antes. La prueba automática de literales sigue pendiente | `tokens.css` | §4 |
| 10 | ~~Un fichero de estilos para todo~~ **Hecho:** `tokens.css`, `base.css` y `estado-servicio.css`; `raiz.css` y `montar.ts` llegaron con la bolita (2026-10-03) | `presentacion/estilos/`, `componentes/estado-servicio/` | §2 |
| 11 | La capa i18n toca el DOM: `fijarLocale` escribe `document.documentElement.lang` | `src/i18n/index.ts` línea 55 | §1.2 (`i18n` no importa nada ni toca el DOM); eso va a `presentacion/montar.ts` |
| 12 | `t()` cae en silencio al catálogo español si la clave falta en inglés; sin prueba de paridad, una traducción que falta pasa desapercibida | `i18n/index.ts` línea 70 | §5.2 prueba de i18n |
| 13 | ~~Ninguna prueba de la interfaz; no hay runner ni `npm test`~~ **Desde el 2026-10-03:** Vitest 5 con happy-dom; `npm test` y `npm run test:cobertura`; ocho ficheros y 86 pruebas: tres de arquitectura (dependencias, DOM inseguro, paridad de enums con la API) y cinco de presentación (`estado-servicio`, `estados`, `bolita`, `montar`, `accesibilidad`), **todas en verde**; `build` exige `npm test`. **`npm run test:cobertura` sigue en rojo, y ya lo estaba**: los ficheros nuevos están al 100 %, pero `contrato/salud.ts` (40 % de líneas), `i18n/index.ts` (87,5 %), `cliente/`, `aplicacion/` y `main.ts` no tienen prueba, y las ramas quedan en el 66 % frente al 80 % exigido. Siguen pendientes de §5.2: las pruebas generales de prefijos y literales CSS, la de selectores, la de i18n (paridad de catálogos), contrato, sitios, y la de contraste para todos los pares de `tokens.css` (hoy solo los que usa la bolita) | `package.json`, `vitest.config.ts`, `tests/` | §5 |
| 14 | Ni lint ni formateador para TypeScript, cuando la API tiene `ruff` y `ruff format` | `apps/web/` | §5.3 punto 3 exige al menos `typecheck`; un lint es deuda declarada |
| 15 | ~~No existe `arquitectura.json` ni prueba de dependencias~~ **Desde el 2026-10-03** existen `arquitectura.json` y `tests/arquitectura/dependencias.test.ts`, en verde tras la reestructuración. La prueba equivalente del lado Python sigue siendo deuda (`ARQUITECTURA.md` §3) | `apps/web/`, `ARQUITECTURA.md` §3 | §1.4 |
| 16 | `index.html` no declara CSP; el panel suelto la necesitará y la extensión la exige | `index.html` | §8 |
| 17 | La explicación del veredicto se genera solo en español en el dominio (`plantilla.py`, `SALIDA`, `MOTIVOS`); la interfaz en inglés no puede mostrarla sin incumplir §10, y hoy no tiene plantillas propias para recomponerla | `apps/api/veritai/domain/plantilla.py` | §1.3 punto 4; es trabajo de interfaz, no de dominio |
| 18 | `sitios/`, `localizacion/`, fixtures y extensión no existen. No es un incumplimiento: es lo que este documento ordena antes de escribirlos | — | §7 |
| 19 | La bolita no está colocada en ninguna página. Falta decidir cómo se ancla el anfitrión a la esquina de la publicación sin tocar el CSS de la página, y de qué lado sale la etiqueta (hoy, siempre a la izquierda) | `aplicacion/`, `montar.ts` | §2.2; es el paso de integración, no el del componente |
| 20 | Los eventos de la bolita salen del shadow root hacia la página: un clic o un Enter sobre ella puede disparar los manejadores de la página (en X, abrir la publicación). Hay que cortarlos en la raíz aislada al integrar | `montar.ts` | §2 |
| 21 | El tema de lo inyectado sigue al sistema (`prefers-color-scheme`), no al tema que tenga la página: en una página oscura con el sistema en claro, la bolita sale clara | `tokens.css` | §2.2 |
| 22 | El símbolo de la bolita se carga por URL (`mask-image`). En la extensión esa URL tiene que ser un recurso accesible desde la página, o ir incrustada, y puede chocar con la CSP de la página | `bolita.css`, `extension/` | §8 |
| 23 | `desconocido` se pinta pero no se anota en ningún registro: `registro.ts` no existe. Anotarlo es trabajo de `aplicacion` | `aplicacion/` | §1.3 punto 2 |
| 24 | El cambio de estado no se anuncia a un lector de pantalla si el foco no está en la bolita: no hay región `aria-live` | `bolita.ts` | §2.2; se decide con el panel |
| 25 | La comprobación de daltonismo es una aproximación (CIELAB sin el eje rojo-verde), no una simulación, y sus umbrales son del proyecto. La fuente que se quiso consultar para las matrices de simulación no se pudo abrir: el `robots.txt` de `www.inf.ufrgs.br` devolvió 403 y no se insistió (DEC-021). Sin fuente verificada no se usan constantes de memoria. `NEEDS_REVIEW`: la referencia (recordada como Machado, Oliveira y Fernandes, 2009) está sin comprobar | `tests/presentacion/_color.ts` | §2.2 |
| 26 | Lo que solo mide un navegador de verdad (teclado, foco, hover, herencia) se comprobó a mano con Chrome y la vitrina; no hay humo e2e automatizado. Y dentro del contenedor `web` no se montan ni `vitrina/` ni `apps/api/veritai/domain/enums.py`: ahí la vitrina no se sirve y la prueba de paridad de enums se omite, a la vista | `vitrina/`, `docker-compose.override.yml` | §5.2, §5.4 |

Lo que **sí** cumple ya: tema claro y oscuro con variables (la idea de los
tokens está, falta el prefijo y la separación); `escapar()` con `textContent`;
tiempo máximo con `AbortController`; la regla de i18n hecha código y
documentada en el propio fichero; CORS con lista explícita en la API; `src/`
montado en solo lectura; puerto publicado solo en `127.0.0.1`; TypeScript
estricto con `noUncheckedIndexedAccess`.

Orden que se siguió el 2026-10-03, decidido por Mateo: primero el runner y
las pruebas de arquitectura (§5.1), en rojo contra el código de entonces;
después `main.ts` a las capas (§2) con `tokens.css` y prefijos, sin cambiar lo
que se ve, y `estado-servicio` como primer módulo de presentación. **Quedan
abiertos los puntos 11, 12, 14, 16 y 17, las pruebas que faltan del 13 (con
la cobertura en rojo), y los puntos 19 a 26, que nacen con la bolita.** El
2026-10-03 se construyó la bolita (§2.2), el primer componente pensado para
inyectarse; no está conectada a ninguna página. El panel del veredicto es el
paso siguiente.
