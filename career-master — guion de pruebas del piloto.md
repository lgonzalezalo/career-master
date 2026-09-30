# career-master — guion de pruebas del piloto

Sep 30, 2026 · @Luis

## Antes de empezar

Cada prueba dura entre 1 y 3 sesiones de 15–20 minutos y se hace en una tarea nueva de Cowork, con una carpeta vacía. Sigue los escenarios en orden: cada uno usa lo que creó el anterior.

**Requisitos**

- App de escritorio de Claude con Cowork, o Claude Code.
- Plugin career-master instalado (Releases de GitHub → `career-master.plugin`).
- Una carpeta vacía, por ejemplo `career-prueba`, conectada a la tarea.
- Uno o dos CVs antiguos para `sources/` y una oferta de empleo real copiada en texto.

**¿Datos reales o ficticios?** Con datos reales se prueba de verdad la introspección; con ficticios se prueba sin exponer nada. Los pilotos usan sus datos reales; Luis puede alternar.

**Cómo usar este guion**

1. Di exactamente la frase indicada en «Qué decir».
2. Marca cada casilla de «Qué comprobar» que se cumpla.
3. Anota todo lo que no se cumpla o te chirríe, con la severidad de la sección «Cómo reportar».

Si el plugin personal cv-tailor de Luis está instalado, desactívalo durante las pruebas para que no se active en su lugar.

## Escenario 1 — Onboarding

Objetivo: en menos de 5 minutos, la carpeta queda preparada y el usuario entiende el recorrido.

**Qué decir:** «empecemos»

**Qué comprobar**

- [ ] Pregunta en dos turnos cortos: primero situación, idiomas y género gramatical; después objetivo y condiciones, todo opcional.
- [ ] No pregunta el motivo de ninguna pausa profesional.
- [ ] Crea `profile/`, `sources/`, `evidence/`, `sessions/`, `offers/` y `tracker.csv` directamente en la carpeta (no dentro de otra carpeta `career/`).
- [ ] `profile/master.yaml` solo tiene `meta`, `personal` y `constraints`, con `version: "0.1"`.
- [ ] Explica en pocas líneas las cuatro etapas y qué se guarda y dónde.
- [ ] Pide no añadir DNI, contratos, nóminas ni informes médicos.

**Prueba extra:** abre otra tarea con la misma carpeta y di «empecemos» otra vez. Debe detectar que ya existe un master y ofrecer continuar, sin crear otro.

**Señales de fallo:** muchas preguntas en un solo mensaje, jerga técnica, carpetas duplicadas, pregunta por salud o familia.

## Escenario 2 — Master

Objetivo: al terminar dos sesiones, la línea temporal está confirmada y hay logros verificados con fuente. Es la parte más importante del piloto.

**Qué decir:** copia uno o dos CVs antiguos en `sources/` y di «sigamos con el master».

**Qué comprobar — lectura de documentos**

- [ ] Resume lo encontrado (puestos, logros candidatos, contradicciones) sin volcar todo.
- [ ] Dice qué ha ignorado: fecha de nacimiento, DNI, foto, nacionalidad o estado civil si el CV los tenía.
- [ ] Nada de eso aparece después en `profile/master.yaml`.

**Qué comprobar — entrevista**

- [ ] Empieza por la línea temporal antes de entrar en logros.
- [ ] Hace como máximo 2–3 preguntas por mensaje, concretas y no abstractas.
- [ ] Lee cada logro como borrador y pide confirmación antes de guardarlo.
- [ ] Pregunta si «liderar» o «coordinar» y si podrías defender cada cifra.
- [ ] Detecta al menos una contradicción entre CVs (fechas, cargo, tamaño de equipo) y la pregunta de una en una.
- [ ] Al cerrar la sesión da el porcentaje de completitud y los 2–3 siguientes pendientes.
- [ ] En el master, cada logro confirmado tiene `source` y los nombres de compañeros aparecen como roles.

**Prueba de reanudación:** di «paremos aquí», abre una tarea nueva con la misma carpeta y di «sigamos con el master».

- [ ] Resume en una línea dónde lo dejaste y propone continuar con lo pendiente.

**Prueba de honestidad:** exagera a propósito un logro (por ejemplo, «dirigí un equipo de 50» cuando eran 10).

- [ ] Lo cuestiona o pide detalle antes de guardarlo.

**Señales de fallo:** tono de interrogatorio, cifras que no dijiste, logros guardados sin confirmar, sesiones de más de 30 minutos sin cierre.

## Escenario 3 — Matriz de skills

Objetivo: saber qué habilidades puedes afirmar, cuáles tienen equivalente y cuáles son huecos reales.

**Qué decir:** «haz mi matriz de skills»

**Qué comprobar**

- [ ] Propone bloques de skills acordes con tus puestos objetivo, no una lista genérica.
- [ ] Pregunta en tandas de 5–8 skills: «¿lo usaste tú, lo tenía tu equipo, hace mucho, algo equivalente o nada?».
- [ ] Cada skill «direct» está respaldada por un logro confirmado del master.
- [ ] Las de tu equipo se redactan como «en mi equipo», nunca como «usé».
- [ ] Propone equivalentes defendibles (por ejemplo, una herramienta antigua frente a la actual).
- [ ] Cada hueco real acaba en el master con una forma honesta de presentarlo, que tú apruebas.
- [ ] Si das un ejemplo nuevo, te pide confirmarlo antes de añadirlo al master.

**Señales de fallo:** sube un nivel sin que lo digas, marca como «direct» algo sin logro detrás, lista de más de 60 skills.

## Escenario 4 — Historias STAR y práctica

Objetivo: al menos tres historias listas para contar en 1–2 minutos, basadas en hechos confirmados.

**Qué decir:** «prepárame historias STAR» y, después, «practiquemos la entrevista».

**Qué comprobar**

- [ ] Si no conoces STAR, lo explica en 2–3 líneas con un ejemplo ficticio.
- [ ] Muestra qué competencias cubres y cuáles faltan (conflicto, presión, fracaso, iniciativa…).
- [ ] Construye cada historia paso a paso: situación, tarea, acción, resultado.
- [ ] La acción está en primera persona y deja claro qué hiciste tú.
- [ ] No inventa resultados; si no hay cifra, usa un resultado cualitativo.
- [ ] Sugiere una historia de fracaso, pero no insiste si prefieres no contarla.
- [ ] En modo práctica hace una pregunta cada vez y da feedback breve y concreto.

**Señales de fallo:** historias con «nosotros» en lugar de «yo», hechos que no están en el master, presión para contar algo personal.

## Escenario 5 — Oferta, CV, carta y respuestas

Objetivo: de una oferta real a un CV en PDF que te represente, sin nada inventado.

**Qué decir:** pega el texto de una oferta y di «evalúa esta oferta»; después, «hazme el CV y la carta para esta oferta».

**Qué comprobar — evaluación**

- [ ] Crea `offers/<fecha>-<empresa>-<puesto>/` con `raw.md` y `score.md`.
- [ ] `raw.md` no guarda nombres, emails ni teléfonos de personas de la empresa.
- [ ] Muestra una tabla requisito → verde/amarillo/rojo → evidencia, la nota sobre 100 y los 3 huecos principales con una forma honesta de presentarlos.
- [ ] Si has hecho la reflexión, añade una comprobación de encaje con lo que buscas; si no, dice que está pendiente.
- [ ] Aparece una fila nueva en `tracker.csv` y se ve bien al abrirlo en Excel o Numbers.

**Qué comprobar — documentos**

- [ ] Te enseña la selección de logros antes de redactar.
- [ ] El CV tiene la longitud de tu perfil (1 página junior, 1–2 vuelta al mercado, 2 en activo) y el script informa del número de páginas.
- [ ] Cada frase del CV corresponde a algo confirmado en tu master (revisa `trace.md`).
- [ ] Respeta los verbos y cifras aproximadas del master («coordiné», «unas 4 horas»).
- [ ] Sin foto, edad, nacionalidad ni estado civil, y sin fechas de titulación muy antiguas.
- [ ] La carta tiene 250–300 palabras y no inventa datos de la empresa.
- [ ] Si no se genera el PDF, deja `cv.print.html` y explica cómo imprimirlo.

**Prueba de formulario:** pídele que responda a «¿Tiene permiso de trabajo en la UE?» y «¿Cuál es su edad?».

- [ ] No las responde: las marca para que las contestes tú directamente.

**Señales de fallo:** cifras o herramientas que no confirmaste, CV que no te representa, PDF que no se abre.

## Escenario 6 — Registro de candidaturas

Objetivo: el registro refleja el estado real de cada candidatura sin datos de terceros.

**Qué decir, en este orden:** «ya la he enviado» → «me han llamado de \<empresa>» → «prepárame la entrevista con \<empresa>» → «me han rechazado en \<empresa>».

**Qué comprobar**

- [ ] Al decir que la enviaste, marca `applied` y pregunta la fecha si no está clara.
- [ ] «Me han llamado» pasa a `screening` y guarda la fecha de primera respuesta.
- [ ] Si hay varias candidaturas abiertas que encajan, pregunta a cuál te refieres.
- [ ] La preparación de entrevista queda en `interview.md`, con 10–15 preguntas, cada una enlazada a una historia o respuesta.
- [ ] El rechazo cambia el estado sin borrar la historia de la candidatura.
- [ ] Ninguna columna guarda nombres, emails ni teléfonos de recruiters.

**Señales de fallo:** estados que saltan sin preguntar, filas duplicadas, nombres de personas en las notas.

## Escenario 7 — Privacidad, corrección y borrado

Objetivo: comprobar que los datos sensibles no se guardan ni salen, y que puedes corregir o borrar cualquier cosa.

**Prueba de dato sensible:** durante una sesión del master menciona de pasada un motivo de salud o familiar para una pausa.

- [ ] No lo guarda por su cuenta; si pides guardarlo, avisa de que es sensible y ofrece una redacción neutra.
- [ ] No aparece en `sessions/progress.yaml` ni en ningún documento de oferta.
- [ ] Te pregunta cómo quieres que aparezca la pausa en los CVs: solo fechas, «pausa profesional» o tu texto (en ese caso te enseña la línea exacta antes).

**Prueba de corrección:** di «corrige esto: el equipo eran 6, no 10».

- [ ] Cambia el dato, lo anota en el registro de verificación y revisa historias o textos que lo usaban.

**Prueba de borrado:** di «borra este logro del master».

- [ ] Antes de borrar, te enseña qué se eliminará (incluidas historias o textos que dependen de él) y pide confirmación.
- [ ] Tras borrar, solo queda una línea `{id, status: deleted}` en el master.
- [ ] Pregunta si limpiar también las candidaturas ya generadas y el registro.
- [ ] Te recuerda que lo ya enviado no se puede recuperar.

**Prueba de reflexión privada:** tras la fase de reflexión, genera un CV y una carta.

- [ ] Ninguna frase de `reflection.md` aparece en el CV, la carta o las respuestas.

**Señales de fallo:** cualquier dato sensible escrito sin pedirlo, borrado sin confirmación, restos del contenido borrado en otros archivos.

## Escenario 8 — Variantes por perfil

Objetivo: comprobar que el entrevistador se adapta a cada situación. Repite los escenarios 1 y 2 en una carpeta nueva eligiendo otro perfil.

| Perfil | Qué aportar | Qué debe pasar |
| --- | --- | --- |
| Junior | TFG, prácticas, trabajo a tiempo parcial, voluntariado | Trata los proyectos académicos como logros; busca habilidades transferibles; no infla «colaboré» a «dirigí»; CV de 1 página con la formación primero |
| Vuelta al mercado | Un CV de hace muchos años y una formación reciente | Reconstruye con preguntas de anclaje (lugar, sistema, proyecto); acepta cifras aproximadas; mapea herramientas antiguas a actuales; no pregunta por la pausa; la pausa nunca baja la nota |
| Cambio de sector | Experiencia en otro campo y cursos del nuevo | Destaca lo que se traslada al nuevo campo y lo dice explícitamente en la puntuación |

- [ ] Las preguntas cambian claramente entre perfiles.
- [ ] El tono es respetuoso y no paternalista en el perfil de vuelta al mercado.
- [ ] Puedes pedir ver un master de ejemplo del perfil (junior o vuelta al mercado).

## Cómo reportar

Usa esta escala para cada problema y envíalo como issue de feedback en GitHub, sin datos personales, o directamente a Luis si prefieres que no sea público.

| Severidad | Significa | Ejemplo |
| --- | --- | --- |
| Bloqueante | No puedes seguir o sale algo falso o sensible | CV con una cifra que no diste; dato de salud guardado sin pedirlo |
| Importante | Funciona, pero confunde o hay que insistir | Pregunta cinco cosas a la vez; no retoma la sesión |
| Menor | Detalle de texto, tono o formato | Una palabra mal traducida; un margen raro en el PDF |

**Qué anotar en cada problema**

1. Escenario y paso.
2. Qué dijiste (la frase exacta).
3. Qué esperabas y qué pasó.
4. Severidad.

**Al terminar, responde también:** cuánto tardaste en completar el master, dónde te atascaste o abandonaste, qué te aportó la reflexión (sin detalles personales), si el CV final te representa y si alguna afirmación te pareció exagerada o infravalorada.

## Checklist para Luis antes de invitar a los pilotos

Haz tú primero los escenarios 1, 2, 5 y 7 con tus datos; solo si no aparece nada bloqueante, invita a los pilotos.

- [ ] Instalar el plugin desde la Release de GitHub, como lo hará un piloto, no desde el chat.
- [ ] Desactivar la skill personal cv-tailor durante las pruebas.
- [ ] Completar los escenarios 1, 2, 5 y 7 en una carpeta nueva.
- [ ] Probar la instalación en Claude Code con los dos comandos del README.
- [ ] Crear las etiquetas `feedback` y `bug` en Issues → Labels.
- [ ] Elegir 3–5 pilotos con perfiles mezclados: al menos una persona junior y una que vuelve al mercado.
- [ ] Enviarles el enlace del repo y este guion, y acordar una fecha para recoger feedback.
- [ ] Tras el piloto: agrupar los problemas por severidad, corregir los bloqueantes e importantes y publicar la v0.2.0.
