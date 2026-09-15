# IA al Día | Observatorio educativo de Inteligencia Artificial

Sitio y agente editorial automático para publicar un resumen diario de noticias de inteligencia artificial con enfoque educativo.

## Qué hace

- Ejecuta una búsqueda web diaria sobre noticias de IA.
- Prioriza hechos recientes, fuentes confiables y temas con impacto social o educativo.
- Genera una entrada en Markdown con 5 a 7 noticias, contexto, riesgos, oportunidades y preguntas para el aula.
- Guarda un historial para reducir noticias repetidas.
- Publica el sitio con GitHub Pages mediante GitHub Actions.

## Configuración necesaria

1. **Nombre del repositorio.** Para que el sitio principal de la cuenta `ljarias` quede en `https://ljarias.github.io/`, renombra este repositorio exactamente a `ljarias.github.io`. Mientras conserve el nombre actual, GitHub Pages lo tratará como un sitio de proyecto.
2. En **Settings → Secrets and variables → Actions**, crea el secreto `OPENAI_API_KEY` con una clave de la API de OpenAI. No publiques la clave en ningún archivo.
3. En **Settings → Pages → Build and deployment**, selecciona **GitHub Actions** como fuente.
4. Abre la pestaña **Actions**, entra en el workflow **Publicar IA al Día** y usa **Run workflow** para ejecutar una primera edición manual.
5. Después, el workflow se ejecutará diariamente a las **7:15 a. m. (America/Bogota)**.

## Estructura

```text
.github/workflows/publicar.yml   Automatización diaria y despliegue
scripts/generar_resumen.py       Agente editorial
prompts/editor_ia.md             Criterios editoriales
data/historial.json              Control básico de duplicados
_posts/                          Resúmenes diarios
_layouts/                        Plantillas del sitio
assets/css/style.css              Diseño visual
index.md                         Portada
acerca.md                        Acerca del proyecto
```

## Criterio editorial

El sitio diferencia entre hechos, declaraciones, estudios, proyecciones y controversias. No intenta presentar predicciones sobre la IA como hechos confirmados. Cada publicación debe incluir fuentes y una sección de aplicación educativa.

## Costos

GitHub Pages y GitHub Actions pueden operar sin costo en este repositorio público dentro de los límites de GitHub. El uso de la API de OpenAI y de búsqueda web genera costos según el modelo y las herramientas utilizadas.

## Seguridad

Nunca agregues `OPENAI_API_KEY` al repositorio. Debe existir únicamente como secreto de GitHub Actions.
