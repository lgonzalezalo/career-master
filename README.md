# career-master

**Revisa tu vida profesional, construye un master verificado y prepara candidaturas honestas.**
*Review your career, build a verified master profile and prepare honest applications.*

Plugin para Claude (Cowork y Claude Code) · v0.1.0 (piloto) · Español / English · [MIT](LICENSE)

---

## Qué es

career-master convierte la búsqueda de empleo en una revisión estructurada de tu trayectoria.
Una entrevista guiada, en sesiones cortas, construye:

1. **Tu master**: tus estudios, puestos y logros convertidos en hechos verificados que puedes
   defender en una entrevista, más una reflexión privada sobre qué te motiva y qué buscas.
2. **Tu matriz de skills**: qué puedes afirmar de cada habilidad, qué equivalentes tienes y
   cuáles son tus huecos reales.
3. **Tus historias STAR** (Situación, Tarea, Acción, Resultado): un banco de historias para
   entrevistas, con modo práctica.
4. **Cada candidatura**: puntuación de encaje con la oferta, CV en PDF, carta, respuestas y un
   registro de candidaturas.

Regla de oro: **nada entra en un documento si tú no lo has confirmado**.

Pensado para personas **junior** que buscan su primera oportunidad, profesionales que **vuelven
al mercado** tras años fuera del mercado laboral o muchos años en la misma empresa, y
profesionales en activo o en **cambio de sector**.

## Requisitos

- La app de escritorio de Claude con Cowork (disponible en planes de pago), o Claude Code.
- Una carpeta vacía en tu ordenador donde se guardará todo.

## Instalación

### Cowork (app de escritorio de Claude)

1. Descarga `career-master.plugin` desde la página de
   [Releases](https://github.com/lgonzalezalo/career-master/releases/latest).
2. En la app de Claude, abre la sección de plugins de Cowork y añade el archivo descargado.
3. Crea una carpeta vacía (por ejemplo `career`), abre una tarea nueva de Cowork, conecta esa
   carpeta y escribe **«empecemos»**.

### Claude Code

Abre Claude Code (`claude` en la Terminal) y escribe:

```
/plugin marketplace add lgonzalezalo/career-master
/plugin install career-master@career-master
```

Después crea una carpeta vacía (por ejemplo `career`), abre Claude Code dentro de ella
(`cd career` y luego `claude`) y escribe **«empecemos»**. Si Claude Code te pide reiniciar tras
instalar, hazlo.

## Uso

| Quiero…                         | Escribe                                        |
|---------------------------------|------------------------------------------------|
| Empezar                         | «empecemos»                                    |
| Seguir con mi master            | «sigamos con el master»                        |
| Mi matriz de skills             | «haz mi matriz de skills»                      |
| Historias para entrevistas      | «prepárame historias STAR»                     |
| Practicar una entrevista        | «practiquemos la entrevista»                   |
| Evaluar una oferta              | pega la oferta + «evalúa esta oferta»          |
| CV y carta                      | «hazme el CV y la carta para esta oferta»      |
| Actualizar candidaturas         | «actualiza mis candidaturas» / «me han llamado de…» |
| Corregir o borrar algo          | «corrige esto» / «borra esto del master»       |

Si Claude no puede crear el PDF, te dejará un archivo `cv.print.html`. Ábrelo con doble clic,
pulsa Ctrl+P (Cmd+P en Mac), elige «Guardar como PDF», tamaño A4 y márgenes predeterminados.

Más detalle en el [README del plugin](plugins/career-master/README.md). Hay dos masters de
ejemplo ficticios en
[`examples/`](plugins/career-master/skills/master-builder/examples/).

## Privacidad

- Tus datos se guardan en tu carpeta, en tu ordenador. El plugin no tiene telemetría.
- Las conversaciones pasan por Claude según las condiciones de tu cuenta.
- No se guardan fecha de nacimiento, DNI, foto, nacionalidad, estado civil, dirección, salud ni
  datos de otras personas, aunque aparezcan en tus CVs antiguos, salvo que tú pidas
  expresamente guardar contexto personal en tu reflexión privada o en la nota de una pausa.
- Tu reflexión personal es privada y nunca aparece en CVs, cartas ni respuestas.
- Puedes pedir «corrige esto» o «borra esto del master» en cualquier momento.
- Tus CVs antiguos siguen en `sources/` tal cual: bórralos cuando ya no los necesites.
- Nunca subas tu carpeta de datos a un repositorio público; si haces un fork, guárdala fuera.

## Feedback

Estamos en fase piloto. Cuéntanos cómo te ha ido abriendo un
[issue de feedback](https://github.com/lgonzalezalo/career-master/issues/new?template=feedback.md).
Los issues son públicos: no incluyas datos personales.

## Para mantenedores

### Comprobaciones automáticas

Se ejecutan en GitHub Actions en cada push. En local:

```bash
pip install pyyaml pypdf markdown playwright && python -m playwright install chromium
python tools/check.py
```

### Publicar una versión

1. Sube la versión en `plugins/career-master/.claude-plugin/plugin.json`,
   `.claude-plugin/marketplace.json` y `CHANGELOG.md`, y ejecuta `python tools/check.py`.
2. Genera el `.plugin` desde cero:

   ```bash
   rm -f career-master.plugin
   (cd plugins/career-master && zip -r ../../career-master.plugin . -x "*.DS_Store" "*/__pycache__/*")
   ```

3. Crea una release en GitHub con el tag `vX.Y.Z` y adjunta `career-master.plugin` (el archivo
   no se guarda en el repositorio).
4. La primera vez, crea las etiquetas `feedback` y `bug` en Issues → Labels.

## Estructura del repositorio

```
.claude-plugin/marketplace.json   # catálogo para instalar desde Claude Code
.github/                          # plantillas de issues y comprobaciones (CI)
tools/check.py                    # comprobaciones automáticas
plugins/career-master/            # el plugin
  ├── .claude-plugin/plugin.json
  ├── skills/                     # career-start, master-builder, skills-matrix, star-coach, job-tailor
  └── README.md
```

---

## English

career-master turns a job search into a structured career review. A guided interview builds a
**verified master profile** (achievements with provenance, status and usage rules), a **skills
matrix** with honest levels and equivalents, and a **STAR story bank**. It then scores job
offers, tailors CVs, cover letters and answers, and tracks applications. Nothing goes into a
document unless you confirmed it.

Privacy: your data stays in your folder; conversations are processed by Claude under your
account's terms. Date of birth, ID numbers, photos, nationality, family status, address, health
and other people's data are never stored, even if old CVs contain them (unless you explicitly ask
to keep personal context in your private reflection or a break note). Your private reflection is
never used in CVs, letters or answers. Say "correct this" or "delete this from my master" at any
time.

Requirements: the Claude desktop app with Cowork (paid plans) or Claude Code, and an empty
folder. Install: download `career-master.plugin` from
[Releases](https://github.com/lgonzalezalo/career-master/releases/latest) and add it in Cowork's
plugin section, or in Claude Code run `/plugin marketplace add lgonzalezalo/career-master` and
`/plugin install career-master@career-master`. Then open the empty folder (connected folder in
Cowork, working directory in Claude Code) and say "let's start".

Feedback welcome through [issues](https://github.com/lgonzalezalo/career-master/issues/new?template=feedback.md)
(public — no personal data). MIT licensed.

Built by [Luis González Alonso](https://lgonzalezalo.github.io).
