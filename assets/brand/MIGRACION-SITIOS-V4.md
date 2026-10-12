# Migración web Arias-Data-Lab al logo vectorial oficial v4.0

**Fecha:** 12 de octubre de 2026  
**Referencia maestra:** [SVG oficial](logo/v4.0/ADL_logo-maestro-color_EDITABLE_v4.0.svg)  
**Estado:** cambio completo para despliegue y control automatizado. La confirmación definitiva de publicación corresponde al workflow de GitHub Pages.

## Alcance aplicado

| Destino | Componentes migrados |
|---|---|
| IA al Día (raíz) | Plantilla Jekyll `_layouts/default.html`: logo cabecera, logo pie, favicon SVG con respaldo PNG; todos los posts que utilizan esta plantilla heredan el cambio |
| Portal Arias-Data-Lab | Página principal `arias-data-lab/index.html`: hero, pie, icono compacto y favicon |
| Productos y soluciones | `arias-data-lab/productos/`: catálogo y dos fichas de proyecto |
| Banco de Problemas del Caribe | `index.html`, `acerca-de.html`, `guia-documentacion.html`, `prompt-maestro.html`: cabeceras, pies, referencias decorativas en CSS inline e iconos |

## Decisiones técnicas

- Fuente canónica: `/assets/brand/logo/v4.0/ADL_logo-maestro-color_EDITABLE_v4.0.svg`.
- Icono escalable: `/assets/brand/logo/v4.0/ADL_isotipo-cuadrado_EDITABLE_v4.0.svg`.
- Favicons: `image/svg+xml` más `image/png` heredado como respaldo.
- Ruta versionada v4.0, sin sustitución destructiva de `logo-adl-v3.webp` ni `favicon-32.png`.
- Se conservaron las medidas de maquetación de los contenedores y el estilo visual del patrón ADL. La versión de CSS del portal incorpora una actualización de caché.
- El arte SVG original **no fue modificado**; los seis SVG del kit permanecen idénticos a los aprobados.

## Pruebas

1. `python3 scripts/verificar_marca_adl.py` verifica SHA-256 de los seis SVG contra `manifest.json`, parseo XML, cantidad de curvas y ausencia de imágenes incrustadas.
2. El mismo script comprueba referencias al logo maestro y al isotipo en las nueve páginas/plantillas, rutas relativas reales y ausencia de enlaces desde fichas públicas a los repositorios privados.
3. Validación estática adicional de HTML y de enlaces internos de las páginas modificadas.
4. Se compararon bloques `<script>` del Banco de Problemas contra el estado previo y resultaron idénticos. No cambiaron datasets, scripts o contenido de problemas.
5. Despliegue final: revisar los estados de `pages build and deployment` y `Verificar identidad corporativa ADL` en la pestaña Actions.
6. Revisión visual en navegador y dispositivos físicos: deseable; una ejecución exitosa en GitHub Actions **no reemplaza** una auditoría WCAG completa ni equivale a una prueba humana en todos los navegadores.

## Fuera del alcance

- No se cambian los repositorios privados `ljarias/prestamos-saas` ni `ljarias/acceso-escolar-inem`, sus sistemas de producción, bases de datos, credenciales o infraestructura.
- No se reemplazan las imágenes dentro de infografías históricas ni se reescribe la automatización editorial de IA al Día.
- No se afirma que una aplicación institucional esté certificada o autorizada para publicación.

**Próxima política:** todas las nuevas páginas corporativas deben utilizar el maestro v4.0 o su isotipo oficial, mantener el manifiesto intacto y ejecutar el control automático en los PR.
