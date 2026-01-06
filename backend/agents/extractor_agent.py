"""
ExtractorAgent: Specialized agent for extracting metrics and context from Redmine
Integrates Redmine tools, knowledge base, and source text tools for comprehensive data analysis
"""

from typing import Optional
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools.knowledge import KnowledgeTools
from backend.tools.custom_tools import (
    SourceTextTools,
    RedmineTools,
    RedmineKnowledgeTools,
    RedmineReasoningTools
)
from backend.knowledge.redmine_kb import RedmineKnowledgeBase
import asyncio


class DataIngestorAgent(Agent):
    """
    Holón de Ingestión: Adquisición asíncrona de datos desde Redmine.
    
    Responsabilidades:
    - Obtener proyectos disponibles en Redmine
    - Recuperar issues y metadatos
    - Almacenar en caché datos frecuentemente accedidos
    """
    def __init__(self, **kwargs):
        redmine_tools = RedmineTools()
        
        super().__init__(
            id="data-ingestor-agent",
            name="DataIngestor",
            role="Adquisición Asíncrona de Datos de Redmine",
            model=OpenAIChat(id="gpt-4o"),
            tools=[redmine_tools],
            description=(
                "Recupera datos de Redmine (issues, wikis, archivos, metadatos) de forma asíncrona. "
                "Coordina la obtención de datos para otros agentes."
            ),
            instructions=[
                "Usa RedmineTools para listar proyectos disponibles.",
                "Extrae metadatos de issues incluyendo custom fields.",
                "Mantén caché local de datos recientemente consultados.",
                "Identifica relaciones entre issues para entender dependencias.",
                "Reporta cualquier error de conexión o autenticación con Redmine."
            ],
            markdown=True,
            **kwargs
        )

    async def ingest_project_data(self, project_id: int):
        """Implementation of async data acquisition"""
        print(f"Ingesting data for project {project_id}...")
        await asyncio.sleep(1)  # Placeholder for async Redmine API calls
        return {"status": "success", "project_id": project_id}


class ExtractorAgent(Agent):
    """
    Holón de Extracción: Transformación de datos en métricas y contexto semántico.
    
    Responsabilidades:
    - Extraer métricas estructuradas de datos crudos
    - Comprimir contexto semántico
    - Mapear datos de Redmine a esquemas Pydantic
    - Usar ReasoningTools para análisis profundo
    
    Patrón: Think → Search Knowledge → Analyze → Extract
    """
    def __init__(
        self,
        knowledge_base: Optional[RedmineKnowledgeBase] = None,
        **kwargs
    ):
        # Initialize Redmine tools for data extraction
        redmine_tools = RedmineTools()
        redmine_kb_tools = RedmineKnowledgeTools(
            knowledge_base=knowledge_base,
            redmine_tools=redmine_tools
        )
        redmine_reasoning = RedmineReasoningTools(redmine_tools=redmine_tools)
        
        super().__init__(
            id="extractor-agent",
            name="ExtractorAgent",
            role="Extractor de Métricas y Contexto Semántico",
            model=OpenAIChat(id="gpt-4o"),
            knowledge=knowledge_base,
            search_knowledge=True,
            tools=[
                redmine_tools,              # Direct Redmine access
                redmine_kb_tools,           # Redmine + Knowledge integration
                redmine_reasoning,          # Pattern analysis
                SourceTextTools(),          # Text extraction & evidence citation
                ReasoningTools(add_instructions=True),
                KnowledgeTools(knowledge=knowledge_base) if knowledge_base else None
            ],
            description=(
                "Extrae métricas estructuradas y comprime contexto semántico de datos de Redmine. "
                "Mapea información a esquemas Pydantic siguiendo reglas de negocio. "
                "Usa ReasoningTools para estructuración y SourceTextTools para evidencia."
            ),
            instructions=[
                # Phase 1: Redmine Data Acquisition
                "PASO 1 - ADQUISICIÓN DE DATOS REDMINE:",
                "  1.1. Usa list_projects() para identificar proyectos disponibles.",
                "  1.2. Usa get_project_issues() para obtener issues del proyecto objetivo.",
                "  1.3. Para cada issue, extrae detalles completos con get_issue_details().",
                "  1.4. Analiza relaciones de issues con get_issue_relations() y analyze_issue_context().",
                "",
                # Phase 2: Knowledge Base Consultation
                "PASO 2 - CONSULTA DE KNOWLEDGE BASE (Consejo #12):",
                "  2.1. Busca plantillas SIC relevantes para el contexto del issue.",
                "  2.2. Consulta reglas de negocio y validaciones aplicables.",
                "  2.3. Usa search_similar_issues() para encontrar patrones previos.",
                "",
                # Phase 3: Reasoning & Structuring
                "PASO 3 - RAZONAMIENTO Y ESTRUCTURACIÓN:",
                "  3.1. Usa ReasoningTools para planificar la extracción de métricas.",
                "  3.2. Usa RedmineReasoningTools para analizar dependencias e impactos.",
                "  3.3. Estructura datos complejos en objetos Pydantic.",
                "",
                # Phase 4: Evidence Extraction
                "PASO 4 - EXTRACCIÓN DE EVIDENCIA:",
                "  4.1. Usa SourceTextTools para extraer fragmentos de evidencia.",
                "  4.2. Cita las fuentes (issues de Redmine, campos custom).",
                "  4.3. Marca fragmentos con nivel de confianza.",
                "",
                # Phase 5: Validation
                "PASO 5 - VALIDACIÓN:",
                "  5.1. Verifica completitud de campos requeridos.",
                "  5.2. Valida tipos de datos y formatos.",
                "  5.3. Compara contra esquemas del Knowledge Base.",
                "",
                # General Guidelines
                "DIRECTRICES GENERALES:",
                "  - SIEMPRE consulta Knowledge Base antes de extraer métricas.",
                "  - Usa patrones de issues similares para mantener consistencia.",
                "  - Cita fuentes explícitamente.",
                "  - Si datos están faltantes, marca como [PENDIENTE] no como null.",
                "  - Mantén lenguaje formal y técnico."
            ],
            markdown=True,
            **kwargs
        )
        self.knowledge_base = knowledge_base

    def get_evidence(self, query: str, project_id: int):
        """
        Consulta de Contexto Obligatoria (Consejo #12 de la documentación)
        Busca evidencia en Knowledge Base con metadatos del proyecto
        """
        if not self.knowledge_base:
            return {"error": "Knowledge base not configured"}
        
        # Search kb with project-specific metadata
        results = self.knowledge_base.search_with_metadata(
            query=query,
            project_id=project_id
        )
        # Results should include source citations and confidence scores
        return results
