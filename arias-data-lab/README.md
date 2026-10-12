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
