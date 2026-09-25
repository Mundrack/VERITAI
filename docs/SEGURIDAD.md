# Seguridad

> Este documento lista los controles **ya implementados y verificados**, no los
> planeados. Lo que falta está en su propia sección, dicho como falta.
>
> Las reglas completas están en `CLAUDE.md` §8 y en el START-HERE §23–25. Esto es
> el registro de qué está hecho de verdad.

**Última actualización:** 2026-09-24

---

## Estado en una línea

**Nada del sistema toca internet todavía.** Eso significa que los controles de
contenido no confiable — SSRF, prompt injection, parsing de archivos — **no
están implementados**, y no deben darse por hechos. Lo que sí está implementado
es todo el perímetro del entorno: red, privilegios, secretos y base de datos.

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
  bloqueo de localhost y rangos privados en fetches externos (SSRF)
  bloqueo de servicios de metadata
  limite de redirects, validados
  limite de descarga y timeout en el backend
  rate limiting
  user-agent identificable, robots.txt

ENTRADA
  limites de tamano de cuerpo en la API
  limites de tiempo por peticion
  validacion de URLs normalizadas
  desconfianza de extension y MIME declarados

ARCHIVOS
  parsers de PDF con minimo privilegio
  prevencion de zip-slip y zip bombs
  almacenamiento temporal aislado, nombres generados internamente

IA
  separacion estricta de SYSTEM / TOOLS / USER / UNTRUSTED CONTENT
  etiquetado del contenido recuperado como no confiable
  validadores deterministas antes de que algo afecte al veredicto

TESTS DE SEGURIDAD
  contra entradas maliciosas
  de SSRF y de path traversal
  de prompt injection
```

Ninguno de estos hace falta hoy, porque no hay ni un componente que salga a la
red. **Todos hacen falta antes del primer conector.**

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

**Acción inmediata.** Rotar la contraseña en *Project Settings → Database → Reset
database password*. Registrado como P-09 en
[`PREGUNTAS-ABIERTAS.md`](PREGUNTAS-ABIERTAS.md). **Abierto.**

**Contención aplicada.** Ninguna credencial se escribió en ningún archivo del
repositorio, ni siquiera el `project-ref`. Los documentos de migración siguen con
marcadores (`RELLENAR_AL_ENLAZAR`).

**Lección.** Una credencial de base de datos no viaja por chat ni por correo. Va
directa al `.env`, que está en `.gitignore`, o a un gestor de contraseñas. Si ya
viajó, se rota — no se "tiene cuidado".
