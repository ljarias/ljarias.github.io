# Arias-Data-Lab · Identidad corporativa (Patrón ADL)

**Logo maestro oficial: versión 4.0 · aprobado el 12/10/2026.**

El titular aprobó la reconstrucción vectorial multicolor basada en su PNG original de 1254 × 1254 px. La versión **SVG v4.0** es la referencia corporativa editable; el PNG original sigue siendo la **referencia visual histórica**. Los SVG se incorporaron al repositorio **sin alterar sus bytes** respecto al kit maestro aprobado.

## Archivos maestros

| Aplicación | Archivo |
|---|---|
| **Logo principal multicolor y transparente** | [ADL_logo-maestro-color_EDITABLE_v4.0.svg](logo/v4.0/ADL_logo-maestro-color_EDITABLE_v4.0.svg) |
| Logo multicolor con fondo blanco | [ADL_logo-sobre-blanco_EDITABLE_v4.0.svg](logo/v4.0/ADL_logo-sobre-blanco_EDITABLE_v4.0.svg) |
| Isotipo multicolor sin texto | [ADL_isotipo-color_EDITABLE_v4.0.svg](logo/v4.0/ADL_isotipo-color_EDITABLE_v4.0.svg) |
| Isotipo cuadrado para iconos | [ADL_isotipo-cuadrado_EDITABLE_v4.0.svg](logo/v4.0/ADL_isotipo-cuadrado_EDITABLE_v4.0.svg) |
| Variante auxiliar de una tinta azul | [ADL_logo-una-tinta-azul_VARIANTE.svg](logo/v4.0/ADL_logo-una-tinta-azul_VARIANTE.svg) |
| Variante auxiliar de una tinta blanca | [ADL_logo-una-tinta-blanco_VARIANTE.svg](logo/v4.0/ADL_logo-una-tinta-blanco_VARIANTE.svg) |

Ver [guía de uso y verificación](logo/v4.0/README.md) y [manifest.json](logo/v4.0/manifest.json) para confirmar integridad.

## Identidad

**Nombre:** Arias-Data-Lab  
**Lema:** Tecnología con criterio humano.  
**Paleta de interfaz:** [adl-tokens.css](adl-tokens.css) — navy `#102A43`, turquesa `#087F8C`, celeste `#D7F1F5`, amarillo `#F4B942`, hielo `#F6F9FC` y gris `#475569`.

Los degradados de la marca reproducen los colores reconstruidos del PNG y **no deben reemplazarse** automáticamente por los colores planos de interfaz.

## Integración web

Para nuevas páginas, emplear una ruta relativa al SVG maestro:

```html
<img src="/assets/brand/logo/v4.0/ADL_logo-maestro-color_EDITABLE_v4.0.svg"
     alt="Arias-Data-Lab" width="240" height="240">
```

Para íconos, usar `ADL_isotipo-cuadrado_EDITABLE_v4.0.svg`. Conservar proporciones y espacio de seguridad. No modificar ni reinterpretar el arte.

**Migración web completada (12/10/2026):** la plantilla Jekyll de IA al Día, el portal Arias-Data-Lab, sus tres páginas de productos y las cuatro páginas del Banco de Problemas utilizan el logo SVG maestro aprobado v4.0. Los encabezados, pies y fondos decorativos emplean rutas al mismo recurso centralizado. Los favicons modernos utilizan el isotipo cuadrado SVG, con `favicon-32.png` conservado como compatibilidad. Los archivos raster anteriores permanecen disponibles como respaldo histórico; ya no son la fuente gráfica activa de las páginas migradas. Los proyectos de aplicaciones independientes y sus repositorios privados no fueron alterados. Ver [registro de migración y QA](MIGRACION-SITIOS-V4.md).

## Origen y alcance de la aprobación

- Referencia PNG original intacta: SHA-256 `4bf5ac3e7ed932cce40e743fc9758598609e552d940a27fe330d3e25300c2e54`.
- Reconstrucción aprobada: logo SVG maestro v4.0 con 8 capas, 25 trazados editables y 13 degradados. Sin imágenes incrustadas ni elementos `<text>`.
- La aprobación corresponde a una reconstrucción visual fiel, **no** a una recuperación exacta de las curvas y fuentes originales de un archivo fuente ya no disponible.
- Se conservan las variantes para impresión en PDF y los PNG preparados en el kit de identidad entregado al titular; el repositorio almacena aquí las fuentes SVG.

## Ubicación principal del ecosistema (12/10/2026)

La entrada pública canónica de Arias-Data-Lab es **https://ljarias.github.io/**. IA al Día se ofrece como observatorio independiente en **/ia-al-dia/**, manteniendo sus publicaciones, telemetría, infografías y automatización. El antiguo portal `/arias-data-lab/` redirige a la nueva portada raíz y sus fichas de productos siguen en `/arias-data-lab/productos/`. Esta reorganización no altera los seis SVG oficiales, los datos ni los repositorios privados.
