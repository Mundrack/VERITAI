# Seguridad

> Este documento lista los controles **ya implementados y verificados**, no los
> planeados. Lo que falta está en su propia sección, dicho como falta.
>
> Las reglas completas están en `CLAUDE.md` §8 y en el START-HERE §23–25. Esto es
> el registro de qué está hecho de verdad.

**Última actualización:** 2026-09-25 (Puerta 2)

---

## Estado en una línea

**Un solo componente toca internet: el cliente del INE** (`infrastructure/ine/tempus.py`),
y solo a `https://servicios.ine.es`, por allowlist. No hay parsing de HTML ni
de PDF, no hay LLM, y `POST /analisis` no acepta URLs: el claim llega ya
estructurado. Por eso los controles de SSRF general, prompt injection y
archivos **siguen sin implementar** y no deben darse por hechos; lo que sí
está hecho es el perímetro del entorno y el perímetro de ese único conector.

---

## Implementado y verificado

### Red y exposición

| Control | Dónde | Verificado |
|---|---|---|
| Puertos publicados solo en `127.0.0.1`, nunca `0.0.0.0` | `docker-compose.yml` | ✅ `docker compose ps` muestra `127.0.0.1:8000->8000/tcp` |
| Red propia `veritai_net`, aislada | `docker-compose.yml` | ✅ |
| CORS con lista blanca explícita | `veritai/main.py` | ✅ |
| El comodín `*` en CORS es un error de arranque | `veritai/config.py` | ✅ test `test_cors_rechaza_comodin` |

**Por qué importa el primero.** La forma corta de publicar un puerto
(`8000:8000`) liga a `0.0.0.0`: el servicio queda accesible desde cualquier
equipo de la red local, incluida una wifi pública.

### Contenido externo: el conector INE (Puerta 2)

| Control | Dónde | Verificado |
|---|---|---|
| Allowlist de host: solo `servicios.ine.es`, solo HTTPS; el id de tabla es un entero y `nult` está acotado | `tempus.py` | ✅ `test_cliente_valida_tabla_y_allowlist` |
| **No se siguen redirecciones** (`follow_redirects=False`) | `tempus.py` | ✅ |
| Timeout por petición y tope de bytes leído en streaming: una respuesta lenta o enorme no tumba la API | `tempus.py`, `config.py` (`HTTP_TIMEOUT_S`, `HTTP_MAX_BYTES`) | ✅ `test_cliente_corta_respuestas_demasiado_grandes` |
| Agente identificado en cada petición (`VERITAI-prototipo/0.1 …`) | `tempus.py` | ✅ `test_cliente_devuelve_texto_crudo_e_identifica_al_agente` |
| Un 401/403/406/418/429 cierra el caso: **no se evade nada** (DEC-018, DEC-021) | `tempus.py` | ✅ `test_cliente_respeta_el_rechazo_del_publicador` |
| El JSON del INE se trata como **dato**, nunca como instrucción: se parsea con `json.loads`, se casa la serie por nombre exacto y cada número conserva su span literal; nada de `eval`, nada de `shell` | `extractor.py`, `proveedor.py` | ✅ `test_extractor_falla_ante_json_roto_o_spans_que_no_cuadran` |
| Entrada de `POST /analisis` acotada por pydantic: texto ≤ 2000, notas ≤ 2000, `claim_id` con patrón, emisor `Literal["INE"]`, periodos parseados, etiquetas ≤ 10 × 80 | `api/routes/analisis.py` | ✅ `test_rechaza_emisores_fuera_de_alcance_y_periodos_malos` |
| Excepción no prevista → 500 con solo el nombre del tipo; la traza va al log, nunca al cliente. El rechazo del publicador no es un error HTTP: el caso de uso lo convierte en abstención (`PRIMARY_SOURCE_NOT_FOUND`) y queda en el veredicto | `api/routes/analisis.py`, `application/analizar_claim.py` | ✅ `test_abstiene_si_la_serie_no_existe` |

### Contenido externo: el conector de edición anterior (2b, DEC-034)

`infrastructure/ine/edicion_anterior.py` descarga el anexo XLSX y la nota HTML
de una edición anterior del INE. Mismas reglas que el conector Tempus, y las
propias de un fichero binario:

- **Allowlist**: solo `https://www.ine.es/`, dos rutas fijas derivadas del
  código de la nota; el código se valida contra un patrón estricto antes de
  formar la URL; sin redirecciones.
- **Timeout y tope de bytes** en cada descarga (`http_timeout_s`,
  `http_max_bytes`).
- **Agente identificado** (DEC-018); 401/403/406/418/429 cierran el caso
  (DEC-021), sin reintento ni disfraz.
- **El XLSX se valida por bytes mágicos** (`PK\x03\x04`), no por extensión ni
  MIME, y se abre con `openpyxl` en modo `data_only` y `read_only` desde
  memoria: no se escribe en disco, no se evalúan fórmulas ni macros. Un fichero
  que no sea ZIP se rechaza con `EXTRACTION_FAILED`.
- **El HTML solo se lee con una expresión regular fija** para la fecha de
  publicación; no se interpreta ni se ejecuta nada.
- **Todo lo descargado es dato.** Si no hay anexo, fila o número, el conector
  devuelve `None` y el dominio abstiene: nunca rellena.
- **Mapa cerrado**: el conector solo actúa sobre 8 operaciones declaradas; una
  operación fuera del mapa no dispara ninguna descarga.

### Privilegios

| Control | Dónde | Verificado |
|---|---|---|
| API y web corren como usuario no-root (uid 10001 / `node`) | ambos `Dockerfile` | ✅ |
| `no-new-privileges:true` en los cuatro servicios | `docker-compose.yml` | ✅ |
| Imágenes con versión fija, nunca `latest` | `docker-compose.yml` | ✅ `pg17`, `python:3.13-slim`, `node:22-alpine` |

### Base de datos

| Control | Dónde | Verificado |
|---|---|---|
| Dos usuarios: `veritai_migrator` (DDL) y `veritai_app` (solo DML) | `scripts/migrate.py`, `001_schema_veritai.sql` | ✅ ver abajo |
| `revoke all ... from public` sobre el esquema | `001_schema_veritai.sql` | ✅ |
| `alter default privileges ... revoke all from public` | `001_schema_veritai.sql` | ✅ |
| RLS como convención obligatoria + vista de cumplimiento | `002_rls_baseline.sql` | ✅ 0 filas sin RLS |
| RLS activada **y forzada** en las 5 tablas de dominio; `veritai_app` solo DML; `audit_log` solo `insert`/`select` (no se puede editar ni borrar auditoría) | `003_puerta2.sql` | ✅ `relrowsecurity` y `relforcerowsecurity` = `t` en las 5 (2026-09-25) |
| Escritura en una sola transacción con parámetros ligados; nada concatenado en SQL | `infrastructure/repositorio.py` | ✅ |
| Identificadores y literales citados por psycopg, nunca concatenados | `scripts/migrate.py` | ✅ `sql.Identifier` / `sql.Literal` |
| Nombre de rol validado contra un patrón antes de usarse | `scripts/migrate.py` | ✅ defensa en profundidad |
| Migraciones inmutables: `sha256` verificado en cada pasada | `scripts/migrate.py` | ✅ |

Prueba del mínimo privilegio:

```
$ set role veritai_app; create table veritai.x(id int);
ERROR:  permission denied for schema veritai
```

### Secretos

| Control | Dónde | Verificado |
|---|---|---|
| `.env` en `.gitignore`, **antes** del primer commit | `.gitignore` | ✅ `git check-ignore -v .env` |
| `.env.example` versionado, solo con marcadores | `.env.example` | ✅ |
| Contraseñas generadas al azar, 32 caracteres alfanuméricos | `scripts/init-env.*` | ✅ |
| `DATABASE_URL` es `SecretStr`: no aparece en `repr()` ni en logs | `veritai/config.py` | ✅ test `test_la_url_de_base_de_datos_no_se_filtra_en_repr` |
| El runner de migraciones oculta la contraseña al registrar la conexión | `scripts/migrate.py` | ✅ log: `veritai_migrator:***@db:5432` |
| Ninguna contraseña real en el repositorio | — | ✅ `git grep` de la contraseña generada: vacío |

**Detalle no obvio:** `init-env` escribe el `.env` con fin de línea **LF** de
forma explícita. Con CRLF, Docker Compose se lleva el `\r` final dentro del valor
y produce una contraseña inválida con un error de autenticación que no dice cuál
es la causa. Lo mismo hace `.gitattributes` con los `.sh`, que si llegan con CRLF
fallan dentro del contenedor con `bad interpreter`.

### Frontend

| Control | Dónde | Verificado |
|---|---|---|
| Todo lo que entra al DOM pasa por `escapar()` con `textContent` | `apps/web/src/main.ts` | ✅ |
| Timeout de 4 s con `AbortController` en cada `fetch` | `apps/web/src/main.ts` | ✅ |
| Código fuente montado como **solo lectura** en el contenedor | `docker-compose.override.yml` | ✅ `:ro` |

### Dependencias

| Control | Dónde | Verificado |
|---|---|---|
| Rangos con tope superior de versión mayor | `requirements.txt` | ✅ |
| Pins exactos resueltos en la imagen | `requirements.lock.txt` | ✅ 29 líneas |
| Lockfile del frontend | `package-lock.json` | ✅ 66 paquetes |

---

## NO implementado todavía

Se lista como pendiente, no como hecho. Aplica **desde la primera línea de código
que toque internet** (adenda, D6).

```
RED
  [hecho, solo INE]  allowlist de un host: sustituye al bloqueo de rangos privados
                     mientras el unico destino sea servicios.ine.es
  [pendiente]        bloqueo de localhost, rangos privados y metadata para
                     cualquier fetch generico (HTML, PDF): no existe ese fetch
  [hecho]            redirecciones: no se siguen
  [hecho]            limite de descarga y timeout en el backend
  [pendiente]        rate limiting hacia el INE y hacia la API
  [hecho / pendiente] user-agent identificable si; robots.txt no se consulta
                     (la API Tempus es un servicio, no una pagina)

ENTRADA
  [parcial]          limites por campo en POST /analisis (pydantic); falta un
                     tope global de cuerpo en el servidor
  [pendiente]        limite de tiempo por peticion en la API (el del cliente INE si)
  [n/a hoy]          validacion de URLs: la API no acepta URLs
  [n/a hoy]          extension y MIME: no se descargan archivos

ARCHIVOS             [n/a hoy] no hay parsers de PDF ni ZIP

IA                   [n/a hoy] no hay LLM. Cuando lo haya: SYSTEM / TOOLS / USER /
                     UNTRUSTED separados; contenido recuperado etiquetado como no
                     confiable; validadores deterministas antes del veredicto
                     (el test 2a y los hard gates ya son esos validadores)

TESTS DE SEGURIDAD
  [hecho]            allowlist, rechazo del publicador, tope de bytes, JSON roto
  [pendiente]        SSRF generico, path traversal, prompt injection
```

Lo marcado `n/a hoy` deja de serlo con el primer fetch genérico, el primer
parser de archivos o el primer LLM. **Se implementa antes, no después.**

---

## Decisiones de seguridad con su porqué

**RLS desde la primera migración, con cero tablas.** En Supabase, PostgREST
expone las tablas con la `anon key`, que es pública por diseño: viaja en el
JavaScript del navegador. Una tabla sin RLS queda legible desde internet. Es la
fuga más frecuente en proyectos Supabase y siempre por la misma causa: la tabla
se creó antes de acordarse de RLS. Cuesta una línea hoy; después es auditar
tablas con datos dentro. Ver DEC-004.

**Dos usuarios de base de datos.** Una inyección SQL que llegue al backend no
puede crear ni borrar tablas, porque el usuario de la API no tiene DDL.
Ver DEC-005.

**Puertos en `127.0.0.1`.** Ver DEC-011.

**El contenido externo es DATA, nunca INSTRUCCIÓN.** Todavía no hay contenido
externo, pero la regla se escribe ahora porque condiciona el diseño del primer
conector, no su revisión posterior.

---

## Incidentes

### 2026-09-24 · Credenciales de Supabase en texto plano

**Qué pasó.** Las credenciales del proyecto Supabase se pegaron en texto plano en
una conversación: URL del proyecto, `publishable key` y **cadena de conexión
completa con la contraseña de la base de datos**.

**Impacto.** La contraseña da acceso total al proyecto y queda en el historial de
la conversación.

**Decisión de Mateo (2026-09-24).** Se mantienen las credenciales actuales por
ahora. La rotación queda **pendiente y explícitamente abierta**, con este umbral:

> **Rotar antes de cargar datos reales o de conectar a Supabase en serio.**

Registrado como P-09 en [`PREGUNTAS-ABIERTAS.md`](PREGUNTAS-ABIERTAS.md).
**Abierto a propósito, no olvidado.**

**Riesgo residual mientras no se rote.** El proyecto Supabase está vacío —sin
esquema, sin datos, y nada de VERITAI conectado— así que hoy no hay información que
perder. Lo que sí puede hacer quien tenga la cadena: crear objetos, consumir cuota
del plan y dejar contenido dentro. Y el umbral hay que respetarlo al pie de la
letra: el primer dato del corpus que entre es trabajo manual irrecuperable.

**Contención aplicada.** Ninguna credencial se escribió en ningún archivo del
repositorio, ni siquiera el `project-ref`. Los documentos de migración siguen con
marcadores (`RELLENAR_AL_ENLAZAR`).

**Lección.** Una credencial de base de datos no viaja por chat ni por correo. Va
directa al `.env`, que está en `.gitignore`, o a un gestor de contraseñas. Si ya
viajó, se rota — no se "tiene cuidado".
