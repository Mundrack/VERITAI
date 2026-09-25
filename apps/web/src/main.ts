/**
 * Panel de comprobacion del entorno local de VERITAI.
 *
 * Alcance deliberadamente minimo: prueba que la cadena completa
 * navegador -> API -> PostgreSQL esta viva. Nada mas.
 * Los componentes de dominio llegan despues de PILOT_GO.
 */

import { fijarLocale, localesDisponibles, localePorDefecto, obtenerLocale, t, type Locale } from "./i18n";

interface RespuestaSalud {
  servicio: string;
  version: string;
  entorno: string;
  base_de_datos: string;
}

const URL_API: string = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

/** Escapa texto antes de insertarlo en el DOM. Ningun dato externo se concatena en crudo. */
function escapar(valor: string): string {
  const div = document.createElement("div");
  div.textContent = valor;
  return div.innerHTML;
}

async function consultarSalud(): Promise<RespuestaSalud | null> {
  const control = new AbortController();
  const limite = setTimeout(() => control.abort(), 4000);
  try {
    const respuesta = await fetch(`${URL_API}/health`, { signal: control.signal });
    if (!respuesta.ok) return null;
    return (await respuesta.json()) as RespuestaSalud;
  } catch {
    return null;
  } finally {
    clearTimeout(limite);
  }
}

function marca(activo: boolean, texto: string): string {
  return `<span class="${activo ? "ok" : "mal"}">${escapar(texto)}</span>`;
}

function pintar(salud: RespuestaSalud | null): void {
  const raiz = document.getElementById("app");
  if (!raiz) return;

  const apiViva = salud !== null;
  const dbViva = salud?.base_de_datos === "conectada";
  const activos = (apiViva ? 1 : 0) + (dbViva ? 1 : 0);

  const opciones = localesDisponibles()
    .map(
      (l) =>
        `<option value="${l}"${l === obtenerLocale() ? " selected" : ""}>${l.toUpperCase()}</option>`,
    )
    .join("");

  raiz.innerHTML = `
    <h1>${escapar(t("app.titulo"))}</h1>
    <p class="subtitulo">${escapar(t("app.subtitulo"))}</p>
    <div class="aviso">${escapar(t("app.aviso_puerta"))}</div>

    <h2>${escapar(t("estado.titulo"))}</h2>
    <table>
      <tbody>
        <tr>
          <th>${escapar(t("estado.api"))}</th>
          <td>${marca(apiViva, apiViva ? "OK" : t("estado.sin_respuesta"))}</td>
        </tr>
        <tr>
          <th>${escapar(t("estado.base_de_datos"))}</th>
          <td>${marca(dbViva, dbViva ? t("estado.conectada") : t("estado.no_disponible"))}</td>
        </tr>
        <tr>
          <th>${escapar(t("estado.entorno"))}</th>
          <td>${escapar(salud?.entorno ?? "-")}</td>
        </tr>
        <tr>
          <th>${escapar(t("estado.version"))}</th>
          <td>${escapar(salud?.version ?? "-")}</td>
        </tr>
      </tbody>
    </table>

    <div class="acciones">
      <button id="recomprobar">${escapar(t("acciones.recomprobar"))}</button>
      <label for="idioma">${escapar(t("acciones.idioma"))}</label>
      <select id="idioma">${opciones}</select>
    </div>

    <p class="pie">
      ${escapar(t("plantilla.servicios_activos", { activos, total: 2 }))} &middot;
      ${escapar(t("plantilla.consultado_en", { hora: new Date().toLocaleTimeString(obtenerLocale()) }))}
    </p>
  `;

  document.getElementById("recomprobar")?.addEventListener("click", () => void refrescar());

  document.getElementById("idioma")?.addEventListener("change", (evento) => {
    const seleccion = (evento.target as HTMLSelectElement).value;
    // Se vuelve a renderizar desde las plantillas del nuevo idioma.
    // No se traduce el HTML ya pintado. Ver la regla en src/i18n/index.ts.
    fijarLocale(seleccion as Locale);
    void refrescar();
  });
}

async function refrescar(): Promise<void> {
  pintar(await consultarSalud());
}

fijarLocale(localePorDefecto());
void refrescar();
