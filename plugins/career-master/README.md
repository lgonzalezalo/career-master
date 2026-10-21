# career-master

**Revisa tu vida profesional, construye un master verificado y prepara candidaturas honestas.**
*Review your career, build a verified master profile and prepare honest applications.*

Plugin para Claude (Cowork y Claude Code) · v0.1.2 (piloto) · Español / English · MIT

---

## Para quién es

- **Personas junior** que buscan su primera oportunidad y no saben cómo contar lo que han hecho
  (estudios, prácticas, proyectos, voluntariado).
- **Profesionales que vuelven al mercado** tras una pausa larga o muchos años en la misma empresa.
- **Profesionales en activo** que buscan el siguiente paso o un cambio de sector.

## Qué hace

1. **Tu master**: una entrevista guiada, en sesiones cortas, que recorre tu trayectoria y
   convierte tus logros en hechos verificados que puedes defender en una entrevista. Es un
   ejercicio de introspección: al final tendrás tu línea temporal, tus logros con evidencia y una
   reflexión privada sobre qué te motiva y qué buscas.
2. **Tu matriz de skills**: qué puedes afirmar con honestidad de cada habilidad, qué equivalentes
   tienes y cuáles son tus huecos reales.
3. **Tus historias STAR** (Situación, Tarea, Acción, Resultado): un banco de historias para
   entrevistas, con modo práctica.
4. **Cada oferta**: puntuación de encaje, CV adaptado en PDF, carta de presentación, respuestas
   a formularios, preparación de entrevista y un registro de candidaturas.

Regla de oro: **nada entra en un documento si tú no lo has confirmado**. El sistema frena las
exageraciones y también te ayuda a no infravalorarte.

## Cómo empezar

1. Instala el plugin (ver el README del repositorio).
2. Crea una carpeta vacía en tu ordenador, por ejemplo `career`.
3. En Cowork: abre una tarea nueva y conecta esa carpeta. En Claude Code: abre Claude Code
   dentro de esa carpeta.
4. Escribe **«empecemos»**. Claude te hará unas pocas preguntas y creará la estructura.
5. Copia en `sources/` tus CVs antiguos, el PDF de tu perfil de LinkedIn, evaluaciones o
   certificados que tengas.
6. Di **«sigamos con el master»** cada vez que tengas 15–20 minutos.

Frases útiles: «haz mi matriz de skills» · «prepárame historias STAR» · «practiquemos la
entrevista» · «evalúa esta oferta» · «hazme el CV y la carta para esta oferta» · «actualiza mis
candidaturas» · «borra esto del master».

Si Claude no puede crear el PDF, te dejará un archivo `cv.print.html`. Ábrelo con doble clic,
pulsa Ctrl+P (Cmd+P en Mac), elige «Guardar como PDF», tamaño A4 y márgenes predeterminados.

## Privacidad

- Todo se guarda en tu carpeta, en tu ordenador. El plugin no tiene telemetría.
- Las conversaciones pasan por Claude según las condiciones de tu cuenta.
- No se guardan fecha de nacimiento, DNI, foto, nacionalidad, estado civil, dirección, salud ni
  datos de otras personas, aunque aparezcan en tus CVs antiguos. Solo si tú lo pides
  expresamente, puedes guardar contexto personal en tu reflexión privada o en la nota de una
  pausa, con tus palabras.
- Tu reflexión personal es privada: nunca se usa en CVs, cartas ni respuestas.
- Nunca se te pedirá que expliques una pausa profesional, y tú decides si se menciona.
- Puedes pedir en cualquier momento «corrige esto» o «borra esto del master»: se elimina del
  master y de tus archivos de trabajo, y Claude te preguntará si también quieres borrarlo de las
  candidaturas guardadas. Lo que ya enviaste no se puede recuperar.
- Tus CVs antiguos siguen en `sources/`: bórralos cuando ya no los necesites.
- Si guardas la carpeta en la nube o en git, mantenla privada.

## Piloto: qué nos ayuda saber

Si estás probando esta versión, anota: cuánto tardaste en completar el master, dónde te
atascaste o abandonaste, qué te aportó la parte de reflexión (sin detalles personales), si el CV
final te representa y si alguna afirmación te pareció exagerada o infravalorada.

---

## English summary

career-master turns a job search into a structured career review. A guided interview builds a
**master profile** of verified achievements (with provenance, status and usage rules), a
**skills matrix** with honest levels and equivalents, and a **STAR story bank**. From there it
scores job offers, tailors CVs, cover letters and answers, and tracks applications. Nothing goes
into a document unless you confirmed it; your private reflection is never used in CVs, letters
or answers; conversations are processed by Claude under your account's terms; you can ask at
any time to correct or delete something. Start by creating an empty folder, opening
it in Cowork (connected folder) or Claude Code, and saying "let's start".

Skills: `career-start` · `master-builder` · `skills-matrix` · `star-coach` · `job-tailor`.
Fictional example masters (junior and returning) are in `skills/master-builder/examples/`.

PDF output needs Playwright/Chromium where Claude runs (pandoc is used if present); otherwise you
get a `cv.print.html` file to print to PDF from your browser.
