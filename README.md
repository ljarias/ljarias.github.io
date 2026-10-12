# Arias-Data-Lab · Portal corporativo y ecosistema digital

**Portada principal:** https://ljarias.github.io/  
**Identidad:** Arias-Data-Lab · *Tecnología con criterio humano.*

Este repositorio público reúne el portal profesional, recursos educativos, el observatorio de inteligencia artificial y las presentaciones públicas de proyectos con código privado.

## Arquitectura del sitio

| Página | Dirección |
|---|---|
| Portal corporativo principal | [ljarias.github.io](https://ljarias.github.io/) |
| IA al Día — Observatorio de IA | [ljarias.github.io/ia-al-dia/](https://ljarias.github.io/ia-al-dia/) |
| Archivo y noticias de IA | [ljarias.github.io/ia-al-dia/](https://ljarias.github.io/ia-al-dia/#ultimas) |
| Transparencia y telemetría | [ljarias.github.io/ia-al-dia/telemetria/](https://ljarias.github.io/ia-al-dia/telemetria/) |
| Acerca de IA al Día | [ljarias.github.io/ia-al-dia/acerca/](https://ljarias.github.io/ia-al-dia/acerca/) |
| Banco de Problemas del Caribe | [ljarias.github.io/banco-problemas-caribe/](https://ljarias.github.io/banco-problemas-caribe/) |
| Productos y soluciones | [ljarias.github.io/arias-data-lab/productos/](https://ljarias.github.io/arias-data-lab/productos/) |

El portal antiguo `/arias-data-lab/` sigue accesible como redirección hacia la portada raíz. El catálogo y las fichas de productos **no se han movido**.

## Cambios en las direcciones de IA al Día

- Portada del observatorio: `/` → `/ia-al-dia/`
- Acerca de: `/acerca/` → `/ia-al-dia/acerca/`
- Telemetría: `/telemetria/` → `/ia-al-dia/telemetria/`
- Ediciones fechadas: `/AAAA/MM/DD/titulo/` → `/ia-al-dia/AAAA/MM/DD/titulo/`
- Cada una de las seis entradas previas tiene una página de redirección compatible con navegadores. El archivo original de publicaciones y la información histórica no se alteraron.
- Infografías: los SVG continúan en `/assets/infografias/`; se actualizaron los enlaces de sus fichas al nuevo destino de las noticias.

El generador `scripts/generar_infografia.py` guarda automáticamente `post_url` con el nuevo prefijo. Los archivos `_posts`, `data/historial.json` y `_data/consumo_api.json` continúan en sus directorios originales para que la automatización conserve su funcionamiento.

## Publicación y mantenimiento

La automatización editorial semanal permanece en `.github/workflows/publicar.yml`; mantiene su calendario de domingos a las 8:00 a. m. (hora de Bogotá), historial, telemetría y construcción Jekyll de GitHub Pages.

- **QA de identidad:** `.github/workflows/qa-identidad-adl.yml`, valida los seis SVG maestros y las referencias del sitio.
- **QA de rutas:** `.github/workflows/qa-portal-raiz.yml`, ejecuta `scripts/verificar_rutas_portal.py`, construye el sitio Jekyll sin publicar y prueba las rutas del archivo histórico.
- El sitio utiliza el vector aprobado de Arias-Data-Lab v4.0 en `assets/brand/logo/v4.0/`.

## Privacidad

Los repositorios `ljarias/prestamos-saas` y `ljarias/acceso-escolar-inem` son privados. El portal público ofrece fichas descriptivas sin enlazar al código interno, incluir bases de datos o divulgar información de estudiantes o clientes.

## Principio de operación

Arias-Data-Lab es el punto de entrada y paraguas institucional; IA al Día y los demás productos mantienen sus identidades y su navegación independiente. Evitar cambios de rutas sin conservar compatibilidad o enlaces históricos.
