# 📋 ESPECIFICACIÓN TÉCNICA DETALLADA - BACKEND MAAS v4.0

## 🏗️ ARQUITECTURA GENERAL

### Modelo Holónico Multi-Agente

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTIM (Agent Runtime)                   │
│                    Powered by: AgentOS + Agno               │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    ┌──────────────────┐
                    │  Context Broker  │ (Single Source of Truth)
                    ├──────────────────┤
                    │ • Project KB     │
                    │ • Rules KB       │
                    │ • Session DB     │
                    └──────────────────┘
                              ↓
        ┌─────────────────────┬──────────────────┬──────────────────┐
        ↓                     ↓                  ↓                  ↓
   GenericData      MetricExtractor        Author             Judge
   Agent            Agent                  Agent              Agent
   (Extraction)     (Transformation)       (Creation)         (Review)
        ↓                     ↓                  ↓                  ↓
    FASE 1              FASE 2               FASE 3             FASE 4
   (Redmine)         (Pydantic)          (Markdown)          (Audit)
```

---

## 🔧 COMPONENTES PRINCIPALES

### 1. PUNTO DE ENTRADA: `backend/main.py`

**Responsabilidad**: Inicialización del sistema y orquestación de agentes

**Flujo de Ejecución**:
```
main.py
├── 1. Load environment variables (.env)
│
├── 2. Initialize Context Broker
│   └── Conexión a PostgreSQL (3 bases de datos)
│
├── 3. Initialize Language Model
│   └── OpenAI GPT-4o (via API)
│
├── 4. Instantiate Agents (6 total)
│   ├── GenericDataAgent (Extracción)
│   ├── MetricExtractorAgent (Transformación)
│   ├── GeneralAuthorAgent (Redacción)
│   ├── ExpertJudgeAgent (Auditoría)
│   ├── MasterPlannerAgent (Planificación)
│   └── DependencyManagerAgent (Gestión de dependencias)
│
├── 5. Create Teams (Agentes colaborativos)
│   └── doc_team: [MetricExtractor, Author, Judge]
│
├── 6. Create Workflows
│   └── DocumentCreationWorkflow
│
├── 7. Setup AgentOS Runtime
│   └── Lifespan: Load rules on startup
│
├── 8. Register Endpoints
│   ├── GET /health (Health check)
│   └── POST /preinversion-plans (Main workflow)
│
└── 9. Start Uvicorn Server (localhost:7777)
```

**Configuraciones Críticas**:
- `authorization_enabled=False` (Development mode)
- `os_security_key=None` (No OS key requirement)
- `reload=False` (Para procesos background)
- `CORS_ALLOWED_ORIGINS=["http://localhost:3001"]`

---

### 2. NÚCLEO: `backend/core/context_broker.py`

**Responsabilidad**: Gestionar todas las bases de datos y conocimiento

**Arquitectura de Datos**:
```
Context Broker
├── Session DB (PostgreSQL table: maas_sessions)
│   └── Almacena: sesiones, historial, metadata
│
├── Project KB (Knowledge Base: project_knowledge)
│   └── Almacena: datos dinámicos, hechos del proyecto
│   └── Search: Hybrid (vector + keyword)
│
└── Rules KB (Knowledge Base: business_rules)
    ├── Almacena: Plantillas SIC (01-22)
    ├── Almacena: Normas CODELCO (NCC24, SGPD)
    └── Search: Hybrid (vector + keyword)
```

**Métodos Principales**:

1. **`load_rules()` (async)**
   - Ejecuta al startup
   - Carga plantillas SIC desde `/backend/knowledge/templates/`
   - Carga normas desde `/backend/knowledge/rules_ncc24.txt`
   - Vector embedding con OpenAI text-embedding-3-small

2. **`get_rules(query)`**
   - Busca reglas de negocio relevantes
   - Retorna TOP 5 resultados ordenados por relevancia

3. **`get_project_context(query, project_id)`**
   - Busca hechos del proyecto específico
   - Filtra por project_id para aislamiento de datos

4. **`publish_finding(findings, project_id)`**
   - Permite que agentes publiquen nuevos hallazgos
   - Integra información en project_kb

---

### 3. HERRAMIENTAS: `backend/tools/custom_tools.py`

**Toolkit 1: RedmineTools** (CRÍTICO)
```
RedmineTools
├── get_issue_details(issue_id)
│   └── Obtiene detalles completos del issue
│   └── Incluye: ID, subject, description, status, proyecto, campos custom
│
├── list_projects()
│   └── Lista todos los proyectos en Redmine
│
├── search_issues(project_id, query)
│   └── Busca issues por criterios
│
├── get_project_issues(project_id)
│   └── Obtiene todos los issues de un proyecto
│
├── analyze_issue_context(issue_id)
│   └── Analiza contexto: descripción, relaciones, cambios
│
├── get_issue_relations(issue_id)
│   └── Obtiene dependencias: bloqueadores, relacionados
│
├── extract_issue_requirements(issue_id)
│   └── Extrae requisitos técnicos
│
└── update_issue_metadata(issue_id, metadata)
    └── Actualiza campos custom de issue
```

**Toolkit 2: RedmineKnowledgeTools**
```
Búsqueda avanzada en Redmine + Knowledge Base
├── search_similar_issues(description, project_id)
│   └── Busca issues similares en histórico
│
├── analyze_issue_patterns(project_id)
│   └── Identifica patrones en issues previos
│
└── find_best_practices(category)
    └── Busca mejores prácticas documentadas
```

**Toolkit 3: RedmineReasoningTools**
```
Análisis de dependencias e impacto
├── analyze_dependencies(issue_id)
│   └── Mapea todas las dependencias
│
├── evaluate_impact(changes)
│   └── Evalúa impacto de cambios
│
└── identify_blockers(issue_id)
    └── Identifica bloqueadores críticos
```

**Toolkit 4: SourceTextTools**
```
Extracción de evidencia con citas
├── extract_text_segments(source, query)
│   └── Extrae fragmentos exactos
│
└── cite_source(content, source_id)
    └── Genera citas formales
```

**Toolkit 5: ReasoningTools** (Agno built-in)
```
Razonamiento y planificación
├── Think step-by-step
├── Plan execution
└── Structure output
```

**Toolkit 6: KnowledgeTools** (Agno built-in)
```
Acceso a Knowledge Bases
├── search_knowledge()
└── retrieve_documents()
```

---

### 4. AGENTES: `backend/agents/`

#### **4.1 GenericDataAgent** (`generic_data_agent.py`)

**Rol**: Holón de Extracción - Adquisición de datos brutos

**Entrada**: project_id (ID de Redmine)

**Salida**: Datos estructurados + contexto del proyecto

**Flujo de 5 Fases**:
```
FASE 1: PLANNING
  └─ Define qué datos extraer del proyecto
     └─ Consulta project_kb para hechos previos

FASE 2: REDMINE ACQUISITION
  └─ Usa RedmineTools para obtener:
     ├── list_projects()
     ├── get_project_issues()
     ├── get_issue_details()
     ├── get_issue_relations()
     └── analyze_issue_context()

FASE 3: KNOWLEDGE SEARCH
  └─ Usa RedmineKnowledgeTools para:
     ├── search_similar_issues()
     └── analyze_issue_patterns()

FASE 4: ANALYSIS & STRUCTURING
  └─ Usa ReasoningTools para:
     ├── Analizar relaciones
     └── Estructurar jerárquicamente

FASE 5: SYNTHESIS
  └─ Retorna resumen de proyecto con:
     ├── Proyectos y issues clave
     ├── Relaciones y dependencias
     ├── Riesgos identificados
     └── Bloqueadores críticos
```

**Herramientas Asignadas**:
- RedmineTools (Extracción directa)
- RedmineKnowledgeTools (Búsqueda de patrones)
- ReasoningTools (Análisis lógico)
- KnowledgeTools (Acceso a KB)

**Knowledge Base**: `broker.project_kb`

**Scoring de Confianza**: 
- ALTA: Datos de campos estructurados
- MEDIA: Inferidos de relaciones
- BAJA: Estimados o parciales

---

#### **4.2 MetricExtractorAgent** (`metric_extractor_agent.py`)

**Rol**: Holón de Extracción - Transformación a métricas validadas

**Entrada**: Datos brutos del GenericDataAgent

**Salida**: Objetos Pydantic validados (SIC14, SIC16, SIC03, etc.)

**Flujo de 6 Fases**:
```
FASE 1: SEARCH KNOWLEDGE
  └─ Consulta rules_kb para:
     ├── Esquemas de métricas
     ├── Validaciones y restricciones
     └── Fórmulas de cálculo

FASE 2: ANALYZE REDMINE
  └─ **Usa RedmineTools directamente**: ✨ NUEVO
     ├── Obtiene datos frescos
     ├── Extrae custom fields
     └── Analiza cambios históricos

FASE 3: STRUCTURING
  └─ Mapea datos Redmine a Pydantic:
     ├── Conversión de tipos
     ├── Cálculo de campos derivados
     └── Aplicación de transformaciones

FASE 4: EVIDENCE EXTRACTION
  └─ Usa SourceTextTools para:
     ├── Extraer fragmentos exactos
     ├── Generar citas formales
     └── Documentar fuentes

FASE 5: VALIDATION
  └─ Valida conformidad:
     ├── Tipos de datos correctos
     ├── Campos obligatorios presentes
     ├── Restricciones min/max
     └── Integridad referencial

FASE 6: SYNTHESIS
  └─ Retorna:
     ├── Objeto Pydantic validado
     ├── Metadata: source, timestamp, confidence
     └── Citas de evidencia
```

**Herramientas Asignadas**:
- **RedmineTools** (CRÍTICO - faltaba en v1)
- RedmineReasoningTools (Análisis de impacto)
- SourceTextTools (Extracción de evidencia)
- ReasoningTools (Estructuración compleja)
- KnowledgeTools (Acceso a esquemas)

**Knowledge Base**: `broker.rules_kb`

**Schemas Soportados**:
- SIC14Plazo (Cronograma)
- SIC16Capex (Capex)
- SIC03Riesgo (Riesgos)
- (Extensible a más SIC)

---

#### **4.3 GeneralAuthorAgent** (`author_agent.py`)

**Rol**: Holón de Creación - Redacción de documentos técnicos

**Entrada**: Métricas validadas + datos del proyecto

**Salida**: Documento markdown completo (SIC)

**Flujo de 5 Fases**:
```
FASE 1: SEARCH TEMPLATES
  └─ Consulta rules_kb para:
     ├── Plantillas SIC (01-22)
     ├── Mejores prácticas
     └── Estilos de redacción

FASE 2: PLANNING
  └─ Planifica estructura:
     ├── Mapea datos a secciones SIC
     ├── Identifica dependencias
     └── Ordena secciones lógicamente

FASE 3: WRITING
  └─ Redacta secciones:
     ├── Sustituye placeholders
     ├── Aplica guías de estilo
     └── Mantiene coherencia

FASE 4: VALIDATION
  └─ Valida coherencia:
     ├── Referencias cruzadas
     ├── Consistencia de datos
     └── Gramática y formato

FASE 5: SYNTHESIS
  └─ Retorna:
     ├── Documento markdown completo
     ├── Índice de contenidos
     └── Referencias a issues
```

**Herramientas Asignadas**:
- RedmineKnowledgeTools (Búsqueda de mejores prácticas)
- ReasoningTools (Planificación estructural)
- KnowledgeTools (Acceso a plantillas SIC)

**Knowledge Base**: `broker.rules_kb` (Plantillas SIC 01-22)

**Plantillas SIC Documentadas**:
- **SIC_01**: Resumen y Recomendaciones
- **SIC_02**: Caso de Negocio
- **SIC_03**: Riesgos
- **SIC_04**: Seguridad y Salud
- **SIC_05**: Medio Ambiente
- **SIC_07**: Geología
- **SIC_08**: Hidrología
- **SIC_09**: Ingeniería Básica
- **SIC_10**: Residuos
- **SIC_12**: Mantenimiento
- **SIC_13**: TI
- **SIC_14**: Cronograma (Plazo)
- **SIC_15**: Cronograma detallado
- **SIC_16**: CAPEX
- **SIC_17**: OPEX
- **SIC_18**: Productos
- **SIC_19**: Legal
- **SIC_20**: Comercial
- **SIC_21**: Evaluación
- **SIC_22**: Avance

---

#### **4.4 ExpertJudgeAgent** (`judge_agent.py`)

**Rol**: Holón de Creación - Auditoría y validación

**Entrada**: Documento completado + datos del proyecto

**Salida**: Reporte de auditoría + scoring de cumplimiento

**Flujo de 6 Fases**:
```
FASE 1: ANALYZE CONTENT
  └─ Revisa estructura del documento:
     ├── Secciones presentes
     ├── Completitud de contenido
     └── Calidad de evidencia

FASE 2: CHECK RULES
  └─ Valida contra normas CODELCO:
     ├── NCC24 (Normas de Coordinación)
     ├── SGPD (Sistema de Gestión)
     └── Políticas internas

FASE 3: EVALUATE IMPACT
  └─ Usa RedmineReasoningTools para:
     ├── Evaluar dependencias
     ├── Identificar riesgos
     └── Analizar bloqueadores

FASE 4: SCORING
  └─ Calcula puntaje por categoría:
     ├── Categoría A: Completitud (30%)
     ├── Categoría B: Normas (40%)
     ├── Categoría C: Evidencia (20%)
     ├── Categoría D: Riesgos (10%)
     └── TOTAL: 0-100

FASE 5: SYNTHESIS
  └─ Genera hallazgos:
     ├── Lista incumplimientos
     ├── Prioriza por severidad
     └── Calcula impacto

FASE 6: REPORT
  └─ Retorna:
     ├── Puntaje final (0-100)
     ├── Estado: PASS/REVIEW/FAIL
     ├── Recomendaciones
     └── Acciones correctivas
```

**Scoring System**:
```
Puntaje → Estado → Acción
≥ 70    → PASS  → Aprobado
50-69   → REVIEW → Requiere cambios
< 50    → FAIL  → Rechazado, cambios obligatorios
```

**Clasificación de Riesgos**:
- CRÍTICO: Bloquea aprobación
- ALTO: Requiere modificación
- MEDIO: Recomendado revisar
- BAJO: Informativo

**Herramientas Asignadas**:
- RedmineReasoningTools (Análisis de impacto)
- ReasoningTools (Razonamiento profundo)
- KnowledgeTools (Acceso a normas)

**Knowledge Base**: `broker.rules_kb` (NCC24, SGPD, policies)

---

#### **4.5 MasterPlannerAgent** (`planner_agent.py`)

**Rol**: Holón de Planificación - Generación dinámica de estrategias

**Entrada**: Tipo de documento + metadata del proyecto

**Salida**: Plan de estructura (DAG de secciones)

**Responsabilidades**:
- Consulta plantillas del Knowledge Base
- Construye grafo de dependencias (DAG)
- Asigna prioridades
- Planifica orden de ejecución

**Modelo de LLM**: o3-mini (razonamiento avanzado)

**Novedades v5.0**:
- **Lectura Dinámica**: Extrae el DAG directamente de `PLANTILLA_MAESTRA_SIC_GENERICO.md`.
- **SGP-LA**: Evalúa lecciones aprendidas al inicio.

---

#### **4.6 DependencyManagerAgent** (`planner_agent.py`)

**Rol**: Holón de Planificación - Gestión de dependencias

**Entrada**: Estructura de proyecto + reglas de negocio

**Salida**: Grafo de dependencias resuelto

**Responsabilidades**:
- Mapea dependencias entre secciones
- Identifica ciclos
- Calcula orden topológico
- Maneja conflictos de dependencias

---

### 5. SCHEMAS: `backend/agents/schemas.py`

**Pydantic Models** para validación de datos:

```python
# Ejemplo: Cronograma (SIC14)
class SIC14Plazo(BaseModel):
    """Cronograma de ejecución del proyecto"""
    proyecto_id: int
    fecha_inicio: date
    fecha_fin: date
    duracion_meses: int
    fases: List[Fase]
    hitos_criticos: List[str]
    buffer_contingencia_pct: float
    
    class Config:
        validate_assignment = True

# Ejemplo: CAPEX (SIC16)
class SIC16Capex(BaseModel):
    """Capital Expenditure planning"""
    items_capex: List[ItemCapex]
    total_capex_usd: float
    contingencia_pct: float
    financiamiento: str
    
    class Config:
        validate_assignment = True

# Ejemplo: Riesgos (SIC03)
class SIC03Riesgo(BaseModel):
    """Risk assessment"""
    riesgos: List[Riesgo]
    riesgo_total_score: float
    estrategias_mitigacion: List[str]
    
    class Config:
        validate_assignment = True
```

---

### 6. WORKFLOWS: `backend/workflows/document_workflow.py`

**Orquestación de agentes colaborativos**:

```
DocumentCreationWorkflow
├── Entrada: project_id, document_type
│
├── ETAPA 1: Planning
│   └── MasterPlanner generaDAG de secciones
│
├── ETAPA 2: Extraction
│   └── GenericDataAgent obtiene datos de Redmine
│
├── ETAPA 3: Transformation
│   └── MetricExtractorAgent valida y estructura
│
├── ETAPA 4: Creation
│   └── Team (Author + Judge) redacta y revisa
│       ├── Author redacta
│       ├── Judge revisa
│       └── Si FAIL → vuelve a Author (iteración)
│
└── Salida: Documento validado + reporte de auditoría
```

---

### 7. ENDPOINTS: FastAPI

#### **GET /health**
```
Propósito: Health check para monitoreo
Parámetros: Ninguno
Respuesta: {"status": "ok", "instantiated_at": timestamp}
Latencia esperada: <50ms
```

#### **POST /preinversion-plans**
```
Propósito: Generar plan de preinversión completo

Parámetros (JSON):
  - project_id: int (ID de proyecto en Redmine)
  - document_type: str (default="SIC")

Flujo Ejecutado:
  1. GenericDataAgent: Extrae datos
  2. MetricExtractorAgent: Transforma a métricas
  3. GeneralAuthorAgent: Redacta documento
  4. ExpertJudgeAgent: Valida y audita

Respuesta:
  {
    "status": "success|error",
    "project_id": int,
    "document_type": str,
    "phases": {
      "data_extraction": "...",
      "metric_transformation": "...",
      "document_authoring": "...",
      "quality_validation": "..."
    },
    "full_document": "# Documento completo...",
    "audit_report": "Reporte de auditoría...",
    "message": "Plan generado exitosamente"
  }

Latencia esperada: 30-60 segundos (procesamiento de agentes)
```

---

### 8. BASE DE DATOS: PostgreSQL

**Tablas Principales**:

```sql
-- Session Management
maas_sessions (
  id UUID PRIMARY KEY,
  project_id INT,
  created_at TIMESTAMP,
  data JSONB
)

-- Project Knowledge
project_knowledge (
  id UUID PRIMARY KEY,
  project_id INT,
  content TEXT,
  embedding VECTOR(1536),  -- OpenAI embeddings
  source VARCHAR,
  created_at TIMESTAMP
)

-- Business Rules
business_rules (
  id UUID PRIMARY KEY,
  content TEXT,
  source VARCHAR (templates/rules_ncc24.txt),
  category VARCHAR (SIC01, SIC02, ..., NCC24, SGPD),
  embedding VECTOR(1536),
  created_at TIMESTAMP
)

-- Audit Trail
audit_logs (
  id UUID PRIMARY KEY,
  agent_id VARCHAR,
  action VARCHAR,
  project_id INT,
  timestamp TIMESTAMP,
  result JSONB
)
```

---

## 🔄 FLUJOS DE DATOS COMPLETOS

### Flujo 1: POST /preinversion-plans

```
Usuario (Frontend)
        ↓
    HTTP POST
    /preinversion-plans
    {project_id: 1, document_type: "SIC"}
        ↓
┌─────────────────────────────────────┐
│ endpoint: generate_preinversion_plan │
└─────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────────┐
│ FASE 1: GenericDataAgent.run()               │
│ "Extrae datos del proyecto 1 en Redmine..."  │
└──────────────────────────────────────────────┘
    ├─ Usa: RedmineTools
    │  └─ list_projects()
    │  └─ get_project_issues()
    │  └─ get_issue_details()
    │  └─ get_issue_relations()
    │
    ├─ Usa: RedmineKnowledgeTools
    │  └─ search_similar_issues()
    │
    └─ Retorna: Datos brutos + contexto
        ↓
┌──────────────────────────────────────────────┐
│ FASE 2: MetricExtractorAgent.run()           │
│ "Transforma datos a métricas Pydantic..."    │
└──────────────────────────────────────────────┘
    ├─ Consulta: rules_kb para esquemas
    │
    ├─ Usa: RedmineTools (obtiene datos frescos)
    │
    ├─ Transforma: data → SIC14, SIC16, SIC03...
    │
    ├─ Valida: Pydantic validation
    │
    └─ Retorna: Objetos Pydantic validados
        ↓
┌──────────────────────────────────────────────┐
│ FASE 3: GeneralAuthorAgent.run()             │
│ "Redacta documento SIC completo..."          │
└──────────────────────────────────────────────┘
    ├─ Consulta: rules_kb para plantillas SIC
    │
    ├─ Planifica: Estructura de documento
    │
    ├─ Redacta: Cada sección SIC
    │  ├─ SIC_01: Resumen y Recomendaciones
    │  ├─ SIC_02: Caso de Negocio
    │  ├─ SIC_03: Riesgos
    │  ├─ ... (20 más)
    │  └─ SIC_22: Avance
    │
    └─ Retorna: Documento markdown completo
        ↓
┌──────────────────────────────────────────────┐
│ FASE 4: ExpertJudgeAgent.run()               │
│ "Valida cumplimiento normativo..."           │
└──────────────────────────────────────────────┘
    ├─ Analiza: Estructura y completitud
    │
    ├─ Valida: Contra normas CODELCO
    │  ├─ NCC24
    │  ├─ SGPD
    │  └─ Políticas internas
    │
    ├─ Evalúa: Riesgos e impacto
    │
    ├─ Calcula: Scoring (0-100)
    │
    └─ Retorna: Reporte + clasificación (PASS/REVIEW/FAIL)
        ↓
┌──────────────────────────────────────────────┐
│ Respuesta HTTP 200/400                       │
│ {status, document, audit_report}             │
└──────────────────────────────────────────────┘
        ↓
    Usuario (Frontend)
```

### Flujo 2: Context Broker durante startup

```
Backend startup
        ↓
main.py
    ├─ broker = ContextBroker(...)
    │  └─ Inicia 3 Knowledge Bases
    │
    ├─ Crea 6 agentes (todos reciben broker)
    │
    ├─ agent_os.lifespan (async)
    │  └─ await broker.load_rules()
    │
    └─ broker.load_rules()
        └─ Lee /backend/knowledge/templates/
            ├─ SIC_01.md → vectoriza → almacena en rules_kb
            ├─ SIC_02.md → vectoriza → almacena en rules_kb
            ├─ ... (22 plantillas)
            └─ rules_ncc24.txt → vectoriza → almacena en rules_kb
        
        └─ result: 22+ documentos indexados en PostgreSQL
                   con embeddings vectoriales (pgvector)
```

---

## 📊 RELACIONES ENTRE ARCHIVOS

```
main.py (Punto de entrada)
    ↓
    ├─→ context_broker.py (Fuente única de verdad)
    │       ├─→ PostgreSQL (3 Knowledge Bases)
    │       └─→ OpenAI Embeddings
    │
    ├─→ agents/ (6 agentes especializados)
    │   ├─→ generic_data_agent.py (Extracción)
    │   │   └─→ tools/custom_tools.py (RedmineTools, ...)
    │   │
    │   ├─→ metric_extractor_agent.py (Transformación)
    │   │   └─→ tools/custom_tools.py (RedmineTools, SourceTextTools, ...)
    │   │   └─→ agents/schemas.py (Pydantic validation)
    │   │
    │   ├─→ author_agent.py (Redacción)
    │   │   └─→ tools/custom_tools.py (RedmineKnowledgeTools, ...)
    │   │
    │   ├─→ judge_agent.py (Auditoría)
    │   │   └─→ tools/custom_tools.py (RedmineReasoningTools, ...)
    │   │
    │   ├─→ planner_agent.py (Planificación)
    │   │   └─→ agents/schemas.py (DocumentPlan)
    │   │
    │   └─→ extractor_agent.py (Ingesta asíncrona)
    │
    ├─→ workflows/ (Orquestación)
    │   └─→ document_workflow.py (Coordinación de agentes)
    │
    ├─→ tools/ (Herramientas compartidas)
    │   └─→ custom_tools.py (6 toolkits)
    │
    └─→ knowledge/ (Contenido estático)
        ├─→ templates/ (SIC_01.md ... SIC_22.md)
        └─→ rules_ncc24.txt (Normas CODELCO)
```

---

## 🔐 FLUJOS DE AUTORIZACIÓN

**Modelo Actual**: Deshabilitado (Development)
```
Authorization: FALSE
OS_SECURITY_KEY: NULL
```

**Modelo de Producción** (Future):
```
Authorization: TRUE
JWT Token Required

Scopes:
├─ agents:read (Consultar agentes)
├─ agents:run (Ejecutar agentes)
├─ sessions:read (Ver sesiones)
└─ sessions:write (Crear sesiones)
```

---

## 🚀 DIAGRAMA DE SECUENCIA: Generación de Preinversión

```
Usuario        Endpoint        GenericData      MetricExtractor      Author          Judge
  │                │                │                 │               │               │
  │─POST──────────→│                │                 │               │               │
  │  /preinversion │                │                 │               │               │
  │   {project_id} │                │                 │               │               │
  │                │                │                 │               │               │
  │                │───"Extrae datos"──→│              │               │               │
  │                │                │    │ (Redmine)  │               │               │
  │                │                │←────"Datos brutos"              │               │
  │                │                                 │               │               │
  │                │────"Transforma"───────────────→│               │               │
  │                │                │               │  │ (Pydantic)│               │
  │                │                │               │←──"Métricas"  │               │
  │                │                │               │               │               │
  │                │────"Redacta"─────────────────────────────────→│               │
  │                │                │               │               │  │ (Markdown)│
  │                │                │               │               │←──"Documento"
  │                │                │               │               │               │
  │                │────"Audita"────────────────────────────────────────────────→│
  │                │                │               │               │               │  
  │                │                │               │               │               │ (Scoring)
  │                │                │               │               │               │
  │                │←──────────────────────────────────────────────────"Reporte"──│
  │                │
  │←──JSON─────────│
     {document,
      audit_report,
      status}
```

---

## 📝 CONFIGURACIÓN REQUERIDA

**`.env` archivo necesario**:
```bash
# Database
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/maas

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1

# Redmine
REDMINE_BASE_URL=http://cidiia.uce.edu.do/
REDMINE_API_KEY=...

# Backend
BACKEND_PORT=7777
BACKEND_HOST=0.0.0.0

# Frontend
FRONTEND_URL=http://localhost:3001
```

---

## ✅ CHECKLIST DE VALIDACIÓN

```
✓ Backend levantado en localhost:7777
✓ PostgreSQL conectado (3 Knowledge Bases)
✓ OpenAI API funcional
✓ Plantillas SIC (01-22) indexadas
✓ Normas CODELCO (NCC24) indexadas
✓ 6 agentes instanciables (o3-mini habilitado para Planner)
✓ Team colaborativo creado (Holón v5.0)
✓ Workflow de documentos disponible (Maker-Checker 5 retries)
✓ GET /health responde
✓ POST /preinversion-plans disponible (v5.0 Hardening)
✓ Tracing enabled (OpenTelemetry)
✓ Background Hooks (Async PDF)
```

---

## 📚 REFERENCIAS

- **Framework**: Agno + AgentOS
- **LLM**: OpenAI GPT-4o
- **Database**: PostgreSQL + pgvector
- **Vector Search**: Hybrid (keyword + semantic)
- **API**: FastAPI + Uvicorn
- **Validación**: Pydantic v2

---

**Versión**: 5.0 - AgentOS v5.0 Hardened Architecture  
**Fecha**: 5 enero 2026  
**Estado**: ✅ Hardened & Auditoría v5.0 Completa
