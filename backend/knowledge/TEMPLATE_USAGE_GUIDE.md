# TEMPLATE_USAGE_GUIDE.md - Guía de Uso de Plantillas SIC

## 1. Estructura de la Plantilla Maestra

La plantilla maestra se encuentra en `backend/knowledge/templates/PLANTILLA_MAESTRA_SIC_GENERICO.md`.
Contiene placeholders que deben ser reemplazados por el `GeneralAuthorAgent`.

### Placeholders Comunes
- `[PROYECTO_NOMBRE]`: Nombre oficial del proyecto de inversión.
- `[VALOR_NUMÉRICO]`: Datos como CAPEX, VAN, TIR o porcentajes.
- `[DESCRIPCIÓN_TÉCNICA]`: Texto redactado basado en los issues de Redmine.
- `[REFERENCIA_REDMINE]`: Cita al issue fuente (ej: *Fuente: Redmine #10940*).

## 2. Instrucciones por Sección

### SIC 01-05: Estrategia y Riesgos
- Enfatizar el alineamiento con el Plan de Negocios de la Corporación.
- Los riesgos deben clasificarse por Impacto y Probabilidad.

### SIC 07-10: Ingeniería y Geología
- Usar datos técnicos precisos (profundidad, toneladas, leyes de mineral).
- Citar issues específicos de la fase de Feasibility.

### SIC 14-17: Gestión y Finanzas
- El cronograma debe incluir hitos críticos.
- El CAPEX/OPEX debe desglosarse según la moneda (USD/CLP) si está disponible.

## 3. Manejo de Datos Faltantes
- Si un dato es crítico pero no existe, usar: `[PENDIENTE: REQUERIR_A_PROYECTO]`.
- En la sección de Recomendaciones (SIC 01), listar todos los gaps identificados.
