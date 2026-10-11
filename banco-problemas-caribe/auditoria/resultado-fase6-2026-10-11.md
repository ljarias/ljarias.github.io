# Auditoría estática — Banco de Problemas del Caribe
**Fase 6 · 11 de octubre de 2026 · Patrón ADL v3.2**

### Verificaciones realizadas
- Los cuatro documentos HTML declaran idioma y título, enlazan el logo corporativo aprobado y el favicon.
- Se revisaron las imágenes y sus `alt`; no se encontraron imágenes sin ese atributo.
- Se verificaron enlaces internos con fragmentos y sus destinos en la navegación principal: sin objetivos ausentes en el análisis estático.
- Se verificó el uso de `rel="noopener"` o `noreferrer` en enlaces externos con `target="_blank"`.
- No se reescribieron ni el catálogo, ni su JSON embebido, ni el prompt maestro.
- Se añadieron enlaces para saltar al contenido en tres páginas independientes.
- Se corrigió el selector de CSS que estilaba indebidamente el pie de nota de seguridad dentro de la guía.
- Los tokens institucionales compartidos se ubican en `/assets/brand/adl-tokens.css`.

### Límites de esta auditoría
- No equivale a certificación WCAG 2.1 AA.
- La inspección estática no demuestra comportamiento de teclado o lector de pantalla ni captura visual responsive en dispositivos reales.
- La prueba en navegador real y la comparación visual sobre el sitio publicado siguen recomendadas.
- **No existe aún un SVG multicolor de curvas y degradados completamente editable, visualmente idéntico al logo original.** Para usos web y documentos, conservar PNG/WebP derivados sin rediseño.
