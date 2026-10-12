# IA al Día | Observatorio educativo de Inteligencia Artificial

Sitio Jekyll y agente editorial automático para publicar un consolidado semanal de noticias de inteligencia artificial con enfoque educativo. Forma parte del ecosistema **Arias-Data-Lab**.

## Qué hace

- Ejecuta una búsqueda web semanal sobre noticias de IA.
- Prioriza hechos recientes, fuentes confiables y temas con impacto social o educativo.
- Genera una entrada Markdown con noticias, contexto, riesgos, oportunidades y preguntas para el aula.
- Guarda un historial para reducir noticias repetidas.
- Publica el sitio con GitHub Pages mediante GitHub Actions.

## Configuración necesaria

1. **Nombre del repositorio.** Para que el sitio principal de la cuenta `ljarias` quede en `https://ljarias.github.io/`, renombra este repositorio exactamente a `ljarias.github.io`. Mientras conserve el nombre actual, GitHub Pages lo tratará como un sitio de proyecto.
2. En **Settings → Secrets and variables → Actions**, crea el secreto `OPENAI_API_KEY` con una clave de la API de OpenAI. No publiques la clave en ningún archivo.
3. En **Settings → Pages → Build and deployment**, selecciona **GitHub Actions** como fuente.
4. Abre la pestaña **Actions**, entra en el workflow **Publicar IA al Día** y usa **Run workflow** para ejecutar una primera edición manual.
5. Después, el workflow está programado para ejecutarse los **domingos a las 8:00 a. m. (America/Bogota)**.

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

## Identidad visual Arias-Data-Lab v4.0

La portada, la plantilla de artículos y el pie de página comparten el logotipo oficial aprobado, el lema **«Tecnología con criterio humano.»** y la paleta corporativa (azul `#102A43`, turquesa `#087F8C`, celeste `#D7F1F5`, amarillo `#F4B942`, blanco hielo `#F6F9FC` y gris `#475569`).

- CSS complementario: `assets/css/adl-ia-al-dia.css` (se carga tras los estilos originales).
- Logo principal: SVG multicolor aprobado en `assets/brand/logo/v4.0/ADL_logo-maestro-color_EDITABLE_v4.0.svg`, con 25 trazados y 13 degradados; isotipo cuadrado oficial en el mismo directorio.
- Favicon SVG en los navegadores compatibles, con PNG de 32 px en `banco-problemas-caribe/assets/` como respaldo.
- La migración está aplicada a la plantilla Jekyll de IA al Día, al portal Arias-Data-Lab y a las cuatro páginas del Banco de Problemas. El resto del contenido histórico permanece sin cambios.
- El logotipo no se modifica ni redibuja; las infografías históricas tampoco se alteran.
- La automatización semanal `.github/workflows/publicar.yml` y la generación editorial permanecen sin cambios.
