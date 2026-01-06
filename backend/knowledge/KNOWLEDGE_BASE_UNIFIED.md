# KNOWLEDGE_BASE_UNIFIED.md - MAAS v5.0 Source of Truth

## §1 - Flujo de 5 Fases de los Agentes Holónicos

Todos los agentes deben seguir este flujo de pensamiento y ejecución:

1. **FASE 1: PLANNING (Planificación)**
   - Definir qué datos se necesitan para la tarea actual.
   - Consultar hechos previos en el Context Broker.
2. **FASE 2: ACQUISITION (Adquisición)**
   - Obtener datos frescos de Redmine usando `RedmineTools`.
   - Buscar patrones similares en el histórico.
3. **FASE 3: KNOWLEDGE SEARCH (Búsqueda de Conocimiento)**
   - Consultar `rules_kb` para plantillas, normas y guías.
4. **FASE 4: ANALYSIS & STRUCTURING (Análisis y Estructuración)**
   - Usar `ReasoningTools` para procesar dependencias y lógica.
   - Mapear datos a esquemas Pydantic.
5. **FASE 5: SYNTHESIS (Síntesis)**
   - Generar el output final citando siempre las fuentes (Issue #ID).

## §2 - Mapeo de Datos Redmine a SIC (01-22)

| Sección SIC | Descripción | Fuente en Redmine (Campos Custom / Issues) |
|-------------|-------------|-------------------------------------------|
| SIC_01 | Resumen y Recomendaciones | Agregado de todos los issues, énfasis en #10940 |
| SIC_02 | Caso de Negocio | Campo 'Business Case', VAN, TIR de issue principal |
| SIC_03 | Riesgos | Issues con categoría 'Riesgo' o campo 'Risk Score' |
| SIC_07 | Geología | Issues técnicos, campo 'Geological Survey' |
| SIC_09 | Ingeniería Básica | Issues de ingeniería, campo 'Engineering Phase' |
| SIC_14 | Plazo/Cronograma | Fechas de inicio/fin de issues, campo 'Timeline' |
| SIC_16 | CAPEX | Campo 'CAPEX', 'Total Investment' |
| SIC_17 | OPEX | Campo 'OPEX', 'Operational Cost' |

## §3 - Estándares de Validación de Calidad (Audit)

El `ExpertJudgeAgent` debe validar:
1. **Completitud (30%)**: Todas las secciones SIC 01-22 deben estar presentes.
2. **Cumplimiento Normativo (40%)**: Alineación con NCC-24 (Normas de Coordinación de Proyectos).
3. **Evidencia (20%)**: Todos los datos técnicos deben citar un Issue ID de Redmine.
4. **Consistencia (10%)**: No debe haber contradicciones (ej. CAPEX en SIC 16 diferente al de SIC 02).

## §4 - Instrucciones de Auditoría (NCC-24)

- **Causal Analysis**: Realizar análisis de causa raíz para gaps identificados (Bow-Tie, 5 Whys).
- **Lessons Learned**: Priorizar "Lessons Learned" usando la matriz Impacto/Esfuerzo.
- **Regulatory Compliance**: Validar estrictamente contra los campos de NCC-24 definidos en `rules_ncc24.txt`.
