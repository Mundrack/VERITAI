/**
 * Orquestacion del panel suelto (docs/ARQUITECTURA-VISUAL.md §1.1, capa
 * aplicacion): pide a cliente el estado de la API, a presentacion el elemento,
 * y lo monta. Es la unica capa que conoce a todas las demas.
 */

import { consultarSalud } from "../cliente/api";
import { fijarLocale, localePorDefecto, type Locale } from "../i18n";
import { crearEstadoServicio } from "../presentacion/componentes/estado-servicio/estado-servicio";

/** Arranca el panel en `raiz`: idioma por defecto y primera consulta. */
export function iniciar(raiz: HTMLElement): void {
  fijarLocale(localePorDefecto());
  void refrescar(raiz);
}

async function refrescar(raiz: HTMLElement): Promise<void> {
  const salud = await consultarSalud();
  const vista = crearEstadoServicio(
    { salud, consultadoEn: new Date() },
    {
      alRecomprobar: () => void refrescar(raiz),
      alCambiarIdioma: (locale: Locale) => {
        fijarLocale(locale);
        void refrescar(raiz);
      },
    },
  );
  raiz.replaceChildren(vista);
}
