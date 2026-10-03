/**
 * Arranque del panel suelto (index.html). Solo monta la aplicacion en #app.
 * Red, orquestacion y pintado viven en sus capas (docs/ARQUITECTURA-VISUAL.md).
 */

import { iniciar } from "./aplicacion/flujo";

const raiz = document.getElementById("app");
if (raiz) iniciar(raiz);
