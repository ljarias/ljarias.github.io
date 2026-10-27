# Instrucciones para Codex · V1.0 (2026-10-27)

## Reglas transversales
- Trabajar en español. Identificar repositorio, rama, estado de Git, documentación y pruebas antes de modificar.
- No mezclar proyectos ni reemplazar decisiones aprobadas sin contrastar evidencias.
- Distinguir PROPUESTO, IMPLEMENTADO, PROBADO, VALIDADO, DESPLEGADO y BLOQUEADO. Nunca inventar pruebas ni capturas.
- Auditorías: solo lectura. Implementaciones autorizadas: cambios mínimos, reversibles y dentro del alcance. Datos reales, secretos, permisos, costos y despliegues exigen autorización específica.
- Revisar sintaxis, dependencias, versiones, rutas, errores y seguridad. Probar lo pertinente y documentar lo no ejecutado.
- Respetar privacidad: no subir información personal de estudiantes, clientes o familiares, ni credenciales/tokens.
- Antes de enlazar archivos generados, verificar existencia, tamaño, formato, integridad y ruta exacta.
- En la entrega informar archivos modificados, verificaciones, limitaciones, riesgos y siguiente paso.

## Arias-Data-Lab y observatorio IA al Día
- Portal público construido con GitHub Pages/Jekyll: página corporativa, IA al Día, banco de problemas y fichas públicas de productos.
- Leer `README.md`, `_config.yml`, workflows en `.github/workflows/`, scripts y rutas actuales antes de cambiar navegación.
- Conservar redirecciones históricas de `/ia-al-dia/`, archivo de `_posts/`, índices, rutas de `assets/` y compatibilidad de publicaciones anteriores.
- Respetar identidad gráfica oficial Arias-Data-Lab, licencias de terceros y accesibilidad; no mostrar código privado ni detalles sensibles de proyectos internos.
- Los workflows pueden publicar automáticamente en GitHub Pages tras push en `main`; advertir este efecto antes de proponer cambios que afecten producción.
- Ejecutar QA de rutas/identidad con herramientas existentes si el entorno lo permite; no afirmar publicación sin verificar build y sitio.
