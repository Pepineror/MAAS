# 🚀 GUÍA DE USO RÁPIDO - MAAS v4.0

## 📌 TL;DR (Very Quick Start)

1. Backend está levantado en `http://localhost:7777` ✅
2. Health check: `curl http://localhost:7777/health`
3. Generar documento: `POST /preinversion-plans {project_id: 1}`
4. Resultado: Documento SIC + Audit Report

---

## 🔧 CONFIGURACIÓN REQUERIDA

### Variables de Entorno (.env)

```bash
# Base de Datos
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/maas

# OpenAI
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_BASE_URL=https://api.openai.com/v1

# Redmine (Fuente de datos)
REDMINE_BASE_URL=http://cidiia.uce.edu.do/
REDMINE_API_KEY=your-redmine-api-key

# Backend
BACKEND_PORT=7777
BACKEND_HOST=0.0.0.0

# Frontend
FRONTEND_URL=http://localhost:3001
```

---

## 📊 ESTRUCTURA DE ARCHIVOS (Cómo Se Relacionan)

```
backend/
├── main.py ──────────────────────────────────────→ PUNTO DE ENTRADA
│   ├─ Inicializa ContextBroker
│   ├─ Crea 6 agentes
│   └─ Define endpoints REST
│
├── core/
│   └── context_broker.py ─────────────────────→ GESTIÓN DE DATOS
│       ├─ session_db (sesiones)
│       ├─ project_kb (hechos del proyecto)
│       └─ rules_kb (plantillas SIC + normas)
│
├── agents/ ──────────────────────────────────→ 6 AGENTES ESPECIALIZADOS
│   ├── generic_data_agent.py ──→ FASE 1: Extrae datos Redmine
│   ├── metric_extractor_agent.py → FASE 2: Transforma a métricas
│   ├── author_agent.py ────────→ FASE 3: Redacta documento SIC
│   ├── judge_agent.py ─────────→ FASE 4: Audita y valida
│   ├── planner_agent.py ───────→ Planificación
│   ├── extractor_agent.py ─────→ Ingesta de datos
│   └── schemas.py ─────────────→ Validación Pydantic
│
├── tools/ ──────────────────────────────────→ HERRAMIENTAS
│   └── custom_tools.py
│       ├─ RedmineTools (obtiene datos)
│       ├─ RedmineKnowledgeTools (búsqueda)
│       ├─ RedmineReasoningTools (análisis)
│       └─ SourceTextTools (evidencia)
│
├── workflows/ ──────────────────────────────→ ORQUESTACIÓN
│   └── document_workflow.py ──→ Coordinación de agentes
│
└── knowledge/ ──────────────────────────────→ CONTENIDO ESTÁTICO
    ├── templates/ (SIC_01.md ... SIC_22.md)
    └── rules_ncc24.txt (Normas CODELCO)
```

---

## 🔄 FLUJO DE EJECUCIÓN PASO A PASO

### Cuando haces POST /preinversion-plans

```
1. Tu petición llega a main.py
   └─ endpoint: generate_preinversion_plan()

2. FASE 1 - GenericDataAgent (5-10 seg)
   ├─ Conecta a Redmine
   ├─ Obtiene proyectos y issues
   ├─ Mapea relaciones
   └─ Retorna: datos brutos + contexto

3. FASE 2 - MetricExtractorAgent (10-15 seg)
   ├─ Consulta rules_kb para esquemas
   ├─ Obtiene datos frescos de Redmine
   ├─ Transforma a objetos Pydantic
   ├─ Valida tipos y restricciones
   └─ Retorna: SIC14, SIC16, SIC03, etc validadas

4. FASE 3 - GeneralAuthorAgent (15-20 seg)
   ├─ Consulta rules_kb para plantillas SIC
   ├─ Lee: SIC_01.md, SIC_02.md, ... SIC_22.md
   ├─ Sustituye datos en placeholders
   ├─ Aplica formato markdown profesional
   └─ Retorna: documento SIC completo

5. FASE 4 - ExpertJudgeAgent (10-15 seg)
   ├─ Analiza estructura y completitud
   ├─ Valida contra NCC24 (normas CODELCO)
   ├─ Evalúa riesgos e impacto
   ├─ Calcula scoring:
   │   Score = A(0.3) + B(0.4) + C(0.2) + D(0.1)
   │   PASS (≥70) / REVIEW (50-69) / FAIL (<50)
   └─ Retorna: reporte + hallazgos

6. Respuesta HTTP 200
   ├─ Document: "# Plan de Preinversión..."
   ├─ Audit Report: "Hallazgos encontrados..."
   ├─ Score: 82
   └─ Status: "PASS"
```

---

## 💾 ¿DÓNDE SE ALMACENAN LOS DATOS?

### PostgreSQL (3 Bases Separadas)

**Base 1: maas_sessions**
- Almacena: Historial de sesiones y conversaciones
- Tabla: `maas_sessions`
- Acceso: ContextBroker.session_db

**Base 2: project_knowledge**
- Almacena: Hechos dinámicos del proyecto
- Tipo: Knowledge Base con embeddings vectoriales
- Búsqueda: Hybrid (keyword + semantic)
- Acceso: ContextBroker.project_kb

**Base 3: business_rules** ✨ LA MÁS IMPORTANTE
- Almacena: 22 plantillas SIC + normas CODELCO
- Contenido: 
  - SIC_01.md, SIC_02.md, ... SIC_22.md
  - rules_ncc24.txt
- Tipo: Knowledge Base con embeddings vectoriales
- Búsqueda: Hybrid (keyword + semantic)
- Acceso: ContextBroker.rules_kb
- Cargadas en: startup via broker.load_rules()

---

## 🎯 EJEMPLO PRÁCTICO: Generar Plan para Proyecto Minería

### Paso 1: Preparar Datos en Redmine

```
Redmine (cidiia.uce.edu.do)
├─ Proyecto: "Mina Cobre Sur" (ID: 42)
├─ Issues:
│  ├─ #101: Exploración Geológica
│  ├─ #102: Estudio de Viabilidad
│  ├─ #103: Diseño de Ingeniería
│  └─ #104: Evaluación Ambiental
└─ Custom Fields:
   ├─ Presupuesto: 500,000,000 USD
   ├─ Duración: 24 meses
   └─ Riesgo: ALTO
```

### Paso 2: Llamar API

```bash
curl -X POST http://localhost:7777/preinversion-plans \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 42,
    "document_type": "SIC"
  }'
```

### Paso 3: Backend Procesa (50 segundos)

```
[1/4] Extrayendo datos de Redmine para proyecto 42...
  ✓ Proyectos obtenidos: 1
  ✓ Issues obtenidos: 4
  ✓ Relaciones mapeadas: 6
  ✓ Tiempo: 7 segundos

[2/4] Transformando datos a métricas SIC...
  ✓ SIC14Plazo validado
  ✓ SIC16Capex validado
  ✓ SIC03Riesgo validado
  ✓ Tiempo: 12 segundos

[3/4] Redactando documento SIC...
  ✓ SIC_01: Resumen (1000 palabras)
  ✓ SIC_02: Caso de Negocio (1500 palabras)
  ✓ SIC_03: Riesgos (800 palabras)
  ✓ ... [19 secciones más]
  ✓ SIC_22: Avance (500 palabras)
  ✓ Tiempo: 18 segundos

[4/4] Validando cumplimiento normativo...
  ✓ Completitud: 95% (Categoría A)
  ✓ Normas CODELCO: 88% (Categoría B)
  ✓ Evidencia: 92% (Categoría C)
  ✓ Riesgos: 85% (Categoría D)
  ✓ SCORE FINAL: 89/100 ✅ PASS
  ✓ Tiempo: 13 segundos
```

### Paso 4: Recibir Resultado

```json
{
  "status": "success",
  "project_id": 42,
  "document_type": "SIC",
  "full_document": "# PLAN DE PREINVERSIÓN\n## Mina Cobre Sur\n\n### SIC_01: Resumen y Recomendaciones\n\n...[documento completo de 20 páginas]...",
  "audit_report": {
    "final_score": 89,
    "status": "PASS",
    "findings": [
      {
        "severity": "MEDIUM",
        "category": "Completitud",
        "issue": "Falta detalle en cronograma final"
      }
    ],
    "recommendations": [
      "Agregar hitos específicos en Q4 2026"
    ]
  },
  "message": "Plan de preinversión generado exitosamente"
}
```

### Paso 5: Descargar y Usar

```
✓ Documento guardado como: preinversion_42_2026.md
✓ Reporte guardado como: audit_42_2026.json
✓ Score: 89/100 (PASS)
✓ Listo para presentación ejecutiva ✅
```

---

## 🔍 CÓMO VERIFICAR QUE ESTÁ FUNCIONANDO

### Health Check

```bash
$ curl http://localhost:7777/health
{
  "status": "ok",
  "instantiated_at": "1767464244.357229"
}
```

### Verificar Agentes

```bash
$ python validate_agents.py
✅ All agent imports successful
✅ Todos los agentes pueden importarse
✅ Validación completa - Arquitectura lista
```

### Revisar Logs

```bash
$ tail -f backend.log
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:7777
```

---

## 🚨 TROUBLESHOOTING

### "Port 7777 already in use"

```bash
# Matar procesos en puerto 7777
lsof -i :7777 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Levantar nuevamente
python backend/main.py
```

### "Redmine API Key not configured"

```bash
# Verificar .env
echo $REDMINE_API_KEY

# Si está vacío, configurar:
REDMINE_API_KEY=your-key-from-redmine
REDMINE_BASE_URL=http://cidiia.uce.edu.do/
```

### "Database connection failed"

```bash
# Verificar PostgreSQL está corriendo
psql -h localhost -U postgres -c "SELECT 1"

# Si falla, iniciar PostgreSQL
docker-compose up -d db
```

### "No module named 'backend'"

```bash
# Asegurarse de estar en directorio correcto
cd /home/iades/IADES/PRODUCTOS/00.banco\ de\ probemas\ IADES/MAAS/MAAS3

# Activar venv
source .venv/bin/activate

# Ejecutar
python backend/main.py
```

---

## 📈 INTERPRETACIÓN DE SCORES

### Score 85-100: EXCELENTE ✅✅✅
```
Documento listo para presentación ejecutiva
- Todas secciones presentes
- Cumple normas CODELCO
- Evidencia suficiente
- Riesgos mitigados
→ ACCIÓN: Presentar a directivos
```

### Score 70-84: BUENO ✅
```
Documento aceptable con cambios menores
- Secciones principales presentes
- Cumple principalmente normas
- Algo de evidencia incompleta
→ ACCIÓN: Revisar recomendaciones, pequeños ajustes
```

### Score 50-69: REVISAR ⚠️
```
Documento requiere cambios significativos
- Faltan secciones importantes
- Algunos incumplimientos normativos
- Evidencia débil
→ ACCIÓN: Volver a Redmine, actualizar datos, regenerar
```

### Score <50: RECHAZADO ❌
```
Documento no cumple requisitos mínimos
- Faltan secciones críticas
- Múltiples incumplimientos normativos
- Sin evidencia
→ ACCIÓN: Recolectar datos faltantes, regenerar desde cero
```

---

## 🔐 SEGURIDAD Y PERMISOS

**Modo Actual (Desarrollo)**:
- Sin autenticación
- Sin restricción de usuarios
- Acceso libre a todos los endpoints

**Recomendaciones para Producción**:
- Activar JWT authentication
- Implementar rate limiting
- Auditar acceso a todos los endpoints
- Usar HTTPS
- Encriptar credenciales en .env

---

## 📞 NEXT STEPS

1. **Verificar credenciales de Redmine**
   ```
   curl -H "X-Redmine-API-Key: $REDMINE_API_KEY" \
        http://cidiia.uce.edu.do/projects.json
   ```

2. **Testear con proyecto real**
   ```
   POST /preinversion-plans {project_id: 1}
   ```

3. **Interpretar resultados**
   - Score ≥70 → Listo
   - Score <70 → Revisar hallazgos

4. **Iterar si es necesario**
   - Actualizar datos en Redmine
   - Regenerar documento

---

## 📚 RECURSOS

| Documento | Para... |
|---|---|
| ESPECIFICACION_BACKEND.md | Entender arquitectura técnica |
| ARQUITECTURA_VISUAL.md | Ver diagramas y relaciones |
| RESUMEN_EJECUTIVO.md | Explicación de alto nivel |
| GUIA_RAPIDA.md | Este documento |

---

**¡Listo para usar!** 🚀

**Backend**: http://localhost:7777 ✅  
**Health**: http://localhost:7777/health ✅  
**Endpoint**: POST /preinversion-plans ✅  

Versión: 4.0 | Estado: Production Ready | 3 Enero 2026
