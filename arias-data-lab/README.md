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

## Perfil profesional ampliado (exportación de LinkedIn · 12/10/2026)

La edición se basó en un PDF de 4 páginas entregado por el titular (**no publicado en el repositorio**). Se utilizaron sus nombres de cargo, entidades, responsabilidades, herramientas y fechas. Para la página `/banco-problemas-caribe/acerca-de.html` se añadió una cronología agrupada y una hoja de estilos independiente (`assets/adl-perfil-timeline-v4.css`). La portada `/arias-data-lab/` presenta una síntesis con cuatro líneas de experiencia.

**Periodos recogidos:** CETECOS 1997–2003; INVEMAR 2000–2024; Fundación Universitaria San Martín 2005; UCC 2006–2018 y desde 2024; CORGEDAS 2015–2017; Unimag desde 2017; NaturalSIG desde 2018; Secretaría de Salud Distrital 2020–2022; INEM desde 2024. Los cargos pueden ser concurrentes y las expresiones «hasta la actualidad» corresponden a lo consignado en la exportación.

**Responsabilidades descritas:** administración de módulos SIAM; datos e indicadores para CMA2 y SPINCAM; representación ante comité técnico SIAC; apoyo en Power BI, Survey123 y ArcGIS a salud pública; docencia, mentoría y transferencia de conocimiento. Se incorporó formación en Universidad del Norte, Arcitura, MinTIC y programa pedagógico Unimag, además de idiomas y certificación de buceo publicados en el propio LinkedIn.

**Protección de datos:** no se expone número telefónico del archivo ni se sube el PDF bruto a GitHub. No se derivaron métricas de impacto o logros cuantitativos ausentes del documento. La maestría en UTB continúa descrita como **en curso** porque no figura en el PDF de LinkedIn y no debe tratarse como grado terminado.


## Productos y soluciones · presentación pública sin código (12/10/2026)

Se incorpora `/arias-data-lab/productos/` con fichas independientes para:

- `productos/prestamos-saas.html`: Préstamos SaaS, gestión de clientes, préstamos, pagos y cartera.
- `productos/acceso-escolar-inem.html`: Acceso Escolar INEM, control de ingreso y asistencia.

Ambos proyectos siguen como **repositorios privados** en GitHub. El portal principal ahora los presenta dentro de «Productos y soluciones», con enlaces exclusivamente a estas fichas públicas y no a GitHub privado. «Recursos y proyectos abiertos» mantiene solo enlaces públicos.

Las fichas:
- Presentan objetivos y alcance general sin prometer funcionalidades finalizadas, conformidad legal, certificaciones ni disponibilidad comercial.
- No incluyen capturas de datos reales, QR, credenciales, rutas internas de aplicaciones ni enlaces a repositorios privados.
- Usan la marca gráfica original aprobada y estilos reutilizados del portal; respetan accesibilidad básica y puntos de quiebre responsive.
- Indican explícitamente que el producto está en desarrollo y que el código no es público.
- Ofrecen contacto por el correo público corporativo ya presente en el sitio.

**Política:** ningún archivo de prueba con información de personas, inventarios, préstamos, registros escolares ni datos de menores debe subirse a estas páginas. Las posibles imágenes de interfaz se validarán y anonimizarán/sintetizarán antes de publicación. Mantener privado no sustituye auditoría de seguridad y revisión de licencias/autorizaciones institucionales.
