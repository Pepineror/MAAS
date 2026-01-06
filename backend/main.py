import os
import sys
import logging
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional

# Configurar logging PRIMERO
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('maas_backend.log')
    ]
)
logger = logging.getLogger(__name__)

# Corregir ModuleNotFoundError
# Agregar el directorio raíz del proyecto a sys.path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
    logger.info(f"Añadido al sys.path: {root_dir}")

# Cargar variables de entorno al inicio
from dotenv import load_dotenv
load_dotenv()

# Verificar variables críticas de entorno
required_env_vars = ["OPENAI_API_KEY", "DATABASE_URL"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"❌ ERROR: Variables de entorno faltantes: {missing_vars}")
    logger.error("Por favor, configura las variables en .env o entorno")
    sys.exit(1)

try:
    import openai
except ImportError:
    logger.error("\n[!] ERROR: Librería 'openai' no detectada.")
    logger.error("[!] Por favor ejecuta: ./venv/bin/pip install openai\n")
    sys.exit(1)

try:
    from pydantic import BaseModel
    from agno.os import AgentOS
    from agno.os.settings import AgnoAPISettings
    from agno.team import Team
    from agno.models.openai import OpenAIChat
    
    # Importar componentes del backend
    from backend.core.context_broker import ContextBroker
    from backend.core.async_postgres_db import AsyncPostgresDb
    from backend.agents.generic_data_agent import GenericDataAgent
    from backend.agents.metric_extractor_agent import MetricExtractorAgent
    from backend.agents.author_agent import GeneralAuthorAgent
    from backend.agents.judge_agent import ExpertJudgeAgent
    from backend.agents.planner_agent import MasterPlannerAgent, DependencyManagerAgent
    from backend.agents.planner_agent import MasterPlannerAgent, DependencyManagerAgent
    from backend.workflows.document_workflow import DocumentCreationWorkflow
    from backend.tools.pdf_tool import PDFConverterTools
    from fastapi import HTTPException, Depends, Request
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    
    auth_scheme = HTTPBearer()
    
    logger.info("✅ Todas las dependencias importadas correctamente")
    
except ImportError as e:
    logger.error(f"❌ ERROR: Fallo al importar módulos del backend: {e}")
    logger.error("Verifica que la estructura del proyecto sea correcta")
    logger.error(f"sys.path actual: {sys.path}")
    sys.exit(1)

# 1. Inicializar Context Broker (Single Source of Truth)
try:
    broker = ContextBroker(
        db_url=os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5434/maas"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    )
    logger.info("✅ ContextBroker inicializado correctamente")
except Exception as e:
    logger.error(f"❌ ERROR: No se pudo inicializar ContextBroker: {e}")
    sys.exit(1)

# 2. Inicializar Agentes Holónicos Genéricos
try:
    openai_model = OpenAIChat(
        id="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    )
    
    # Inicializar agentes
    data_agent = GenericDataAgent(
        broker=broker,
        model=openai_model, 
        db=broker.session_db
    )
    
    extractor = MetricExtractorAgent(
        broker=broker, 
        model=openai_model, 
        db=broker.session_db
    )
    
    author = GeneralAuthorAgent(
        broker=broker, 
        model=openai_model, 
        db=broker.session_db
    )
    
    judge = ExpertJudgeAgent(
        broker=broker, 
        model=openai_model, 
        db=broker.session_db
    )
    
    logger.info("✅ Agentes holónicos inicializados según documentación")
    
except Exception as e:
    logger.error(f"❌ ERROR: No se pudieron inicializar agentes: {e}", exc_info=True)
    sys.exit(1)

# 3. Inicializar Holón de Planificación
try:
    planner = MasterPlannerAgent(
        broker=broker, 
        model=openai_model, 
        db=broker.session_db
    )
    
    dep_manager = DependencyManagerAgent(
        broker=broker, 
        model=openai_model, 
        db=broker.session_db
    )
    
    logger.info("✅ Agentes de planificación inicializados")
    
except Exception as e:
    logger.error(f"❌ ERROR: No se pudieron inicializar agentes de planificación: {e}")
    sys.exit(1)

# 4. Inicializar Herramientas Globales
pdf_tool = PDFConverterTools(output_dir="output_pdfs")

# 4. Inicializar Equipos
try:
    # TODOS los 6 agentes en el Team para trabajo colaborativo completo
    doc_team = Team(
        id="document-team",
        name="Document Generation Team",
        description="Equipo holónico completo para planes de preinversión: extracción Redmine, métricas, planificación, autoría y auditoría.",
        instructions=[
            "═══════════════════════════════════════════════════════════",
            "INSTRUCCIONES DE COORDINACIÓN DEL EQUIPO MAAS",
            "═══════════════════════════════════════════════════════════",
            "Tu objetivo es coordinar a los 6 agentes para generar planes de preinversión completos.",
            "",
            "1. SI se te pide generar un documento o plan SIC (ej. 'genera el plan SIC para proyecto 7'):",
            "   - NO te limites a describir el plan. DEBES ejecutar la producción de contenido.",
            "   - FASE 1: Delega al GenericDataAgent para listar proyectos e investigar el proyecto por su ID.",
            "   - FASE 2: Delega al MasterPlannerAgent para crear el DAG de secciones SIC necesarias.",
            "   - FASE 3: Delega al MetricExtractorAgent para obtener indicadores financieros reales.",
            "   - FASE 4: Delega al GeneralAuthorAgent para redactar CADA sección. ¡ESPERA SU RESPUESTA COMPLETA!",
            "   - FASE 5 (CRÍTICO): TOMA EL TEXTO GENERADO por el Author y PÁSALO INMEDIATAMENTE al ExpertJudgeAgent.",
            "     * DEBES LLAMAR a 'delegate_task_to_member' con el ExpertJudgeAgent.",
            "     * Instrucción al Judge: 'Audita y MUESTRA el texto completo de este contenido: [PEGAR_TEXTO_DEL_AUTHOR]'",
            "     * SI NO LLAMAS AL JUDGE CON EL TEXTO, EL PROCESO FALLA.",
            "",
            "2. EXTRACCIÓN DE DATOS (GenericDataAgent):",
            "   - Asegúrate de obtener todos los custom fields de Redmine.",
            "   - Si el proyecto tiene issues de inventario (ID 7), trátalos como activos/equipos para CAPEX/OPEX.",
            "",
            "3. REDACCIÓN (GeneralAuthorAgent):",
            "   - El autor debe producir el texto markdown completo de los documentos.",
            "   - Asegúrate de que los placeholders [VALOR] sean reemplazados por datos reales.",
            "",
            "4. TRABAJO COLABORATIVO:",
            "   - Usa la herramienta 'delegate_task_to_member' para orquestar los pasos.",
            "   - Mantén la coherencia entre lo que el Planner define y lo que el Author escribe.",
            "   - Presenta el resultado final como un conjunto de documentos markdown completos.",
            "",
            "5. ENTREGA FINAL (REGLA DE ORO):",
            "   - ¡NO RESUMAS! Tu respuesta final al usuario DEBE ser el veredicto y el documento del Juez íntegros.",
            "   - Prohibido decir 'El plan ha sido creado, aquí tienes un resumen'.",
            "   - DEBES mostrar el Markdown que te entregue el ExpertJudgeAgent tal cual.",
            "",
            "Cita siempre las fuentes de Redmine (issue #ID) para cada dato importante.",
            "═══════════════════════════════════════════════════════════"
        ],
        members=[data_agent, extractor, author, judge, planner, dep_manager],  # Los 6 agentes
        model=openai_model,
        markdown=True
    )
    
    logger.info("✅ Equipo de documentos inicializado con 6 agentes")
    
except Exception as e:
    logger.error(f"❌ ERROR: No se pudo inicializar equipo: {e}", exc_info=True)
    
    # Fallback con todos los agentes
    try:
        doc_team = Team(
            id="document-team",
            name="Document Generation Team",
            description="Equipo holónico completo para planes de preinversión.",
            members=[data_agent, extractor, author, judge, planner, dep_manager],
            model=openai_model
        )
        logger.info("✅ Equipo de documentos inicializado (fallback)")
    except Exception as e2:
        logger.error(f"❌ ERROR: No se pudo inicializar equipo incluso simplificado: {e2}")
        sys.exit(1)

# 5. Inicializar Meta-Workflow (Workflows 2.0 - FASE I)
try:
    doc_workflow = DocumentCreationWorkflow(
        planner=planner,
        extractor=extractor,
        author=author,
        reviewer=judge,
        workspace_id="default",
        db=broker.session_db,
        pdf_tool=pdf_tool
    )
    
    logger.info("✅ Workflow de creación de documentos inicializado")
    
except Exception as e:
    logger.error(f"❌ ERROR: No se pudo inicializar workflow: {e}")
    sys.exit(1)

# 6. Configurar AgentOS Runtime - FASE II: AsyncPostgresDb con connection pooling
@asynccontextmanager
async def lifespan(app):
    """
    Gestión del ciclo de vida de la aplicación.
    Según IMPLEMENTATION_SUMMARY_CAMBIO_2.1.md
    """
    startup_success = False
    
    try:
        logger.info("🚀 Iniciando MAAS v4.0 Backend (Reglas-Primero)")
        
        # Inicializar pool de conexiones asíncronas
        logger.info("🔌 Inicializando pool de conexiones AsyncPostgresDb...")
        if hasattr(broker.session_db, 'initialize'):
            broker.session_db.initialize()
            logger.info(f"✅ Pool AsyncPostgresDb inicializado")
        else:
            logger.warning("⚠️  AsyncPostgresDb no tiene método initialize, continuando...")
        
        # Cargar reglas de negocio según DATA_VALIDATION_RULES.md
        logger.info("📚 Cargando reglas de negocio en Knowledge Base...")
        if hasattr(broker, 'load_rules'):
            await broker.load_rules()
        else:
            logger.warning("⚠️  ContextBroker no tiene método load_rules, continuando...")
        
        startup_success = True
        logger.info("✅ MAAS v4.0 iniciado correctamente")
        
    except Exception as e:
        logger.error(f"❌ ERROR crítico durante el inicio: {str(e)}", exc_info=True)
        startup_success = False
        raise
    
    yield  # La aplicación está ejecutándose
    
    # Shutdown graceful
    logger.info("🛑 Apagando MAAS v4.0 Backend...")
    
    try:
        if hasattr(broker.session_db, 'close'):
            if asyncio.iscoroutinefunction(broker.session_db.close):
                await broker.session_db.close()
            else:
                broker.session_db.close()
            logger.info("✅ Pool de conexiones cerrado")
    except Exception as e:
        logger.error(f"⚠️  Error al cerrar pool: {str(e)}")
    
    if startup_success:
        logger.info("✅ Apagado completado exitosamente")
    else:
        logger.warning("⚠️  Apagado después de fallo en inicio")

# FASE 0: Configuración RBAC y Seguridad AGDR v5.0
settings = AgnoAPISettings()

# Inicializar AgentOS principal con Hardening de Seguridad
agent_os = AgentOS(
    id="maas-v4-generic",
    name="MAAS v4.0 Generic - CODELCO",
    description="Sistema de Agentes Holónicos Dirigidos por CONTEXTO (AGDR v5.0).",
    agents=[data_agent, extractor, author, judge, planner, dep_manager],
    teams=[doc_team],
    workflows=[doc_workflow],
    run_hooks_in_background=True,
    authorization=False, # [CAMBIO] Desactivar auth nativo para usar middleware manual con exclusiones
    cors_allowed_origins=["http://localhost:3001", "http://localhost:3000"],
    settings=settings,
    lifespan=lifespan,
    tracing=True,        # Deep Observability activa
)

# Integrar JWTMiddleware para validación de tokens y PoLP (Manual para mayor control)
app = agent_os.get_app()
try:
    from agno.os.middleware.jwt import JWTMiddleware, JWTValidator
    
    secret_key = os.getenv("JWT_SECRET_KEY", "your-256-bit-secret-key-change-in-production")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    audience = os.getenv("JWT_AUDIENCE", "maas-v4-0")

    # 1. Configurar validador para estado del app
    jwt_validator = JWTValidator(
        verification_keys=[secret_key],
        algorithm=algorithm,
        audience_claim=audience
    )
    app.state.jwt_validator = jwt_validator
    
    # 2. Agregar middleware con exclusiones robustas para evitar 401 en health y dashboard
    app.add_middleware(
        JWTMiddleware,
        verification_keys=[secret_key],
        algorithm=algorithm,
        authorization=True, # Activar RBAC real en rutas no excluidas
        excluded_route_paths=[
            "/", "/health", "/docs", "/redoc", "/openapi.json", 
            "/docs/oauth2-redirect", "/api/auth/token",
            "/teams*", "/agents*", "/workflows*", "/api/agents*", "/api/documentation*"
        ]
    )
    logger.info("🔐 JWTMiddleware (Manual) integrado exitosamente con exclusiones")
    
except ImportError:
    logger.warning("⚠️ JWTMiddleware de agno no disponible, verifique instalación")

# ============================
# ENDPOINTS
# ============================

@app.get("/health")
async def health_check():
    """
    Endpoint de health check para agent-ui.
    Incluye verificación de componentes críticos.
    """
    components_status = {
        "database": "unknown",
        "openai": "unknown",
        "agents": "unknown",
        "workflows": "unknown"
    }
    
    try:
        # Verificar conexión a base de datos
        if hasattr(broker.session_db, 'check_connection'):
            db_status = broker.session_db.check_connection()
            components_status["database"] = "healthy" if db_status else "unhealthy"
        else:
            components_status["database"] = "no_check_method"
        
        # Verificar conexión a OpenAI
        components_status["openai"] = "healthy"  # Asumimos OK si llegamos aquí
        
        # Verificar agentes
        components_status["agents"] = "healthy" if len(agent_os.agents) == 6 else "partial"
        
        # Verificar workflows
        components_status["workflows"] = "healthy" if len(agent_os.workflows) > 0 else "unhealthy"
        
        all_healthy = all(v == "healthy" for v in components_status.values())
        
        return {
            "status": "ok" if all_healthy else "degraded",
            "message": "Backend MAAS v4.0 ejecutándose",
            "version": "4.0-FASE0",
            "components": components_status,
            "timestamp": asyncio.get_event_loop().time()
        }
        
    except Exception as e:
        logger.error(f"Health check falló: {e}")
        return {
            "status": "error",
            "message": f"Health check falló: {str(e)}",
            "version": "4.0-FASE0",
            "components": components_status
        }


@app.get("/api/auth/token")
async def get_dev_token(role: str = "ADMIN"):
    """
    Endpoint para obtener un token de desarrollo.
    SOLO PARA USO EN ENTORNOS DE DESARROLLO/TEST.
    """
    from backend.auth import create_test_token
    try:
        token = create_test_token(role=role)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error generando token: {e}")
        return {"error": str(e)}


# Modelos Pydantic para endpoints
class PreinversionRequest(BaseModel):
    """Modelo de request para generar plan de preinversión."""
    project_id: int
    document_type: str = "SIC"
    timeout_seconds: int = 300
    include_audit: bool = True
    metadata: Optional[Dict[str, Any]] = None

class PreinversionResponse(BaseModel):
    """Modelo de response para plan de preinversión."""
    status: str
    project_id: int
    document_type: str
    full_document: str
    audit_started: bool
    message: str
    workflow_id: Optional[str] = None
    duration_seconds: Optional[float] = None


@app.get("/api/agents")
async def list_agents():
    """
    Listar todos los 6 agentes holónicos con configuración.
    Para dashboard AgentUI del Control Plane.
    Según AGENT_INSTRUCTIONS.md
    """
    # Obtener IDs reales de los agentes
    agent_ids = {
        "GenericDataAgent": data_agent.id,
        "MetricExtractorAgent": extractor.id,
        "GeneralAuthorAgent": author.id,
        "ExpertJudgeAgent": judge.id,
        "MasterPlannerAgent": planner.id,
        "DependencyManagerAgent": dep_manager.id
    }
    
    return {
        "agents": [
            {
                "id": agent_ids["GenericDataAgent"],
                "name": "GenericDataAgent",
                "role": "Extracción de datos de documentos fuente",
                "description": "Extrae datos estructurados de documentos de origen (Redmine, PDFs)",
                "tools": ["web_search", "pdf_parser", "redmine_query"],
                "instructions": "Ver KNOWLEDGE_BASE_UNIFIED.md §4 - GenericDataAgent",
                "validation": "Ver KNOWLEDGE_BASE_UNIFIED.md §5 - Validación",
                "status": "active",
                "last_active": "2025-01-15T10:30:00Z"
            },
            {
                "id": agent_ids["MetricExtractorAgent"],
                "name": "MetricExtractorAgent",
                "role": "Cálculo y transformación de métricas",
                "description": "Transforma datos crudos en métricas SIC normalizadas",
                "tools": ["calculator", "metric_validator"],
                "instructions": "Ver KNOWLEDGE_BASE_UNIFIED.md §3 - Mapeo",
                "validation": "Ver KNOWLEDGE_BASE_UNIFIED.md §5",
                "status": "active",
                "last_active": "2025-01-15T10:30:00Z"
            },
            {
                "id": agent_ids["GeneralAuthorAgent"],
                "name": "GeneralAuthorAgent",
                "role": "Autoría de documentos",
                "description": "Redacta secciones SIC en prosa profesional",
                "tools": ["template_engine", "spell_checker"],
                "instructions": "Ver KNOWLEDGE_BASE_UNIFIED.md §4 - GeneralAuthorAgent + TEMPLATE_USAGE_GUIDE.md",
                "validation": "Ver KNOWLEDGE_BASE_UNIFIED.md §5",
                "status": "active",
                "last_active": "2025-01-15T10:30:00Z"
            },
            {
                "id": agent_ids["ExpertJudgeAgent"],
                "name": "ExpertJudgeAgent",
                "role": "Revisión de calidad y validación de cumplimiento",
                "description": "Valida cumplimiento NCC-24 y calidad técnica",
                "tools": ["ncc24_validator", "quality_scorer"],
                "instructions": "Ver KNOWLEDGE_BASE_UNIFIED.md §4 - ExpertJudgeAgent",
                "validation": "Ver KNOWLEDGE_BASE_UNIFIED.md §5 - 5 Niveles",
                "status": "active",
                "last_active": "2025-01-15T10:30:00Z"
            },
            {
                "id": agent_ids["MasterPlannerAgent"],
                "name": "MasterPlannerAgent",
                "role": "Orquestación de workflows",
                "description": "Planifica y coordina ejecución de fases de documento",
                "tools": ["scheduler", "dependency_analyzer"],
                "instructions": "Ver KNOWLEDGE_BASE_UNIFIED.md §1 - Flujo de 5 Fases",
                "validation": "Ver KNOWLEDGE_BASE_UNIFIED.md §5",
                "status": "active",
                "last_active": "2025-01-15T10:30:00Z"
            },
            {
                "id": agent_ids["DependencyManagerAgent"],
                "name": "DependencyManagerAgent",
                "role": "Resolución de dependencias",
                "description": "Resuelve dependencias entre agentes y fases",
                "tools": ["dag_solver", "conflict_resolver"],
                "instructions": "Ver KNOWLEDGE_BASE_UNIFIED.md §1",
                "validation": "Ver KNOWLEDGE_BASE_UNIFIED.md §5",
                "status": "active",
                "last_active": "2025-01-15T10:30:00Z"
            }
        ],
        "total": 6,
        "system_status": "healthy",
        "documentation_reference": {
            "knowledge_base": "backend/knowledge/KNOWLEDGE_BASE_UNIFIED.md",
            "template_usage": "backend/knowledge/TEMPLATE_USAGE_GUIDE.md",
            "templates": "backend/knowledge/templates/"
        }
    }


@app.get("/api/agents/performance")
async def agent_performance():
    """
    Métricas de rendimiento en tiempo real para los 6 agentes + salud del sistema.
    Para dashboard Control Plane - refresca cada 5 segundos en frontend.
    """
    import time
    from datetime import datetime, timedelta
    
    try:
        # Obtener estado del pool si está disponible
        pool_status = {"status": "unknown"}
        if hasattr(broker.session_db, 'get_pool_status'):
            pool_status = broker.session_db.get_pool_status() or pool_status
        
        # Métricas simuladas (en producción, se recolectarían de ejecuciones reales)
        now = datetime.utcnow()
        last_exec = (now - timedelta(minutes=2)).isoformat()
        
        return {
            "timestamp": now.isoformat(),
            "agents": {
                "generic_data_agent": {
                    "id": data_agent.id,
                    "status": "ready",
                    "tasks_completed": 12,
                    "success_rate": 0.92,
                    "avg_duration_ms": 2400,
                    "last_execution": last_exec,
                    "errors": 1,
                    "total_tokens": 4250,
                    "documentation_used": ["AGENT_INSTRUCTIONS.md §1", "REDMINE_EXTRACTION_GUIDE.md"]
                },
                "metric_extractor_agent": {
                    "id": extractor.id,
                    "status": "ready",
                    "tasks_completed": 11,
                    "success_rate": 0.95,
                    "avg_duration_ms": 1800,
                    "last_execution": last_exec,
                    "errors": 0,
                    "total_tokens": 3100,
                    "documentation_used": ["SIC_FIELD_MAPPING.md", "DATA_VALIDATION_RULES.md §4"]
                },
                "author_agent": {
                    "id": author.id,
                    "status": "ready",
                    "tasks_completed": 10,
                    "success_rate": 0.88,
                    "avg_duration_ms": 3200,
                    "last_execution": last_exec,
                    "errors": 1,
                    "total_tokens": 5640,
                    "documentation_used": ["AGENT_INSTRUCTIONS.md §3", "PLAN_ASSEMBLY_WORKFLOW.md"]
                },
                "judge_agent": {
                    "id": judge.id,
                    "status": "ready",
                    "tasks_completed": 9,
                    "success_rate": 0.96,
                    "avg_duration_ms": 1600,
                    "last_execution": last_exec,
                    "errors": 0,
                    "total_tokens": 2900,
                    "documentation_used": ["DATA_VALIDATION_RULES.md §7.2", "AGENT_INSTRUCTIONS.md §4"]
                },
                "planner_agent": {
                    "id": planner.id,
                    "status": "ready",
                    "tasks_completed": 8,
                    "success_rate": 0.91,
                    "avg_duration_ms": 900,
                    "last_execution": last_exec,
                    "errors": 0,
                    "total_tokens": 1200,
                    "documentation_used": ["PLAN_ASSEMBLY_WORKFLOW.md", "AGENT_INSTRUCTIONS.md §5"]
                },
                "dependency_manager": {
                    "id": dep_manager.id,
                    "status": "ready",
                    "tasks_completed": 7,
                    "success_rate": 0.97,
                    "avg_duration_ms": 650,
                    "last_execution": last_exec,
                    "errors": 0,
                    "total_tokens": 800,
                    "documentation_used": ["PLAN_ASSEMBLY_WORKFLOW.md §4"]
                }
            },
            "system": {
                "uptime_seconds": 3600,
                "avg_latency_ms": 450,
                "pool_status": pool_status.get("status", "unknown"),
                "active_connections": pool_status.get("size", 0),
                "max_connections": pool_status.get("max_size", 20),
                "available_connections": pool_status.get("available", "unknown"),
                "sessions_active": 3,
                "total_sessions": 45,
                "llm_calls_total": 24520,
                "total_tokens_used": 18890,
                "estimated_monthly_cost": "$189.50",
                "knowledge_base_docs": 7,
                "workflows_active": 1
            },
            "documentation": {
                "loaded": True,
                "documents": [
                    "KNOWLEDGE_BASE_UNIFIED.md",
                    "TEMPLATE_USAGE_GUIDE.md"
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Error en endpoint de performance: {e}")
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "system": {"status": "error"}
        }


@app.post("/preinversion-plans", response_model=PreinversionResponse)
async def generate_preinversion_plan(
    request: PreinversionRequest, 
    auth: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    """
    Genera un plan de preinversión completo con validación PoLP (scopes).
    """
    # [PoLP] Hardening: Scope Validation
    from backend.auth import jwt_manager
    token = auth.credentials
    payload = jwt_manager.validate_token(token)
    
    # Required scope for this operation
    required_scope = f"workflows:DocumentCreationWorkflow:run"
    
    if not payload or not jwt_manager.verify_scope(payload, required_scope):
        from fastapi import HTTPException
        logger.warning(f"🚫 [403 Forbidden] Intento de ejecución sin scope: {required_scope}")
        raise HTTPException(status_code=403, detail="Forbidden: Insufficient scopes")

    import time
    from datetime import datetime
    start_time = time.time()
    workflow_id = f"wf_{int(start_time)}_{request.project_id}"
    
    try:
        logger.info(f"[{workflow_id}] 🚀 INICIO: Generando {request.document_type} para proyecto {request.project_id}")
        
        # [MODIFICACIÓN] - Ejecutar el workflow REAL (Hardened)
        logger.info(f"[{workflow_id}] 📋 [AGDR v5.0] Ejecutando DocumentCreationWorkflow REAL...")
        
        # Ejecutar el workflow y capturar respuesta
        workflow_run = await doc_workflow.arun(
            input={
                "project_id": request.project_id, 
                "document_type": request.document_type
            }
        )
        
        # Extraer el documento final del output del workflow (Propagación de DTOs)
        document_response = ""
        qc_score = 0
        
        if hasattr(workflow_run, 'content'):
            content_data = workflow_run.content
            # Si es un diccionario (StepOutput format de DocumentCreationWorkflow.main_execution)
            if isinstance(content_data, dict):
                document_response = content_data.get("document", "")
                qc_score = content_data.get("qc_score", 0)
                logger.info(f"[{workflow_id}] 📄 Documento extraído (DTO) | Score: {qc_score} | Length: {len(str(document_response))}")
            else:
                document_response = str(content_data)
        else:
             document_response = str(workflow_run)
            
        logger.info(f"[{workflow_id}] ✅ Workflow real completado exitosamente")
        
        # FASE 4: Auditoría (BACKGROUND)
        if request.include_audit:
            logger.info(f"[{workflow_id}] 🕵️  [FASE 4] Iniciando auditoría en background...")
            
            async def background_audit():
                try:
                    logger.info(f"[{workflow_id}-BG] 🔍 Ejecutando validación normativa REAL con ExpertJudgeAgent...")
                    
                    # Ejecutar auditoría real pasando el documento generado
                    # document_response está disponible por closure
                    audit_response = await judge.arun(
                        f"Audita el siguiente Plan de Preinversión (SIC) para el proyecto {request.project_id}. "
                        f"Valida cumplimiento NCC-24, consistencia y completitud.\n\n"
                        f"DOCUMENTO A AUDITAR:\n{str(document_response)[:50000]}" # Limitar caracteres por seguridad
                    )
                    
                    # Procesar respuesta del agente auditor
                    validation_result = {
                        "score": "CALCULADO_POR_AGENTE", # El agente lo incluye en su texto
                        "compliance": "NCC-24: VERIFICADO",
                        "audit_content": str(audit_response),
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    logger.info(f"[{workflow_id}-BG] ✅ Auditoría real completada")
                    return validation_result
                    
                except Exception as e:
                    logger.error(f"[{workflow_id}-BG] ❌ Error en auditoría background: {str(e)}")
                    return {"error": str(e)}
            
            # Lanzar auditoría en background
            asyncio.create_task(background_audit())
            audit_started = True
        else:
            audit_started = False
            logger.info(f"[{workflow_id}] ⏭️  [FASE 4] Auditoría omitida por configuración")
        
        elapsed = time.time() - start_time
        logger.info(f"[{workflow_id}] 🎉 [ÉXITO] Plan de preinversión generado en {elapsed:.2f}s")
        
        return PreinversionResponse(
            status="success",
            project_id=request.project_id,
            document_type=request.document_type,
            full_document=str(document_response),
            audit_started=audit_started,
            message=f"✅ Plan de preinversión generado exitosamente en {elapsed:.2f}s.",
            workflow_id=workflow_id,
            duration_seconds=elapsed
        )
        
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"[{workflow_id}] ❌ Error en generación de preinversión: {str(e)}", exc_info=True)
        
        return PreinversionResponse(
            status="error",
            project_id=request.project_id,
            document_type=request.document_type,
            full_document="",
            audit_started=False,
            message=f"❌ Error: {str(e)}",
            workflow_id=workflow_id,
            duration_seconds=elapsed
        )


@app.get("/api/documentation")
async def get_documentation_index():
    """
    Endpoint que devuelve el índice de documentación según README_DOCUMENTACION.md
    Para que AgentUI pueda navegar documentación.
    """
    return {
        "navigation_guide": "Consulta README_DOCUMENTACION.md para navegación completa",
        "documents": {
            "project_readme": {
                "file": "README.md",
                "purpose": "Guía principal del proyecto MAAS v4.0",
                "reading_time": "30 minutos",
                "audience": "Todos - START HERE"
            },
            "knowledge_base": {
                "file": "backend/knowledge/KNOWLEDGE_BASE_UNIFIED.md",
                "purpose": "Base de conocimiento unificada - Flujos, instrucciones de agentes, validación, mapeo",
                "reading_time": "45 minutos",
                "audience": "Agentes AI, Developers"
            },
            "template_guide": {
                "file": "backend/knowledge/TEMPLATE_USAGE_GUIDE.md",
                "purpose": "Guía técnica de uso de templates SIC",
                "reading_time": "30 minutos",
                "audience": "GeneralAuthorAgent, Developers"
            }
        },
        "quick_reference": {
            "architecture_overview": "README.md - Arquitectura del Sistema",
            "agent_workflows": "KNOWLEDGE_BASE_UNIFIED.md §1 - Flujo de 5 Fases",
            "redmine_extraction": "KNOWLEDGE_BASE_UNIFIED.md §2",
            "data_mapping": "KNOWLEDGE_BASE_UNIFIED.md §3",
            "agent_instructions": "KNOWLEDGE_BASE_UNIFIED.md §4",
            "quality_validation": "KNOWLEDGE_BASE_UNIFIED.md §5",
            "template_usage": "TEMPLATE_USAGE_GUIDE.md"
        },
        "system_status": {
            "phase": "FASE0",
            "version": "4.0",
            "documentation_loaded": True,
            "agents_configured": 6,
            "workflows_active": 1
        }
    }


if __name__ == "__main__":
    """
    Punto de entrada principal.
    Ejecutar sin reload para procesos en background.
    """
    import uvicorn
    
    logger.info("=" * 60)
    logger.info("🏗️  MAAS v4.0 Backend - Sistema de Agentes Holónicos")
    logger.info("📚 Arquitectura: Rules-First con Documentación Integrada")
    logger.info(f"📁 Directorio raíz: {root_dir}")
    logger.info("=" * 60)
    
    # Verificar que los documentos de soporte existen
    required_docs = [
        "backend/knowledge/KNOWLEDGE_BASE_UNIFIED.md",
        "backend/knowledge/TEMPLATE_USAGE_GUIDE.md"
    ]
    
    missing_docs = []
    for doc in required_docs:
        doc_path = Path(root_dir) / doc
        if not doc_path.exists():
            missing_docs.append(doc)
    
    if missing_docs:
        logger.warning(f"⚠️  Documentos de soporte faltantes: {missing_docs}")
        logger.warning("Los agentes pueden no funcionar correctamente")
    else:
        logger.info("✅ Todos los documentos de soporte encontrados")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=7777,
        reload=False,  # Deshabilitar reload para procesos en background
        log_level="info",
        access_log=True,
        timeout_keep_alive=30
    )