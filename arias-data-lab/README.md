# Portal corporativo Arias-Data-Lab

**Fase 7 · versión 1.0 · 12 de octubre de 2026**

Sitio: https://ljarias.github.io/arias-data-lab/

## Arquitectura y publicación

- `/arias-data-lab/index.html` contiene la presentación corporativa: áreas de trabajo, portafolio, metodología, perfil y contacto.
- `/arias-data-lab/portal.css` define la presentación mobile-first sin dependencias de JavaScript.
- Se usan los tokens centralizados en `/assets/brand/adl-tokens.css`.
- **Logotipo original:** se carga sin modificaciones desde `/banco-problemas-caribe/assets/logo-adl-v3.webp`. El favicon se carga desde el isotipo aprobado.
- IA al Día sigue en `/` con sus noticias, publicaciones y automatización intactas; el Banco de Problemas sigue en `/banco-problemas-caribe/`.
- La plantilla Jekyll `/_layouts/default.html` y `/acerca.md` enlazan a este portal.

## Contenido verificable

- IA al Día y Banco de Problemas tienen páginas públicas dentro del mismo sitio.
- Otros cuatro proyectos se enlazan a repositorios públicos del perfil `github.com/ljarias`: Tablero ICFES INEM, Acceso Escolar INEM, Red Piezométrica y Préstamos SaaS.
- La sección de perfil enlaza a la presentación académica y profesional publicada en el Banco de Problemas.
- Contacto: correo ya publicado previamente en la sección Acerca de de IA al Día.

## Identidad y accesibilidad

Conservar el nombre **Arias-Data-Lab** y el lema **Tecnología con criterio humano**. No redibujar ni reemplazar el logotipo. Las imágenes incluyen atributo `alt`, los enlaces nuevos que abren pestaña incorporan `rel="noopener noreferrer"`, la navegación dispone de un salto directo al contenido y las animaciones respetan `prefers-reduced-motion`.

## Validación

Revisar rutas, anclas, contraste y adaptación a 360, 768 y 1280 px tras la publicación. La inspección estática del HTML/CSS no constituye una auditoría integral WCAG ni una prueba real de navegador.

## Reversión

Esta versión introduce archivos independientes y dos ajustes de enlaces. Puede revertirse mediante el pull request de esta fase sin afectar las publicaciones históricas de IA al Día ni los datos del Banco de Problemas.


## Enriquecimiento de perfil y trayectoria — 12/10/2026

Fuente primaria declarativa: [LinkedIn de Leonardo Arias-Alemán](https://www.linkedin.com/in/ljarias), versión pública indexada. El acceso directo a LinkedIn puede estar restringido y algunos empleos/fechas aparecen ocultos; no se reconstruyeron.

Se añadieron únicamente:
- Más de dos décadas de experiencia profesional (el extracto público dice 24 años).
- Participación registrada en **Caribbean Marine Atlas – Phase 2** (proyecto fechado desde 2016); sin inventar título laboral, periodo de contrato ni responsabilidad técnica específica.
- Mentoría en **Colombia Programa / nodo 268** (2024).
- Formación pedagógica de **480 horas** en Universidad del Magdalena (2024).
- Voluntariado ambiental en limpieza de playas con **Club de Buceo Narvales** (1994–2000).

Se mantiene explícitamente **maestría en curso** y no se afirma obtención del título. Otros empleos de LinkedIn no se incorporaron al no estar visibles sus cargos. La relación con Universidad Cooperativa de Colombia y Universidad del Magdalena ya estaba publicada en el perfil anterior.

Cambios de presentación: nueva sección de trayectoria en el portal, ampliación del dossier profesional en el Banco de Problemas y enlace al perfil público. Se preservan logotipo, recursos, navegación a los seis proyectos y automatización de IA al Día.

Nota de mantenimiento: confirmar en LinkedIn cargos, periodos, responsabilidades y afiliaciones cuando se disponga de una exportación auténtica del perfil, antes de ampliar la cronología.
