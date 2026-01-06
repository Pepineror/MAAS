## PLANTILLA MAESTRA DE ESTRUCTURA Y DEPENDENCIAS PARA DOCUMENTOS SIC (Genérico)

### A. REGLAS DE ORQUESTACIÓN Y DEPENDENCIAS CRÍTICAS

La orquestación debe seguir una secuencia lógica donde los documentos de justificación (SIC 02, 03) y los de cumplimiento se generan antes que los documentos de detalle técnico y de costos (SIC 16, 17), y el Plan de Ejecución (SIC 14) es el integrador final.

| Orden de Creación (Fase) | Documento SIC (ID) | Título Principal | Dependencias Críticas (Input Requerido) |
| :--- | :--- | :--- | :--- |
| **01 (Base)** | **SIC 02** | CASO DE NEGOCIO | Datos de la Fase de Datos (Problema, Alcance, Justificación, Ubicación). |
| **02** | **SIC 03** | RIESGOS | **SIC 02** (Alcance, Contexto). Requiere la Matriz de Probabilidad e Impacto. |
| **03** | **SIC 04/05/06/10** | SSO, MEDIO AMBIENTE, DESECHOS, RELACIONES EXT. | **SIC 03** (Riesgos de Sustentabilidad); **SIC 02** (Ubicación, Contexto Legal). |
| **04** | **SIC 11/13/19/20** | INFRAESTRUCTURA, TECNOLOGÍA, LEGALES, COMERCIALES | **SIC 02** (Solución Técnica, Alcance, Requerimientos). |
| **05** | **SIC 16** | COSTOS DE CAPITAL (CAPEX) | **SIC 11** (Infraestructura/Solución Técnica); **SIC 03** (Contingencia por ETP). |
| **06** | **SIC 17** | COSTOS DE OPERACIÓN (OPEX) | **SIC 16** (Activos/Equipos); **SIC 12** (Dotación de Mantenimiento). |
| **07** | **SIC 12** | RECURSOS HUMANOS | **SIC 15** (Plan de Operación); **SIC 17** (Costo de Mantenimiento HH/año). |
| **08** | **SIC 14** | PLAN DE EJECUCIÓN DEL PROYECTO (PEP) | **Documento Integrador.** Depende de **SIC 03** (MCR/Riesgos), **SIC 16** (Costos/WBS), **SIC 11** (Secuencia Constructiva). |
| **09** | **SIC 15** | OPERACIONES | **SIC 14** (Plan de Puesta en Marcha/Traspaso). |
| **10** | **SIC 01** | RESUMEN Y RECOMENDACIONES | **Documento Ejecutivo Final.** Depende de **SIC 14** (Metas, Plazo); **SIC 16** (CAPEX Final); **SIC 03** (Riesgos Residuales). |
| **11** | **SIC 07, 08, 09, 18** | GEOLOGÍA, MINERÍA, PROCESAMIENTO, PRODUCTOS | Se generan y declaran No Aplicables si el Alcance es de Infraestructura/Servicios Auxiliares (Depende de **SIC 02**). |
| **12** | **SIC 21** | ANEXO FINANCIERO DETALLE | **SIC 16** (Flujos de Caja, Análisis de Sensibilidad detallado). |
| **13** | **SIC 22** | ANEXO TÉCNICO DETALLE | **SIC 11** (Especificaciones Técnicas, Planos de Ingeniería). |

---

## B. ESTRUCTURA DETALLADA DE ÍNDICES Y SECCIONES SIC

### SIC 01: RESUMEN Y RECOMENDACIONES

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **1. RESUMEN Y RECOMENDACIONES** | Presentación ejecutiva del proyecto (propósito, ubicación, alcance). |
| 1.1 Recomendación | Justificación del proyecto (e.g., cumplimiento normativo, continuidad operacional). Recomendación de avance (Go/No-Go). Costo de inversión (CAPEX) y plazo total de ejecución. |
| 1.2 Caso de Negocio | Resumen de la definición del problema y valor estratégico (e.g., evitar sanciones, asegurar suministro). |
| 1.3 Aspectos Técnicos del proyecto | Estrategia constructiva general (e.g., Frentes de trabajo, secuencia de actividades) y el diseño de la solución. |
| 1.4 Descripción del alcance del proyecto | Definición de los activos o sistemas a intervenir/reemplazar. |
| 1.5 Sustentabilidad y SSO | Resumen de los riesgos de Sustentabilidad y Salud Ocupacional (NCC-XX) y la aplicación de los estándares corporativos. |
| 1.6 Ejecución del Proyecto | Resumen del Plan de Ejecución (PEP) y los **Hitos Clave** (e.g., Adquisiciones, Construcción, Puesta en Marcha). |
| 1.7 Operación del Proyecto | Conclusión sobre el impacto en RRHH, plan de mantenimiento (OPEX) y costos operacionales. |
| 1.8 Alcance del Estudio y Plan de Trabajo | Agentes o empresas que participaron en el desarrollo del estudio (e.g., consultoras, contraparte). Declaración de fases de estudio futuras (si aplica). |
| 1.9 Parámetros Clave de Resultados y Parámetros Referenciales | Indicadores de éxito (Costo, Plazo, Seguridad, Ambiental) e indicadores económicos referenciales. |
| **ÍNDICE DE FIGURAS** | Figura X1: Esquema de activos existentes y proyectados. Figura X2/X3: Emplazamiento geográfico y ubicación de las instalaciones. Figura X4: Estrategia constructiva (Flujo). Figura X5: Variables clave de sustentabilidad por ámbito de relevancia (Gráfico). Figuras X6, X7, X8: Gráficos de Peligros (SSO, Salud, Bienes Físicos). |
| **ÍNDICE DE TABLAS** | Tabla X1: Condiciones geográficas y ambientales generales del sitio. Tabla X2: Indicadores Económicos (CAPEX, Plazo, Ahorros Referenciales). Tabla X3: Principales procesos operativos antes y después de la intervención. Tabla X4: Paquetes de trabajo y sus actividades por disciplina. Tabla X5: Hitos del Proyecto (con fechas). Tabla X6: Agentes en el desarrollo de los estudios. |

### SIC 02: CASO DE NEGOCIO

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **2. CASO DE NEGOCIO** | Justificación detallada del proyecto de inversión. |
| 2.1 Resumen | Resumen de la justificación principal (e.g., cumplimiento normativo y continuidad operacional) y objetivos. |
| 2.2 Contexto | **Descripción del Problema:** Detalle del problema (e.g., obsolescencia de activos, mandato de cumplimiento legal). **Ubicación y condiciones de sitio:** Región, comuna, altitud, condiciones ambientales (Tabla 21). **Demanda Máxima:** Demanda de energía o recursos que requieren los procesos productivos. (Tabla 22). |
| 2.3 Atractivo Industrial | **Valor Externo:** Cumplimiento de compromisos corporativos o ambientales (e.g., imagen corporativa). **Valor Interno:** Continuidad operacional, aseguramiento de la calidad de servicio (e.g., cumplimiento de factor de potencia). |
| 2.4 Alineamiento Estratégico | Ajuste a los planes productivos (PND) y estrategia corporativa. Importancia del proyecto para la continuidad de la Línea de Producción. |
| 2.5 Opciones Estratégicas del Proyecto | Análisis de la viabilidad de postergar o abandonar el proyecto frente a los plazos de cumplimiento (e.g., Convenio de Estocolmo). |
| 2.6 Análisis de Escenarios | **Escenario sin proyecto (Caso Base):** Consecuencias operacionales y financieras de no ejecutar el proyecto (e.g., detención operacional, sobrecostos). **Escenario con el proyecto (Recomendado):** Beneficios económicos cuantificables (e.g., ahorros mensuales/anuales). |
| 2.7 Estrategia de Salida | Declaración sobre si el proyecto considera o no una estrategia de salida (Generalmente no aplica para proyectos de cumplimiento/seguridad). |
| 2.8 Proceso de Configuración y Grupos de Interés | Configuración técnica recomendada y optimizada. Listado de los principales *Stakeholders* (e.g., Gerencia, Operaciones, Organismos Reguladores). |
| 2.9 ANEXOS | ANEXO A: Evaluación Económica Detallada (.XLSM). ANEXO B: Informe de Condición Operacional/Técnica. |
| **ÍNDICE DE FIGURAS** | Figura 21: Esquema de activos existentes y proyectados. Figura 22/23: Emplazamiento Geográfico. Figura 24: Gráfico de Demanda de Recursos/Potencia del Proceso Productivo (PND). |
| **ÍNDICE DE TABLAS** | Tabla 21: Condiciones geográficas y ambientales generales del sitio. Tabla 22: Demanda Máxima PND – Período de N años (MVA/Toneladas por proceso). Tabla 23: Indicadores Económicos (VAN/TIR si aplica, Ahorros Referenciales). |

### SIC 03: RIESGOS

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **3. RIESGO** | Análisis de riesgos en las etapas de ejecución, operación y cierre del proyecto. |
| 3.1 Resumen | Perfil de riesgos inicial (inherente) y residual (post-mitigación). Énfasis en áreas de alto impacto (e.g., construcción, abastecimiento). |
| 3.2 Contexto y Antecedentes | Metodología de análisis de riesgos (e.g., NCC N°47, Procedimiento Corporativo). **Tabla 32/33/34:** Métrica de Probabilidad e Impacto (escalas, consecuencias en CAPEX, Plazo, SySO, Legal). |
| 3.3 Resultado del análisis cualitativo de riesgo | Cuantificación inicial y residual de riesgos (Total identificados, Riesgos Altos/Medios/Bajos). |
| 3.4 Identificación y análisis de los principales riesgos | **Tabla 37: Matriz de Riesgos** (ID, Evento Incierto, Causa, Consecuencia(s)). Incluir riesgos clave (e.g., incumplimiento legal, errores de alcance, fallas de equipos). |
| 3.5 Evaluación y tratamiento de los principales riesgos | **Tabla 38: Controles de Mitigación.** (Riesgo, MRIg [Magnitud Inherente], Controles, MRRg [Magnitud Residual]). |
| 3.6 Evaluación cuantitativa de riesgo | Cálculo de la **Exposición Total del Proyecto (ETP)** en términos de CAPEX y Plazo (requiere fórmulas ETP). |
| 3.7 Plan de gestión de Riesgo | Detalle de las responsabilidades, programa de monitoreo y control (frecuencia, reuniones) y manejo de la información (Consultar SIC 14). |
| **ANEXOS** | ANEXO A: Matrices de Riesgo Detalladas. ANEXO B: Informe NCC47/Estándar Corporativo de Gestión integral de Riesgos. |
| **ÍNDICE DE FIGURAS** | Figura 34: RBS (Estructura de Desglose de Riesgos) del proyecto (Gráfico). Figura 35: Cantidad de riesgos por familia (Gráfico). Figuras 36/37: Distribución de riesgos (Inherentes y Residuales) por familia (Gráficos). |
| **ÍNDICE DE TABLAS** | Tablas 32/33/34: Métrica de probabilidad, impacto y Magnitud del riesgo (Matriz Probabilidad/Impacto). Tablas 35/36: Magnitud de los riesgos (Inherentes y Residuales). Tabla 37: Identificación de riesgos. Tabla 38: Controles de mitigación de riesgos. |

### SIC 04: SEGURIDAD Y SALUD OCUPACIONAL (SSO)

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **4. SEGURIDAD Y SALUD OCUPACIONAL** | Propósito, alcance y objetivos del análisis de SSO. |
| 4.1. Descripción del problema | Listado de equipos o activos a intervenir/reemplazar por Subestación/Área. Cuantificación de los riesgos de exposición (e.g., 10 bancos, 75.5 ton). |
| 4.2. Política Corporativa de Gestión de Seguridad, Salud en el Trabajo y Riesgos Operacionales | Ilustración de la Política Corporativa de SSO (Figura 4-1). |
| 4.3. Definiciones | Definiciones de términos clave (e.g., Incidente, Peligro, Riesgo, Riesgo Crítico). |
| 4.4. Objetivos del Análisis de S. y S.O. | Aplicación de la Norma Corporativa NCC-24 (o estándar equivalente) para identificar Peligros y evaluar Riesgos. |
| 4.5. Antecedentes del Proyecto | Actividades realizadas para el análisis (Reconocimiento del sitio, Revisión de normativas, Levantamiento de condiciones subestándar). |
| 4.6. Objetivo del Documento | Alertar a la organización de peligros y riesgos y medidas de control. |
| 4.7. Objetivos del Proyecto | Reemplazo de activos, cumplimiento normativo y aseguramiento de la función operativa. |
| 4.8. Emplazamiento del proyecto y condiciones de sitio | Ubicación geográfica y condiciones generales del sitio (Tabla 4-2). |
| 4.9. Criterios para la determinación de la magnitud del riesgo a las personas y a los bienes físicos | Criterios de evaluación de la consecuencia e impacto según el Procedimiento Corporativo. |
| 4.10. Análisis de Riesgo de Seguridad a las Personas | Identificación y cuantificación de peligros a la seguridad (e.g., 94 situaciones). Peligros relacionados con **Estándares de Controles Críticos (ECC)** (e.g., Interacción con energía eléctrica, trabajo en altura). |
| 4.11. Análisis de Peligros que revisten Riesgos a la Salud de las Personas | Identificación y cuantificación de peligros a la salud ocupacional (e.g., 58 situaciones) (Exposición a ruido/vibraciones, manejo manual de cargas). Cumplimiento de Protocolos guías y normas técnicas. |
| 4.12. Análisis de riesgo a bienes físicos | Evaluación de peligros de riesgo a los Bienes Físicos. |
| 4.13. Identificación/Análisis Variables Claves de Sustentabilidad | Aplicación de Norma Corporativa NCC-XX; evaluación de variables de relevancia Alta/Media (e.g., manejo de sustancias peligrosas, Incertidumbre en la Gestión). Líneas de acción (e.g., Plan de Seguridad y Salud en el Trabajo, ECC). |
| 4.14. ANEXOS | ANEXO 1: Matriz de Riesgos y Controles (VACS-SI-F-008). |
| **ÍNDICE DE FIGURAS** | Figura 4-1: Política Corporativa SSO. Figuras 4-2, 4-3, 4-4: Emplazamiento y activos. Figura 4-5: Criterios de evaluación. Figuras 4-6, 4-7, 4-8: Gráficos de Peligros (Seguridad, Riesgos Altos, Salud Ocupacional). |
| **ÍNDICE DE TABLAS** | Tabla 4-1: Activos a intervenir con contaminantes por Subestación/Área. Tabla 4-2: Condiciones geográficas y ambientales generales del sitio. Tabla 4-3: Peligros por proceso (N° de situaciones de peligro). Tablas 4-4/4-5: Peligros que revisten riesgos altos a la seguridad y salud. |

### SIC 05: MEDIO AMBIENTE

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **MEDIO AMBIENTE** | Justificación del proyecto desde la perspectiva ambiental. |
| Resumen del Proyecto | Descripción del problema (e.g., contaminantes orgánicos persistentes) y el plan de retiro, reemplazo y eliminación certificada. |
| Contexto | Necesidad de eliminar activos peligrosos. Cronograma de obras previas y montaje. |
| Análisis de Variables Clave de Sustentabilidad | **Tabla 5-2: Análisis de Variables Claves.** Evaluación de impacto a componentes ambientales (Suelo, Aire) y **Riesgos críticos ambientales** (e.g., manejo de sustancias peligrosas). Medidas de control para prevenir efectos (e.g., uso de bandejas en transporte, cumplimiento SIDREP). |
| Estrategia Ambiental | Plazos de cumplimiento normativo (e.g., detención de uso 2025, eliminación 2028). **Protocolos de manejo de residuos peligrosos** (supervisión, cumplimiento D. 148/2004 y D. 298). Permisos estratégicos y no críticos a tramitar. |
| Medidas de Mitigación, Reparación y Compensación | Declaración de **no ingreso** (o ingreso) al SEIA. Justificación de que **no necesita medidas de mitigación, reparación y/o compensación** (si aplica) o descripción de las medidas de control. |
| Cumplimiento Normativo | Resumen de la Normativa Ambiental y SSO (e.g., Matriz de Regulación VACS-SI-F-004). |
| Relación del Proyecto con Lineamientos Corporativos de Sustentabilidad | **Tabla 5-3/5-4:** Alineamiento con los compromisos de sustentabilidad (e.g., Convenio de Estocolmo/Basilea). |
| Plan de Ejecución Costos y Recursos | Costo estimado del contrato de Retiro y Eliminación de residuos peligrosos (e.g., 1.511 KUS$). Seguimiento a permisos de la empresa eliminadora. |
| Cierre y Post Cierre | Declaración de que el cierre es parte del Plan de Cierre Divisional vigente autorizado. |
| **ÍNDICE DE FIGURAS** | Figuras 5-1, 5-2, 5-3: Emplazamiento Geográfico y activos. |
| **ÍNDICE DE TABLAS** | Tabla 5-1: Condiciones geográficas y ambientales generales del sitio. Tabla 5-2: Analisis de Variables Claves de Sustentabilidad (Impacto, relevancia e indicadores). Tabla 5-3: Relación del Proyecto con los compromisos de sustentabilidad (corporativos/nacionales). |

### SIC 06: RELACIONES EXTERNAS Y COMUNITARIAS

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **RELACIONES EXTERNAS Y COMUNITARIAS** | Evaluación del impacto en el entorno social y grupos de interés. |
| Resumen del Proyecto | Descripción del problema (e.g., necesidad de eliminar contaminantes) y alcance del proyecto. |
| Revisión Marco Normativo Comunitario Aplicable al Proyecto | **Tabla 6-2: Revisión Marco Normativo Comunitario.** Evaluación de leyes (e.g., Ley 19.300 / SEIA, Convenio 169 OIT) y su relación con el proyecto (e.g., **No Aplica** ingreso al SEIA). |
| Análisis de los Principales Aspectos Comunitarios Asociados al Proyecto | **Tabla 6-3/6-4: Análisis Aspectos Comunitarios.** Identificación de **Grupos de Interés Críticos (GIC)**. Evaluación de riesgos de **Alteración infraestructura comunitaria** (e.g., red vial, seguridad, salud) y medidas de mitigación valorizadas (e.g., contratación de mano de obra local). |
| Plan de Acción Comunitario Requerido por el Proyecto | **Tabla 6-5: Plan de Acción Comunitario (PAC)**. Detalle de acciones (Medida, Plazos, Recursos, Resultados Esperados) para abordar variables críticas (e.g., plan para evitar exposición de habitantes durante transporte de residuos peligrosos). |
| **ANEXOS** | ANEXO 1. INFORME DE APLICACIÓN DE NORMA NCC24 V4 / Análisis de Riesgos en Sustentabilidad. |
| **ÍNDICE DE FIGURAS** | Figuras 6-1, 6-2, 6-3: Emplazamiento Geográfico y activos. |
| **ÍNDICE DE TABLAS** | Tabla 6-1: Condiciones geográficas y ambientales generales del sitio. Tabla 6-2: Revisión Marco Normativo Comunitario. Tablas 6-3/6-4/6-5: Análisis Aspectos Comunitarios y Plan de Acción Comunitario. |

### SIC 07: GEOLOGÍA Y RECURSOS MINERALES

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **7. GEOLOGÍA Y RECURSOS MINERALES** | Declaración de la no afectación a la base geológica/mineral. |
| 7.1 Resumen del Proyecto | Descripción del alcance del proyecto (e.g., reemplazo de activos, infraestructura). |
| 7.2 Resumen del capítulo | Declaración de que el capítulo **no fue desarrollado/no aplica** porque el proyecto no genera variaciones en la base geológica actual (e.g., la intervención es superficial o en infraestructura existente). |
| 7.3 Geología Regional | Declaración de **no desarrollado** (si aplica). |
| 7.4 Historial de Exploración | Declaración de **no desarrollado** (si aplica). |
| 7.5 Recopilación de Datos | Declaración de **no desarrollado** (si aplica). |
| 7.6 Geología del Yacimiento | Declaración de **no desarrollado** (si aplica). |
| 7.7 Estimación de Recursos | Declaración de **no desarrollado** (si aplica). |
| 7.8 Geometalurgia y Caracterización Ambiental | Declaración de **no desarrollado** (si aplica). |
| 7.9 Hidrogeología | Declaración de **no desarrollado** (si aplica). |
| 7.10 Geotecnia y Geomecánica | Declaración de **no desarrollado** (si aplica). |
| 7.11 Programa de Trabajo | Declaración de **no desarrollado** (si aplica). |
| 7.12 Evaluación de Riesgo | Declaración de **no desarrollado** (si aplica). |
| 7.13 Declaración de Recursos Geológicos | Declaración de **no desarrollado** (si aplica). |
| **ÍNDICE DE FIGURAS** | Figuras 71, 72, 73: Emplazamiento Geográfico y activos. |
| **ÍNDICE DE TABLAS** | Tabla 71: Condiciones geográficas y ambientales generales del sitio. |

### SIC 08: MINERÍA Y RESERVAS MINERALES

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **8. MINERÍA Y RESERVAS MINERALES** | Evaluación del impacto en la base de recursos y reservas minerales. |
| 8.1 Resumen del Proyecto | Descripción del alcance del proyecto (e.g., reemplazo de activos, infraestructura). |
| 8.2 Resumen del capítulo | Declaración de que el capítulo **no fue desarrollado/no aplica** porque el proyecto no genera variaciones en la base de recursos minerales y reservas mineras ni en la planificación minera actual. |
| 8.3 Consideraciones para el Diseño Minero | Declaración de **no desarrollado** (si aplica). |
| 8.4 Diseño Minero | Declaración de **no desarrollado** (si aplica). |
| 8.5 Planificación Minera | Declaración de **no desarrollado** (si aplica). |
| 8.6 Declaración de Recursos Minerales y Reservas Mineras | Declaración de **no desarrollado** (si aplica). |
| 8.7 Evaluación de Riesgo | Declaración de **no desarrollado** (si aplica). |
| **ÍNDICE DE FIGURAS** | Figuras 81, 82, 83: Emplazamiento Geográfico y activos. |
| **ÍNDICE DE TABLAS** | Tabla 81: Condiciones geográficas y ambientales generales del sitio. |

### SIC 09: PROCESAMIENTO DE MINERALES

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **9. PROCESAMIENTO DE MINERALES** | Evaluación del impacto en los parámetros de diseño del proceso y el plan de producción. |
| 9.1 Resumen del Proyecto | Descripción del alcance del proyecto (e.g., reemplazo de activos, infraestructura). |
| 9.2 Resumen del capítulo | Declaración de que el capítulo **no fue desarrollado/no aplica** porque el proyecto no genera variaciones en los parámetros de diseño del proceso ni en el plan de producción actual. |
| 9.3 Pruebas Metalúrgicas, de Laboratorio y Piloto | Declaración de **no desarrollado** (si aplica). |
| 9.4 Selección y Base del Proceso | Declaración de **no desarrollado** (si aplica). |
| 9.5 Residuos del Procesamiento de Mineral | Declaración de **no desarrollado** (si aplica). |
| 9.6 Descripción de la Planta | Declaración de **no desarrollado** (si aplica). |
| 9.7 Interferencias con Operaciones y Otros Proyectos | Declaración de **no desarrollado** (si aplica). |
| 9.8 Plan de Producción | Declaración de **no desarrollado** (si aplica). |
| 9.9 Evaluación de Riesgos | Declaración de **no desarrollado** (si aplica). |
| **ÍNDICE DE FIGURAS** | Figuras 91, 92, 93: Emplazamiento Geográfico y activos. |
| **ÍNDICE DE TABLAS** | Tabla 91: Condiciones geográficas y ambientales generales del sitio. |

### SIC 10: MANEJO DESECHOS Y GESTIÓN DE AGUAS

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **MANEJO DESECHOS Y GESTIÓN DE AGUAS** | Resumen ejecutivo del proyecto (alcance, problema, ubicación). |
| Fuente y Volumen de Emisiones, Descargas y Residuos | **Emisiones:** Emisiones atmosféricas (MP10, SO2) y medidas de control (e.g., humectación). **Descargas:** Declaración de **no generación de descarga de efluentes industriales**. **Residuos:** Cuantificación de residuos peligrosos (e.g., contaminantes) y no peligrosos (e.g., acero, hormigón). Cuantificación de desechos líquidos (e.g., baños químicos, disgregante fecal). |
| Medidas de Mitigación, Reparación y Compensación | Declaración de no implementación de medidas SEIA. Medidas de control de **Suelo** (e.g., Plan de Emergencias, Sistemas de Gestión) y **Aire** (e.g., revisión técnica de vehículos, humectación). |
| Cumplimiento Normativo | Resumen de Normativa Ambiental y SSO (e.g., D. 148, D. 298, SIDREP, Matriz de Regulación VACS-SI-F-004). |
| Relación del Proyecto con Lineamientos Corporativos de Sustentabilidad | **Tabla 10-2:** Alineamiento con los compromisos de sustentabilidad (e.g., convenios internacionales). |
| **ANEXOS** | ANEXO 1. INFORME DE APLICACIÓN DE NORMA NCC24 V4. |
| **ÍNDICE DE FIGURAS** | Figuras 10-1, 10-2, 10-3: Emplazamiento Geográfico y activos. |
| **ÍNDICE DE TABLAS** | Tabla 10-1: Condiciones geográficas y ambientales generales del sitio. Tabla 10-2: Relación del Proyecto con los compromisos de sustentabilidad. |

### SIC 11: INFRAESTRUCTURA Y SERVICIOS

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **11. INFRAESTRUCTURA Y SERVICIOS** | Descripción de la infraestructura existente y nueva. |
| 11.1 Resumen del proyecto | Descripción del problema (e.g., cumplimiento normativo, obsolescencia) y alcance del proyecto. |
| 11.2 Resumen del capítulo | Presentación de la infraestructura existente y la infraestructura nueva. |
| 11.3 Infraestructura existente | Descripción de las instalaciones existentes (e.g., subestaciones, plantas, fundaciones, capacidad). |
| 11.4 Infraestructura nueva | **Reemplazo/Adaptación:** Nuevos equipos (e.g., equipos híbridos, modulares, contenedores) manteniendo la capacidad actual. Estructuras de soporte proyectadas. |
| Estudio de Emplazamientos | Declaración de que las obras se emplazarán en las áreas actuales o en espacios libres cercanos, sin interferir con la operación (Figura 1111). |
| Instalaciones Planta | **Almacenamiento de productos:** Plan de manejo/almacenamiento de residuos peligrosos. **Taller/Barrio Cívico/Campamento/Laboratorios:** Declaración de **no aplica** (si corresponde). |
| Suministros e insumos | Requerimientos de Energía eléctrica, Agua, Combustible, y Disposición de residuos. |
| Infraestructura Temporal | Requerimientos de Energía eléctrica, Agua (e.g., bidones), Áreas de instalación de faenas y Comunicaciones (e.g., celulares). |
| **ANEXOS** | ANEXO A: NCC 30 Mantenibilidad y Confiabilidad. ANEXO B: NCC 32 Eficiencia Energética. |
| **ÍNDICE DE FIGURAS** | Figuras 114 a 118: Activos Existentes (e.g., Bancos de Condensadores S/E A). Figuras 119/1110: Equipos Nuevos (e.g., Equipos Híbridos/Disposición Modular). Figura 1111: Emplazamiento de subestaciones/áreas de intervención (Mapa). |
| **ÍNDICE DE TABLAS** | Tabla 111: Condiciones geográficas y ambientales generales del sitio. |

### SIC 12: RECURSOS HUMANOS

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **12. RECURSOS HUMANOS** | Evaluación del impacto en la dotación, competencias y gestión de personal. |
| 12.2 Resumen del capítulo | Declaración de **no modificación a la dotación operacional** (si aplica). Requerimientos de **HH/año** para mantenimiento (e.g., 420 HH/año) y alcance de capacitación/entrenamiento. |
| 12.3 Competencias requeridas | Conclusión sobre si aplica o no la evaluación de competencias. Requerimiento de capacitación y entrenamiento en terreno (e.g., al proveedor). |
| 12.4 Fuentes de Recursos Humanos | Declaración de **no contemplar un nuevo vector dotacional** (si aplica). Estrategia de reentrenamiento del personal actual. Cuantificación de HH/año para mantenimiento preventivo. |
| 12.5 Gestión de Operaciones | Declaración de **no modificación** de la organización actual para atender las nuevas instalaciones. |
| 12.6 Productividad | Conclusión de **no impacto** en la productividad de la fuerza laboral (si aplica). |
| 12.7 Evaluación de Impactos | Conclusión de no impacto en la organización/dotación. Énfasis en el cumplimiento de la normativa que asegura la protección del medio ambiente y las personas. |
| 12.8 Criterios Detallados | **Obligaciones Legales:** Listado de normativas aplicables (e.g., Código del Trabajo, D.S. N° 594, Ley 16.744, D.S. N° 38/2005 Convenio de Estocolmo). |
| **ANEXOS** | Anexo A: Matriz RRHH. Anexo B: Nota interna. |
| **ÍNDICE DE FIGURAS** | Figuras 121, 122, 123: Emplazamiento Geográfico y activos. |
| **ÍNDICE DE TABLAS** | Tabla 121: Condiciones geográficas y ambientales generales del sitio. |

### SIC 13: TECNOLOGÍA Y SISTEMAS DE INFORMACIÓN

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **13. TECNOLOGÍA Y SISTEMAS DE INFORMACIÓN** | Declaración de uso o no uso de nuevas TICS y su integración con sistemas existentes. |
| 13.2 Resumen del capítulo | Declaración de **no contemplar el uso de nuevas tecnologías de información y comunicaciones** (si aplica) y solo conexión de equipos reemplazados al sistema de control (e.g., SCADA/HMI) existente. |
| 13.3 Definiciones | Declaración de **no desarrollado** (si aplica). |
| 13.4 Tecnologías del proyecto | Requerimientos técnicos mínimos para la **conectividad Divisional** (e.g., SCADA, drivers, protocolos de comunicación). Riesgos tecnológicos asociados. |
| **ÍNDICE DE FIGURAS** | Figuras 131, 132, 133: Emplazamiento Geográfico y activos. |
| **ÍNDICE DE TABLAS** | Tabla 131: Condiciones geográficas y ambientales generales del sitio. |

### SIC 14: PLAN DE EJECUCIÓN DEL PROYECTO (PEP)

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **14. RESUMEN EJECUTIVO DEL PROYECTO** | Resumen de los principales objetivos y estrategias del PEP. |
| 14.1 VISIÓN DEL PROYECTO | **14.1.1 Objetivo Estratégico de Negocio:** Alineamiento con la estrategia (e.g., cumplimiento normativo). **14.1.2 Objetivo del Proyecto:** Costo total (CAPEX) y plazo. **14.1.3 Alcance:** Retiro, reemplazo y eliminación certificada de activos. **14.1.4 Línea Base:** Condiciones de sitio y ubicaciones (Tabla 14-1). |
| 14.2 Estructura de desglose del trabajo EDT (WBS Divisional) | **Ilustración 14-4:** WBS corporativa o divisional aplicable al proyecto (e.g., códigos de 5 dígitos). |
| 14.3 Entregables finales al cliente | **Tabla 14-2:** Entregables Finales al Cliente (Obras habilitadas, Operativas y Bajo Normativa Vigente), incluyendo Límites de Batería (LOB). |
| 14.4 Exclusiones del Proyecto | Lista de exclusiones (e.g., DIA/EIA, Provisión por paralizaciones, Resolución de interferencias por terceros). |
| 14.5 Metas e indicadores de éxito | **Tabla 14-3:** KPI (e.g., CAPEX total KUSD, Plazo total, Índice de Gravedad Cero, Incidentes Ambientales Cero). **Tabla 14-4:** Actividades Críticas a Controlar (e.g., Taller de Constructibilidad, Protocolos Puesta en Marcha). |
| **14.6 ESTRATEGIA PARA LA GESTIÓN DEL PROYECTO** | Descripción de la estrategia de gestión. |
| 14.6.1 Plan de Organización | **Ilustración 14-5:** Organigrama de Ejecución (DCH). **Roles y Responsabilidades** (e.g., Director, Jefe de Proyecto, Asesor SSO) con % de participación (Tabla detallada). |
| 14.6.2 Plan de gestión de Riesgos | **Tabla 14-5:** Plan de Riesgos MCR (Mitigación/Control/Respuesta) - Referencial al SIC 03. |
| 14.6.3 Plan de gestión de Ingeniería | Matriz de entregables de Ingeniería (Tabla 14-6), responsabilidades y **Estrategia de ejecución de la ingeniería** (e.g., detalles, vendors, adquisición). |
| 14.6.4 Plan de implementación de mejores prácticas (Lean Execution) | **Tabla 14-7:** Matriz Prácticas de Agregación de Valor (e.g., Pull Planning, Obeya, Should Cost, POD, Kaizen). |
| 14.6.5 Plan de gestión de Contratos | **Tabla 14-8: Matriz de Contratos** (Estrategia de contratación, Tipos de Contratos T&M/Fixed Price/Cost Reimbursable, Adquisiciones principales). |
| 14.6.6 Plan de gestión de Adquisiciones | **Tabla 14-9: Matriz de Adquisiciones** (Equipos principales, Proveedor, Crítico/No Crítico). Estrategia de inspección (e.g., Inspección en Fábrica/Plan de Inspección y Ensayos). |
| 14.6.7 Plan de gestión de la Construcción | **Secuencia Constructiva Detallada** por área/subestación. **Actividades Previas** (e.g., Instalación de Faena, Reconocimiento de Áreas, Acreditación de Personal). **Interferencias** (e.g., barras energizadas, cercanía de equipos). |
| 14.6.8 Plan de gestión de Puesta en marcha (PEM) | **Estrategia de PEM** (Comisionamiento y Puesta en Servicio). Plan de Puesta En Servicio (Organización, Cronograma y matriz de pruebas, Plan de energización). |
| **14.7 HERRAMIENTAS PARA LA GESTIÓN DEL PROYECTO** | Herramientas de soporte. |
| 14.7.3 Plan de gestión de la Calidad | **Tabla 14-10:** Matriz Plan de Calidad (Actividades QA/QC, Talleres de Riesgo, Auditoría a EECC, Gestión de No Conformidades). |
| 14.7.4 Plan de gestión de Sustentabilidad, medioambiente y permisos | Plan de gestión de Sustentabilidad y Medioambiente (VACS). |
| 14.7.5 Plan de gestión de permisos | **Tabla 14-11:** Matriz Plan de Permisos (Permisos estratégicos/no críticos, Plazos, Responsables). |
| 14.7.6 Plan de gestión de Costos | **Tabla 14-12:** Resumen de Costos (CAPEX total, Moneda Base, Tasa de Cambio). |
| 14.7.7 Plan de gestión del Cronograma | **Tabla 14-13: Resumen de Hitos** (Fechas de Adjudicación, Inicio Construcción, Fin Eliminación). **Criterios de Programación** (e.g., WBS, Primavera P6, Ruta Crítica, Calendario 7x7). |
| 14.7.8 Plan de Control integrado | Uso de Plataforma Corporativa de Control (EZPRO). **Control del Alcance, requisitos y cambios** (Control de Cambios SGPD). **Control de costos** (EAC, Valor Ganado). |
| 14.7.10 Plan de gestión de SSO | Plan de seguridad basado en NCC-24 (o estándar equivalente) e incorporación a Matriz de Gestión de Salud. |
| 14.7.11 Plan de gestión de las Comunicaciones | **Tabla 14-14: Matriz Plan de Comunicaciones** (Objetivo, Frecuencia, Responsable, Medio/Formato). |
| 14.7.12 Plan de gestión de Talleres | **Tabla 14-15: Matriz Plan de Talleres** (KOM, Constructibilidad, Revisión de Ingeniería). |
| 14.7.13 Plan de gestión de Documentos | **Estrategia Documental:** **Tabla 14-16: Matriz de Flujo Documental** (Entregables, Revisión, Almacenamiento SGDOC). **Reportabilidad Documental** (Estatus, Revisión, Estatus de Transmittal). |
| 14.7.14 Plan de Cierre del Proyecto | Plan de Cierre del Proyecto (SGPD-09GES-PLNGS-0001) para la entrega al Cliente y Cierre. |
| **ANEXOS** | ANEXO A/B/C/D/E: Plan de Ejecución (SGPD), Programas Maestros (XER/PDF), Cronograma Ruta Crítica. |
| **ÍNDICE DE FIGURAS** | Ilustración 14-4: WBS. Ilustración 14-5: Organigrama. Ilustración 14-6 a 14-11: Ilustraciones de activos intervenidos (existentes/proyectados). |
| **ÍNDICE DE TABLAS** | Tablas 14-1 a 14-16 (Condiciones Geográficas, Entregables, KPI, MCR, Contratos, Adquisiciones, Calidad, Permisos, Costos, Hitos, Comunicaciones, Talleres, Documental). |

### SIC 15: OPERACIONES

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **15. OPERACIONES** | Evaluación del impacto sobre el plan de operaciones existente. |
| 15.2 Resumen del capítulo | Conclusión sobre si el proyecto contempla o no **cambios al plan de operaciones** o requerimientos adicionales, ya que solo es un reemplazo de activos auxiliares (si aplica). |
| **ÍNDICE DE FIGURAS** | Figuras 151, 152, 153: Emplazamiento Geográfico y activos. |
| **ÍNDICE DE TABLAS** | Tabla 151: Condiciones geográficas y ambientales generales del sitio. |

### SIC 16: COSTOS DE CAPITAL (CAPEX)

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **16. COSTOS DE CAPITAL** | Estimación detallada del CAPEX (Clase 3) y su estructura. |
| 16.2 Base de Estimación | **Definición de la Base (Clase 3, Archivos Excel).** Fecha Base y Tasas de Cambio de Divisas (Tabla 162/163). **Definición de Costos:** Costos Directos (Suministros, Gastos Generales, Utilidades) e Indirectos (Ingeniería, Servicios, Dueño). |
| 16.3 CAPEX resumen | **Tabla 164: Resumen Costos de Capital.** Total USD y % Incidencia por Disciplina (e.g., Adquisiciones 31.20%, Construcción 7.51%). |
| 16.4 Estructura de Quiebre del Proyecto | **Tabla 165: Estructura de Quiebre (WBS).** WBS por niveles (Nivel 1 al 5), incluyendo la codificación de áreas (e.g., 06515 Subestación Media Tensión) y descripción de cada nivel. |
| 16.5 Costos del Dueño, Preproducción y Puesta en Marcha | **Resumen Costos del Dueño** (Tabla 166). Desglose por HH/Staff y equipos por ítem (e.g., Jefe de Proyecto, ITO, Apoyo Especializado). |
| 16.8 Contingencia y Precisión | **Tabla 1611: Valor Contingencia.** Contingencia Base y Operacional (e.g., 20% Total). Justificación de la Contingencia (riesgo, constructibilidad, informes de visita a terreno). |
| 16.9 Proyección del Flujo de Caja | Detalle del Flujo de Caja anualizado por ITEM (Adquisición, Construcción, Servicio Eliminación de Residuos, Costos Indirectos). |
| 16.11 Validación de la Estimación de Costos de Capital | Responsabilidades (Equipo de Estimación, Revisores, Aprobación) y metodología de revisión. |
| **ANEXOS** | ANEXO A: Cálculo de Contingencia (Gráfico de Tornado). ANEXO B: CAPEX detallado. ANEXO C/D: Informe Visita a Terreno/Constructibilidad. |
| **ÍNDICE DE FIGURAS** | Figuras 161, 162, 163: Emplazamiento Geográfico y activos. Figura 01: Gráfico de Tornado (Cálculo de Contingencia). |
| **ÍNDICE DE TABLAS** | Tablas 162/163: Moneda Base (e.g., 2024), Tasas de Cambio e Indicadores Financieros. Tablas 164: Resumen Costos de Capital. Tablas 165: Estructura de Quiebre (WBS). Tablas 166 a 1610: Desglose de Costos del Dueño (e.g., ITO, Administración Interna). Tabla 1611: Valor Contingencia. |

### SIC 17: COSTOS DE OPERACIÓN (OPEX)

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **17. COSTOS DE OPERACIÓN** | Proyección del costo para el funcionamiento y mantenimiento de los equipos instalados. |
| 17.2 Resumen del Capítulo | Distribución de gastos operacionales (Mano de Obra y Repuestos) para 10 años (Tabla 172). |
| 17.3 Base de Estimación | **Base de Estimación (Clase 3).** Estándares y Procedimientos DCH (Tabla 173). Grado de Definición de la Información (Tabla 174). Moneda Base y Factores de Corrección. **Definición de Costos:** Costos Fijos (Mano de Obra) y Variables (Consumibles, Repuestos). |
| Estructura de Quiebre Organizacional | Clasificación de Gastos (Mano de Obra, Generales, Consumibles, Electricidad, Combustible, Mantenimiento) y justificación de **No Aplica** (si corresponde). |
| Mantenimiento de Infraestructura y Servicios | **Plan de Mantenibilidad:** Matriz de Mantenimiento por Activo (e.g., 100 kV, 13,8 kV) con Frecuencia, HH/Año y Total HH (Tablas 179/1710). **Costos Mano de Obra:** Costo total (USD/Año) de personal directo/indirecto para mantenimiento (Tablas 1711/1712). **Repuestos:** Listado y costo de Repuestos e Insumos de Mantenimiento (Tablas 1713/1714). |
| 17.5 Costos de Puesta en Marcha y Ramp-Up | Declaración de **no se consideran costos asociados a ramp-up** (si aplica). **Tabla 1715:** Costos para la Operación del Primer Año Completo. |
| 17.7 Precisión | Clase 3 (e.g., $\pm 5$ a $10 \%$ ) y cumplimiento del Estándar SIC-P-005. |
| 17.8 Revisión de la Estimación de Costos de Operación | Matriz de Responsabilidades de Revisión (Equipo de Estimación, Revisores, Aprobación). |
| **ANEXOS** | ANEXO A: Estimación OPEX. ANEXO B: Informe OPEX. |
| **ÍNDICE DE FIGURAS** | Figuras 171, 172, 173: Emplazamiento Geográfico y activos. Figura 174: Costos Operacionales Anuales (Gráfico comparativo MO vs Repuestos). Figura 175: Metodología de Trabajo. |
| **ÍNDICE DE TABLAS** | Tablas 172 a 1715 (OPEX, Procedimientos, Definición de Estimación Clase 3, Moneda Base, Mantenimiento, Costos M.O., Repuestos, Costos Primer Año). |

### SIC 18: PRODUCTOS

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **18. PRODUCTOS** | Evaluación del impacto en los tipos de productos y cantidades producidas. |
| 18.2 Resumen del capítulo | Declaración de que el capítulo **no fue desarrollado/no aplica** porque el proyecto no genera variaciones en los tipos de productos ni en las cantidades producidas (si aplica). |
| 18.3 Especificación del Producto | Declaración de **no desarrollado** (si aplica). |
| 18.4 Proyección de la Demanda | Declaración de **no desarrollado** (si aplica). |
| 18.5 Proyecciones de la Oferta | Declaración de **no desarrollado** (si aplica). |
| 18.6 Despacho, Almacenamiento y Distribución del Producto | Declaración de **no desarrollado** (si aplica). |
| **ÍNDICE DE FIGURAS** | Figuras 181, 182, 183: Emplazamiento Geográfico y activos. |
| **ÍNDICE DE TABLAS** | Tabla 181: Condiciones geográficas y ambientales generales del sitio. |

### SIC 19: PROPIEDAD Y ASPECTOS LEGALES

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **PROPIEDAD Y ASPECTOS LEGALES** | Evaluación de las necesidades de adquisición de terrenos, servidumbres y propiedad intelectual. |
| Resumen | Descripción del problema (e.g., cumplimiento normativo) y alcance del proyecto. |
| Acuerdos Finales de Compras de Tierra u otras necesidades del proyecto | Declaración de **no requerir acordar compras de terreno** o servidumbres (si aplica) y justificación (e.g., se ubica en instalaciones existentes con servidumbre del Dueño). |
| Tecnología del proyecto | Declaración de si hay acuerdos sobre tecnología/propiedad intelectual (si aplica). |
| **ANEXOS** | ANEXO 1. INFORME DE APLICACIÓN DE NORMA NCC24 V4. |
| **ÍNDICE DE FIGURAS** | Ilustraciones 19-1, 19-2, 19-3: Emplazamiento Geográfico y activos. |
| **ÍNDICE DE TABLAS** | Tabla 19-1: Condiciones geográficas y ambientales generales del sitio. |

### SIC 20: ACUERDOS COMERCIALES

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Generalizado) |
| :--- | :--- |
| **20. ACUERDOS COMERCIALES** | Evaluación de la necesidad de Joint Ventures, Asociaciones o Gestión Territorial. |
| 20.2 Resumen Capítulo | Declaración de **no aplica** (si corresponde), ya que la naturaleza del proyecto no tiene efectos sobre aspectos comerciales. |
| 20.3 Asociaciones (Joint Ventures) | Declaración de **no ser necesaria** la firma de acuerdos comerciales, asociaciones o joint ventures (si aplica). |
| 20.4 Gestión Territorial | Plan de acción para el retiro y traslado de activos/residuos fuera de las instalaciones (e.g., almacenamiento temporal autorizado externo). |
| 20.5 Propiedad Intelectual | Declaración de **no aplicar** diseños a tecnologías propias que requieran gestión de propiedad intelectual. |
| **ÍNDICE DE FIGURAS** | Figuras 201, 202, 203: Emplazamiento Geográfico y activos. |
| **ÍNDICE DE TABLAS** | Tabla 201: Condiciones geográficas y ambientales generales del sitio. |

### SIC 21: ANEXO FINANCIERO DETALLE

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Genérico) |
| :--- | :--- |
| **21. ANEXO FINANCIERO DETALLE** | **Documento de respaldo del SIC 16.** Incluye la información de cálculo completa y detallada de costos e indicadores. |
| 21.1 Flujo de Caja Proyectado | Flujo de Caja detallado y anualizado por ítem (e.g., Adquisición, Construcción, Servicios Indirectos), sensibilidad y proyecciones. |
| 21.2 Indicadores de Valoración | Cálculo detallado de **VAN** (Valor Actual Neto), **TIR** (Tasa Interna de Retorno) y **Payback** (si aplica). |
| 21.3 Análisis de Sensibilidad | Evaluación del impacto de las variables de riesgo (e.g., variaciones en el CAPEX por la ETP) en la viabilidad económica del proyecto (e.g., Gráfico de Tornado). |
| **ÍNDICE DE FIGURAS** | Figura 211: Gráfico de Flujo de Caja (Curvas S). Figura 212: Gráfico de Tornado (Análisis de Riesgo). |
| **ÍNDICE DE TABLAS** | Tablas de cálculo de CAPEX, OPEX, Flujos de Caja y Reservas de Contingencia. |

### SIC 22: ANEXO TÉCNICO DETALLE

| ÍNDICE GENERAL | CONTENIDO REQUERIDO (Genérico) |
| :--- | :--- |
| **22. ANEXO TÉCNICO DETALLE** | **Documento de respaldo del SIC 14 y SIC 11.** Incluye la información de ingeniería y constructibilidad completa y detallada. |
| 22.1 Especificaciones Técnicas de Equipos | Especificaciones detalladas de **Equipos Críticos** (e.g., Activos, Maquinaria, Componentes Electromecánicos) incluyendo sus parámetros (e.g., tensión, capacidad, altura de diseño). |
| 22.2 Planos y Diagramas de Ingeniería | Referencia a los planos clave del proyecto (e.g., Diagramas Unifilares, Lay-outs, Planos AS-BUILT). |
| 22.3 Informes de Constructibilidad y Levantamiento | Informes de soporte al PEP (SIC 14) que detallan las Interferencias y la Secuencia Constructiva específica por ubicación. |
| 22.4 WBS Detallada (Nivel 4/5/6) | Detalle de la Estructura de Desglose de Trabajo (WBS) hasta el nivel de Actividad/Paquete de Trabajo para la ejecución. |
| **ÍNDICE DE FIGURAS** | Figura 221: Diagrama de WBS detallado. Figura 222: Planos de Ubicación (Lay-outs) por área de intervención. |
| **ÍNDICE DE TABLAS** | Tabla 221: Matriz de Adquisiciones Detallada. Tabla 222: Listado de Tie-ins Eléctricos/Conexiones. |
