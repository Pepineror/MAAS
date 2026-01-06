# 🎯 GUÍA VISUAL DE RELACIONES - BACKEND MAAS v4.0

## 1. PIRÁMIDE DE DEPENDENCIAS

```
                    ┌─────────────────────┐
                    │   Usuario/Frontend  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   FastAPI/Uvicorn   │
                    │   Endpoints REST    │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   ┌────▼────┐         ┌──────▼──────┐         ┌─────▼────┐
   │ /health │         │/preinversion│         │ /sessions│
   │  (GET)  │         │-plans (POST)│         │ (other)  │
   └────┬────┘         └──────┬──────┘         └─────┬────┘
        │                     │                      │
        └──────────────────────┼──────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   AgentOS Runtime   │
                    │  Orquestación de    │
                    │     agentes         │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   ┌────▼────┐         ┌──────▼──────┐         ┌─────▼────┐
   │ Agentes │         │  Workflows  │         │  Teams   │
   │(6 total)│         │(Orquestación)         │(Colabo)  │
   └────┬────┘         └──────┬──────┘         └─────┬────┘
        │                     │                      │
        └──────────────────────┼──────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Context Broker    │
                    │ (Single Source of  │
                    │    Truth)          │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   ┌────▼────┐         ┌──────▼──────┐         ┌─────▼────┐
   │Session  │         │ Project KB  │         │ Rules KB │
   │Database │         │(Hechos del  │         │(Plantillas
   │         │         │ proyecto)   │         │ & Normas)│
   └─────────┘         └─────────────┘         └──────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │    PostgreSQL       │
                    │  + pgvector (3 DBs) │
                    └─────────────────────┘
```

---

## 2. MAPA DE AGENTES Y SUS HERRAMIENTAS

```
┌───────────────────────────────────────────────────────────┐
│                     AGENTIOS (6 agentes)                   │
└───────────────────────────────────────────────────────────┘

1️⃣  GenericDataAgent ──────→ Entrada: project_id
    Role: Extracción         Salida: Datos brutos + contexto
    ├─ Herramientas:
    │  ├─ RedmineTools ✨✨✨ (list, issues, details)
    │  ├─ RedmineKnowledgeTools (search similar)
    │  ├─ ReasoningTools (plan extracción)
    │  └─ KnowledgeTools (acceso KB)
    │
    └─ Knowledge Base: project_kb
        
        ↓
        
2️⃣  MetricExtractorAgent ──→ Entrada: Datos brutos
    Role: Transformación      Salida: Pydantic objects
    ├─ Herramientas:
    │  ├─ RedmineTools ✨✨✨ (refresh data)
    │  ├─ RedmineReasoningTools (impact analysis)
    │  ├─ SourceTextTools (evidence extraction)
    │  ├─ ReasoningTools (structure data)
    │  └─ KnowledgeTools (schemas from KB)
    │
    └─ Knowledge Base: rules_kb (schemas)
    
        ↓
        
3️⃣  GeneralAuthorAgent ────→ Entrada: Métricas validadas
    Role: Redacción           Salida: Documento SIC markdown
    ├─ Herramientas:
    │  ├─ RedmineKnowledgeTools (best practices)
    │  ├─ ReasoningTools (plan estructura)
    │  └─ KnowledgeTools (SIC templates)
    │
    └─ Knowledge Base: rules_kb (SIC 01-22)
    
        ↓
        
4️⃣  ExpertJudgeAgent ──────→ Entrada: Documento SIC
    Role: Auditoría           Salida: Reporte + scoring (0-100)
    ├─ Herramientas:
    │  ├─ RedmineReasoningTools (impact eval)
    │  ├─ ReasoningTools (deep analysis)
    │  └─ KnowledgeTools (normas CODELCO)
    │
    └─ Knowledge Base: rules_kb (NCC24, SGPD)
        
        └─ Scoring: PASS(≥70) / REVIEW(50-69) / FAIL(<50)

5️⃣  MasterPlannerAgent ────→ Entrada: document_type
    Role: Planificación       Salida: DAG de secciones
    └─ Herramientas:
       └─ Razonamiento avanzado (o3-mini)
       
6️⃣  DependencyManagerAgent ─→ Entrada: Estructura
    Role: Dependencias        Salida: Grafo resuelto
    └─ Herramientas:
       └─ Análisis de grafos
```

---

## 3. MATRIZ DE HERRAMIENTAS VS AGENTES

```
┌──────────────────────┬──────┬────────┬────────┬───────┬────────┬──────────┐
│ Tool / Agent         │ Data │Extract │Author  │Judge  │Planner │Depend    │
├──────────────────────┼──────┼────────┼────────┼───────┼────────┼──────────┤
│ RedmineTools         │ ✅✅ │ ✅✅   │        │       │        │          │
│ RedmineKnowledge     │ ✅   │        │ ✅✅   │       │        │          │
│ RedmineReasoning     │      │ ✅     │        │ ✅✅  │        │ ✅       │
│ SourceTextTools      │      │ ✅✅   │        │       │        │          │
│ ReasoningTools       │ ✅   │ ✅     │ ✅     │ ✅    │ ✅✅   │ ✅✅     │
│ KnowledgeTools       │ ✅   │ ✅     │ ✅     │ ✅    │ ✅     │ ✅       │
└──────────────────────┴──────┴────────┴────────┴───────┴────────┴──────────┘

Leyenda:
✅    = Usa esta herramienta
✅✅  = Uso crítico/frecuente
(vacío) = No la usa
```

---

## 4. FLUJO DE DATOS PRINCIPAL

```
ENTRADA DEL USUARIO
        │
        │ POST /preinversion-plans
        │ {project_id: 1, document_type: "SIC"}
        ↓
    ┌───────────────────────────────────────────┐
    │ FASE 1: DATA EXTRACTION                   │
    │ GenericDataAgent                          │
    └───────────────────────────────────────────┘
        │
        ├─ Usa RedmineTools.list_projects()
        ├─ Usa RedmineTools.get_project_issues()
        ├─ Usa RedmineTools.get_issue_details()
        ├─ Usa RedmineTools.get_issue_relations()
        ├─ Usa RedmineKnowledgeTools.search_similar()
        ├─ Consulta: project_kb
        │
        ↓
        Salida: {
          "projects": [...],
          "issues": [...],
          "relations": [...],
          "context": "..."
        }
        │
        ├─ Almacena en session_db
        │
        ↓
    ┌───────────────────────────────────────────┐
    │ FASE 2: DATA TRANSFORMATION               │
    │ MetricExtractorAgent                      │
    └───────────────────────────────────────────┘
        │
        ├─ Consulta: rules_kb (esquemas)
        ├─ Usa RedmineTools.get_issue_details() ✨ NUEVO
        ├─ Estructura: data → SIC14, SIC16, SIC03
        ├─ Valida: Pydantic validation
        ├─ Cita: SourceTextTools evidence extraction
        │
        ↓
        Salida: {
          "SIC14": SIC14Plazo(...),
          "SIC16": SIC16Capex(...),
          "SIC03": SIC03Riesgo(...),
          "confidence": 0.95,
          "sources": [...]
        }
        │
        ├─ Almacena en session_db
        │
        ↓
    ┌───────────────────────────────────────────┐
    │ FASE 3: DOCUMENT AUTHORING                │
    │ GeneralAuthorAgent                        │
    └───────────────────────────────────────────┘
        │
        ├─ Consulta: rules_kb (SIC templates)
        ├─ Lee: SIC_01.md, SIC_02.md, ... SIC_22.md
        ├─ Planifica: Estructura de documento
        ├─ Redacta: Cada sección SIC
        │
        ↓
        Salida: {
          "document": "# Preinversión...\n\n## SIC_01...",
          "sections": 22,
          "word_count": 15000,
          "toc": [...]
        }
        │
        ├─ Almacena en session_db
        │
        ↓
    ┌───────────────────────────────────────────┐
    │ FASE 4: QUALITY AUDIT & VALIDATION        │
    │ ExpertJudgeAgent                          │
    └───────────────────────────────────────────┘
        │
        ├─ Consulta: rules_kb (NCC24, SGPD)
        ├─ Analiza: Estructura y completitud
        ├─ Valida: Contra normas CODELCO
        ├─ Evalúa: Riesgos e impacto
        ├─ Calcula: Scoring por categoría
        │
        │   Cálculo de Scoring:
        │   ├─ Categoría A (Completitud): 30% weight
        │   ├─ Categoría B (Normas): 40% weight
        │   ├─ Categoría C (Evidencia): 20% weight
        │   ├─ Categoría D (Riesgos): 10% weight
        │   └─ TOTAL SCORE = A*0.3 + B*0.4 + C*0.2 + D*0.1
        │
        ├─ Clasificación:
        │   ├─ PASS (≥70): Aprobado
        │   ├─ REVIEW (50-69): Requiere cambios
        │   └─ FAIL (<50): Rechazado
        │
        ↓
        Salida: {
          "final_score": 82,
          "status": "PASS",
          "findings": [...],
          "recommendations": [...],
          "blockers": [],
          "audit_trail": [...]
        }
        │
        ├─ Almacena en session_db + audit_logs
        │
        ↓
    ┌───────────────────────────────────────────┐
    │ RESPUESTA HTTP 200                        │
    │ {                                         │
    │   "status": "success",                    │
    │   "document": "...",                      │
    │   "audit_report": "...",                  │
    │   "score": 82,                            │
    │   "message": "Plan generado"              │
    │ }                                         │
    └───────────────────────────────────────────┘
        │
        ↓
    USUARIO RECIBE DOCUMENTO
    Y REPORTE DE AUDITORÍA
```

---

## 5. DIAGRAMA DE BASES DE DATOS

```
PostgreSQL Instance
│
├─ Base 1: maas_sessions
│   ├─ Tabla: maas_sessions
│   │   ├─ id (UUID)
│   │   ├─ project_id (INT)
│   │   ├─ data (JSONB) ← Historial de conversación
│   │   └─ created_at (TIMESTAMP)
│   │
│   └─ Almacena: Sesiones, historial de agentes
│
├─ Base 2: project_knowledge (PgVector)
│   ├─ Tabla: project_knowledge
│   │   ├─ id (UUID)
│   │   ├─ project_id (INT)
│   │   ├─ content (TEXT)
│   │   ├─ embedding (VECTOR[1536]) ← OpenAI embeddings
│   │   ├─ source (VARCHAR)
│   │   └─ created_at (TIMESTAMP)
│   │
│   ├─ Search Type: Hybrid (keyword + semantic)
│   └─ Almacena: Hechos dinámicos del proyecto
│
└─ Base 3: business_rules (PgVector)
    ├─ Tabla: business_rules
    │   ├─ id (UUID)
    │   ├─ content (TEXT)
    │   ├─ source (VARCHAR) ← SIC_01.md, rules_ncc24.txt, etc
    │   ├─ category (VARCHAR) ← SIC01, SIC02, ..., NCC24, SGPD
    │   ├─ embedding (VECTOR[1536]) ← OpenAI embeddings
    │   └─ created_at (TIMESTAMP)
    │
    ├─ Tabla: business_rules_contents (metadata)
    │   └─ Índices para búsqueda rápida
    │
    ├─ Search Type: Hybrid (keyword + semantic)
    │
    └─ Almacena: 22 plantillas SIC + normas CODELCO
        ├─ SIC_01.md → Resumen y Recomendaciones
        ├─ SIC_02.md → Caso de Negocio
        ├─ SIC_03.md → Riesgos
        ├─ ... (19 más)
        ├─ SIC_22.md → Avance
        └─ rules_ncc24.txt → Normas CODELCO
```

---

## 6. CICLO DE VIDA DEL BACKEND

```
┌─────────────────────────────────────────────────────────┐
│                   STARTUP (Startup)                      │
└─────────────────────────────────────────────────────────┘
    │
    ├─ 1. Load .env variables
    │   └─ DATABASE_URL, OPENAI_API_KEY, REDMINE_*
    │
    ├─ 2. Initialize ContextBroker
    │   ├─ session_db = PostgresDb()
    │   ├─ project_kb = Knowledge()
    │   └─ rules_kb = Knowledge()
    │
    ├─ 3. Initialize OpenAI GPT-4o Model
    │   └─ api_key, base_url from env
    │
    ├─ 4. Instantiate 6 Agents
    │   ├─ GenericDataAgent(broker, model)
    │   ├─ MetricExtractorAgent(broker, model)
    │   ├─ GeneralAuthorAgent(broker, model)
    │   ├─ ExpertJudgeAgent(broker, model)
    │   ├─ MasterPlannerAgent(broker, model)
    │   └─ DependencyManagerAgent(broker, model)
    │
    ├─ 5. Create Team (Colaborativo)
    │   └─ doc_team = Team([Extractor, Author, Judge])
    │
    ├─ 6. Lifespan STARTUP EVENT
    │   └─ await broker.load_rules()
    │       ├─ Lee /templates/ → 22 archivos SIC
    │       ├─ Vectoriza con OpenAI embeddings
    │       └─ Almacena en rules_kb (PostgreSQL)
    │
    ├─ 7. Create AgentOS Runtime
    │   ├─ agents=[...6 agentes...]
    │   ├─ teams=[doc_team]
    │   └─ workflows=[DocumentCreationWorkflow]
    │
    ├─ 8. Register Endpoints
    │   ├─ GET /health
    │   └─ POST /preinversion-plans
    │
    └─ 9. Start Uvicorn Server
        └─ http://localhost:7777 → READY ✅

┌─────────────────────────────────────────────────────────┐
│                    RUNNING (Runtime)                     │
└─────────────────────────────────────────────────────────┘
    │
    ├─ GET /health
    │   └─ Retorna: {"status": "ok"}
    │
    └─ POST /preinversion-plans
        ├─ Ejecuta FASE 1 (DataAgent)
        ├─ Ejecuta FASE 2 (ExtractorAgent)
        ├─ Ejecuta FASE 3 (AuthorAgent)
        ├─ Ejecuta FASE 4 (JudgeAgent)
        └─ Retorna: {document, audit_report}

┌─────────────────────────────────────────────────────────┐
│                    SHUTDOWN (Cleanup)                    │
└─────────────────────────────────────────────────────────┘
    │
    ├─ Lifespan SHUTDOWN EVENT
    │   └─ Cierra conexiones a PostgreSQL
    │
    └─ Uvicorn Server Stopped
```

---

## 7. MATRIZ DE RESPONSABILIDADES

```
┌──────────────────────────┬────────────────────────────────────────┐
│ Componente               │ Responsabilidades                      │
├──────────────────────────┼────────────────────────────────────────┤
│ main.py                  │ • Inicializar sistema                  │
│                          │ • Crear agentes                        │
│                          │ • Setup endpoints                      │
│                          │ • Start server                         │
├──────────────────────────┼────────────────────────────────────────┤
│ ContextBroker            │ • Gestionar 3 Knowledge Bases          │
│                          │ • Vector embeddings (OpenAI)           │
│                          │ • Load rules at startup                │
│                          │ • Query KBs for agents                 │
├──────────────────────────┼────────────────────────────────────────┤
│ GenericDataAgent         │ • Extraer datos de Redmine             │
│                          │ • Analizar relaciones                  │
│                          │ • Buscar patrones históricos           │
│                          │ • Proporcionar contexto del proyecto   │
├──────────────────────────┼────────────────────────────────────────┤
│ MetricExtractorAgent     │ • Transformar datos brutos             │
│                          │ • Validar con Pydantic                 │
│                          │ • Extraer evidencia                    │
│                          │ • Citar fuentes                        │
├──────────────────────────┼────────────────────────────────────────┤
│ GeneralAuthorAgent       │ • Redactar documento SIC               │
│                          │ • Aplicar plantillas (01-22)           │
│                          │ • Mantener coherencia                  │
│                          │ • Generar markdown profesional         │
├──────────────────────────┼────────────────────────────────────────┤
│ ExpertJudgeAgent         │ • Auditar documento                    │
│                          │ • Validar contra normas CODELCO        │
│                          │ • Calcular scoring (0-100)             │
│                          │ • Generar recomendaciones              │
├──────────────────────────┼────────────────────────────────────────┤
│ MasterPlannerAgent       │ • Planificar estructura de documento   │
│                          │ • Crear DAG de secciones               │
│                          │ • Asignar prioridades                  │
├──────────────────────────┼────────────────────────────────────────┤
│ DependencyManagerAgent   │ • Mapear dependencias                  │
│                          │ • Resolver ciclos                      │
│                          │ • Calcular orden topológico            │
├──────────────────────────┼────────────────────────────────────────┤
│ RedmineTools             │ • Conectar a Redmine API               │
│                          │ • Listar proyectos e issues            │
│                          │ • Cache de resultados                  │
├──────────────────────────┼────────────────────────────────────────┤
│ PostgreSQL               │ • Almacenar sesiones                   │
│                          │ • Índices vectoriales (pgvector)       │
│                          │ • Hybrid search (keyword + semantic)   │
├──────────────────────────┼────────────────────────────────────────┤
│ OpenAI (GPT-4o)          │ • Razonamiento de agentes              │
│                          │ • Generación de texto                  │
│                          │ • Embeddings (text-embedding-3-small)  │
└──────────────────────────┴────────────────────────────────────────┘
```

---

## 8. CASOS DE USO PRINCIPALES

### Caso 1: Generar Plan de Preinversión

```
Usuario quiere un documento SIC para proyecto minería

1. POST /preinversion-plans {project_id: 42, document_type: "SIC"}
   │
   ├─ Data Agent obtiene: proyectos, issues, metadata desde Redmine
   │
   ├─ Extractor convierte a: SIC14 (plazo), SIC16 (CAPEX), etc
   │
   ├─ Author redacta: 22 secciones SIC markdown
   │
   ├─ Judge audita: 
   │   ├─ Completitud ✓ 95%
   │   ├─ Normas CODELCO ✓ 85%
   │   ├─ Evidencia ✓ 90%
   │   └─ Score Final: 82/100 → PASS
   │
   └─ Usuario recibe: Documento + Reporte de Auditoría
```

### Caso 2: Revisar Plan Existente

```
Usuario quiere validar un documento anterior

1. Carga documento en sistema
2. POST /audit {document: "...", project_id: 42}
3. Judge valida contra normas CODELCO
4. Retorna: Hallazgos + Recomendaciones
```

### Caso 3: Iterar y Mejorar

```
Usuario recibe documento con score 65 (REVIEW)

1. Identifica hallazgos críticos
2. Modifica datos en Redmine
3. POST /preinversion-plans {project_id: 42} (nuevamente)
4. Sistema genera documento mejorado
5. Score aumenta a 82 (PASS)
```

---

**Este documento detalla la especificación técnica completa del backend MAAS v4.0.**

Versión: 4.0 | Estado: ✅ Production Ready | Fecha: 3 Enero 2026
