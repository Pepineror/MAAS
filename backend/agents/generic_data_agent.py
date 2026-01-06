"""
GenericDataAgent - Adquisición de Datos y Hechos

Holón de Extracción: Recupera datos de fuentes externas (Redmine) y del repositorio 
de hechos del proyecto. Analiza patrones, relaciones entre issues, y construye la 
vista inicial del proyecto.

RESPONSABILIDADES:
    1. Conectar y listar proyectos en Redmine
    2. Recuperar issues y metadatos específicos
    3. Analizar relaciones entre issues (dependencias, bloqueadores)
    4. Buscar patrones similares en el Knowledge Base
    5. Proporcionar vista integral del contexto del proyecto

PATRÓN DE EJECUCIÓN:
    THINK → SEARCH KNOWLEDGE → ANALYZE REDMINE → STRUCTURE

HERRAMIENTAS UTILIZADAS:
    - RedmineTools: Acceso directo a Redmine (proyectos, issues, metadata)
    - RedmineKnowledgeTools: Búsqueda de issues similares y patrones previos
    - ReasoningTools: Planificación y estructuración del análisis
    - KnowledgeTools: Acceso a Knowledge Base de hechos del proyecto

SALIDA DEL AGENTE:
    - Lista de proyectos disponibles en Redmine
    - Issues clave con metadata completa
    - Relaciones y dependencias entre issues
    - Patrones identificados en datos históricos
"""

from typing import Optional
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools.knowledge import KnowledgeTools
from backend.tools.custom_tools import (
    RedmineTools,
    RedmineKnowledgeTools
)
from backend.core.context_broker import ContextBroker


class GenericDataAgent(Agent):
    """
    Holón de Extracción: Adquisición de datos brutos con herramientas Redmine mejoradas.
    
    Este agente es responsable de:
    - Conectar a Redmine y obtener información de proyectos
    - Extraer issues con todos sus metadatos
    - Analizar relaciones y dependencias entre issues
    - Buscar patrones similares en datos históricos
    - Proporcionar un contexto completo para otros agentes
    
    Utiliza un patrón Think→Search→Analyze:
    1. THINK: Planifica qué datos necesita extraer
    2. SEARCH KNOWLEDGE: Busca issues similares y patrones previos
    3. ANALYZE: Extrae datos de Redmine y analiza relaciones
    4. STRUCTURE: Organiza datos en formato comprensible
    """
    
    def __init__(self, broker: ContextBroker, model: Optional[OpenAIChat] = None, **kwargs):
        # Initialize Redmine tools for data extraction
        redmine_tools = RedmineTools()
        redmine_kb_tools = RedmineKnowledgeTools(
            knowledge_base=broker.project_kb,
            redmine_tools=redmine_tools
        )
        
        super().__init__(
            id="generic-data-agent",
            name="GenericDataAgent",
            role="Adquisición de Datos y Hechos",
            model=model or OpenAIChat(id="gpt-4o"),
            knowledge=broker.project_kb,
            search_knowledge=True,
            tools=[
                redmine_tools,           # Direct Redmine access
                redmine_kb_tools,        # Redmine + Knowledge integration
                ReasoningTools(add_instructions=True),
                KnowledgeTools(knowledge=broker.project_kb)
            ],
            description=(
                "Recupera datos de fuentes externas (Redmine) y del repositorio de hechos del proyecto "
                "con análisis de patrones. Proporciona la visión inicial y contextual de los datos."
            ),
            instructions=[
                "═══════════════════════════════════════════════════════════",
                "FLUJO DE EXTRACCIÓN DE DATOS",
                "═══════════════════════════════════════════════════════════",
                "",
                "FASE 1 - PLANIFICACIÓN ESTRATÉGICA (Planner):",
                "  • Define qué datos necesitas extraer del proyecto",
                "  • Identifica proyectos y issues objetivo",
                "  • Planifica el análisis de relaciones",
                "  • Usa ReasoningTools para estructurar tu plan",
                "",
                "FASE 2 - ADQUISICIÓN DE DATOS REDMINE (Executor):",
                "  2.1. list_projects()",
                "       → Obtén lista de todos los proyectos disponibles",
                "       → Identifica proyectos de interés",
                "",
                "  2.2. get_project_issues(project_id)",
                "       → Extrae issues del proyecto objetivo",
                "       → Nota: Puedes filtrar por estado, prioridad, etc",
                "",
                "  2.3. get_issue_details(issue_id)",
                "       → Obtén detalles completos de cada issue",
                "       → Incluye custom fields, descripción, metadata",
                "",
                "  2.4. get_issue_relations(issue_id)",
                "       → Analiza dependencias (blocks, depends_on, etc)",
                "       → Identifica issues relacionados",
                "",
                "  2.5. analyze_issue_context(issue_id)",
                "       → Extrae contexto y cambios recientes",
                "       → Revisa historia de modificaciones",
                "",
                "FASE 3 - VERIFICACIÓN Y METACOGNICIÓN (Verifier):",
                "  3.1. Auto-Verificación (PEV):",
                "       • ¿Los datos extraídos son suficientes para un Plan SIC?",
                "       • Verifica integridad: ¿Existen costos (SIC 16)? ¿Riesgos (SIC 03)?",
                "       • Si faltan datos críticos, REINTENTA con búsqueda alternativa o marca explícitamente el GAP.",
                "",
                "  3.2. Reflexión Metacognitiva:",
                "       • ¿Es confiable este dato? (Ej. Un presupuesto de $0 para una mina es sospechoso).",
                "       • ¿Necesito escalar esto a un humano? (Si hay contradicciones graves).",
                "",
                "FASE 4 - BÚSQUEDA EN KNOWLEDGE BASE (Search):",
                "  • search_similar_issues(): Encuentra issues similares en histórico",
                "  • analyze_issue_patterns(): Identifica patrones comunes",
                "  • Busca mejores prácticas y soluciones previas",
                "  • Consulta plantillas SIC relevantes",
                "",
                "FASE 5 - ANÁLISIS Y ESTRUCTURACIÓN (Analyze):",
                "  • Analiza relaciones entre issues para entender flujos",
                "  • Identifica bloqueadores y dependencias críticas",
                "  • Estructura datos en formato jerárquico",
                "  • Marca datos incompletos como [PENDIENTE]",
                "  • Usa ReasoningTools para análisis complejo",
                "",
                "FASE 6 - SÍNTESIS (Summary):",
                "  • Proporciona resumen del estado actual del proyecto",
                "  • Lista issues clave con prioridades",
                "  • Identifica riesgos y bloqueadores",
                "  • Cita fuentes (issues, custom fields)",
                "  • Formato markdown bien estructurado",
                "  • Include section: 'Quality Gaps' identificados en Fase 3",
                "",
                "═══════════════════════════════════════════════════════════",
                "DIRECTRICES GENERALES",
                "═══════════════════════════════════════════════════════════",
                "",
                "✓ SIEMPRE usa RedmineTools para obtener datos frescos",
                "✓ Aplica el ciclo PEV (Plan-Execute-Verify) en cada paso crítico",
                "✓ Cita explícitamente todas las fuentes (issue #ID, campo)",
                "✓ Si datos faltan tras verificación, marca [PENDIENTE] NO null",
                "✓ Mantén lenguaje formal y estructurado",
                "✓ Incluye timestamps y estados actuales",
                "✓ Estructura jerárquica clara (# Proyecto > ## Issue > ### Detalles)",
                "✓ Usa tablas para comparaciones y listas",
                "✓ Analiza dependencias entre issues",
                "✓ Identifica patrones repetidos"
            ],
            markdown=True,
            **kwargs
        )
