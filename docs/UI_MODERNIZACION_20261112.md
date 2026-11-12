# Evolución de interfaz del portal ADL · 2026-11-12

**Estado:** código fusionado a `main`, compilado y desplegado en GitHub Pages el 2026-11-12. Pruebas automáticas de navegador Chrome (escritorio y móvil), rutas e identidad corporativa exitosas. La auditoría manual WCAG completa y la consulta HTTP independiente del resultado publicado no se efectuaron.  
**Rama original:** `ui/refresh-portal-adl-20261112`, integrada mediante PR #36.

Se mejoró la jerarquía visual de acciones, tarjetas de proyectos, trayectoria y productos, con ajustes móviles, foco accesible y soporte de movimiento reducido. El CSS se versionó como `portal.css?v=1.6` en la portada para evitar ver estilos antiguos después de una futura publicación.

No se alteran los logotipos SVG corporativos v4.0 ni la identidad profesional, contenido institucional, licencias, fichas comerciales, métricas o enlaces de datos.

**Verificado estáticamente:** selectores relevantes, llaves CSS, rutas oficiales SVG y versión del recurso.  
**Pendiente:** pruebas visuales de navegación, móvil 320/360/768/1440, accesibilidad, enlaces, Lighthouse y CI de GitHub Pages antes de fusionar o publicar.

No reabrir INEM Convive ni proyectos pausados por un ajuste del portal.

## Evidencia de publicación
- PR: https://github.com/ljarias/ljarias.github.io/pull/36
- Commit fusionado: `92a0d037ba7d462a8b8c8296cc87f1faa0a5a937`.
- GitHub Actions: https://github.com/ljarias/ljarias.github.io/actions/runs/43293903639 (build, deploy y report-build-status, todos SUCCESS).
- Pruebas PR: Jekyll/rutas, identidad SVG v4.0 y Chrome mobile/desktop, todas SUCCESS.
- Público: https://ljarias.github.io/ (publicación certificada por GitHub Pages; comprobación HTTP independiente pendiente por limitación de red del entorno de ejecución).
