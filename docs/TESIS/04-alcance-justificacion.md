> **Esqueleto. Nada redactado.** Solo estructura y qué material del repositorio
> alimenta la sección. Nombre y orden de la sección: `NEEDS_REVIEW` hasta
> cotejar con la plantilla de titulación de la UDLA (P-06, no está en el repo).
> Los números llevan fuente y fecha; los que dependen de la jornada 5 o del
> arnés sobre el conjunto congelado están marcados **pendiente**.

# 4. Alcance declarado y justificación

**Propósito.** Para quién y sobre qué funciona el sistema, con los límites
escritos antes de medir; y por qué merece una tesis.

## Material que lo alimenta

| Qué | De dónde | Número |
|---|---|---|
| Publicadores de nivel 1 | DEC-024; `docs/TESIS-ENCUADRE.md` §Alcance declarado | nivel 1: 84,2 % de recuperabilidad en el piloto; resto 58,3 % (`PILOT-DECISION`, 2026-09-25) |
| Emisores del conjunto de evaluación | DEC-032: INE, Portal Estadístico de Criminalidad, SEPE, Banco de España; FMI e `interior.gob.es` fuera por 403 | 9 casos bloqueados en cubeta E (`validar_evaluacion.py`, 2026-09-27: E = 11) |
| Cuota de emisor | diseño §1 (INE ≤ 70 %) y §4f | INE 41/66 = 62,1 % (2026-09-27) |
| Mapa cerrado de operaciones del INE | `docs/PROPUESTA-2B.md`; `apps/api/veritai/infrastructure/ine/mapa_anexos.py` | 8 operaciones; ~1 h por operación nueva; fuera del mapa = fallo de cobertura declarado |
| Límite del fenómeno 2b | diseño §4d y §4g | 2b solo en 2 de las 8 operaciones (EOH, EOAT) |
| Lo que sale del corpus | DEC-013 (P08, P09), DEC-027 (`other_observed`) | |
| Lo que no se implementa | `CLAUDE.md` §11; `02-1` §Fuera del alcance | |
| Alcance honesto tras el piloto | `research/PILOT-FINDINGS.md` §4 | |
| Justificación (por qué es tesis) | `02-1` §"Por qué esto sí es una tesis"; `03-2` | contrastar con el encuadre vigente |
| Coste variable ~0 y reproducibilidad | `CLAUDE.md` §7 (librerías prohibidas), DEC-018 | |

## Qué afirma esta sección que hoy no está respaldado

| Afirmación | Dónde se afirma | Qué falta | Buscar en |
|---|---|---|---|
| Los publicadores de nivel 1 (organismos con API, dataset o boletín en URL estable) son un alcance con sentido; los demás son una limitación | DEC-024; piloto 84,2 % / 58,3 % | marco de datos abiertos oficiales y de acceso automatizado; qué se sabe de la cobertura de API en organismos estadísticos | C8, C9 |
| No evadir bloqueos anti-bot es la conducta correcta de un agente recolector, y un rechazo es un resultado | DEC-018, DEC-021 | ética y legalidad de la recolección automatizada; `robots.txt` y términos de uso | C8 |
| Coste variable ~0 y reproducibilidad justifican prohibir APIs comerciales como dependencia | `CLAUDE.md` §7 | literatura sobre reproducibilidad en sistemas con modelos y sobre coste de verificación | C6, C7 |
| El mapa cerrado de 8 operaciones es un alcance defendible y un 2b fuera del mapa es un fallo de cobertura, no un error | `PROPUESTA-2B`; DEC-035 | precedente de "cobertura declarada" en sistemas de verificación | C1, C2 |
| Esto es una tesis (y no un producto): el problema es abierto y el método es evaluable | `02-1` §Por qué esto sí es una tesis | estado del arte que muestre el hueco | C1, C2, C3 |

## No entra

Modelo de negocio, nombre comercial, empresa patrocinadora (`00b`, P-07):
aplazados y sin efecto técnico.
