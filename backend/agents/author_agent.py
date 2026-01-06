"""
GeneralAuthorAgent - Redacción Modular de Documentos

Holón de Creación: Escribe secciones de documentos técnicos basándose en 
las plantillas y guías encontradas en el Knowledge Base. Integra datos 
estructurados con plantillas SIC para generar documentación de calidad.

RESPONSABILIDADES:
    1. Consultar plantillas SIC (01-22) del Knowledge Base
    2. Planificar estructura de secciones
    3. Redactar contenido técnico coherente
    4. Asegurar consistencia con hallazgos previos
    5. Aplicar mejores prácticas de documentación
    6. Buscar patrones similares en issues previos

PATRÓN DE EJECUCIÓN:
    SEARCH TEMPLATES → PLAN STRUCTURE → WRITE SECTIONS → ENSURE CONSISTENCY

HERRAMIENTAS UTILIZADAS:
    - RedmineKnowledgeTools: Búsqueda de mejores prácticas y patrones
    - ReasoningTools: Planificación de estructura y lógica del documento
    - KnowledgeTools: Acceso a plantillas SIC y guías de estilo

SALIDA DEL AGENTE:
    - Documento markdown bien estructurado
    - Secciones SIC (01-22) completas
    - Referencias a issues de Redmine
    - Lenguaje coherente y profesional
"""

from typing import Optional
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools.knowledge import KnowledgeTools
from backend.tools.custom_tools import (
    RedmineKnowledgeTools,
    RedmineTools
)
from backend.core.context_broker import ContextBroker


from backend.agents.schemas import SIC_DTO

class GeneralAuthorAgent(Agent):
    """
    Holón de Creación: Redactor Modular Dirigido por Reglas (AGDR v5.0).
    
    Implementa el "Mandato del Sistema":
    - Adherencia Estricta a la 'PLANTILLA_MAESTRA_SIC_GENERICO.md'.
    - Uso de SIC_DTO para transferencia de contexto eficiente.
    - Mitigación de Context Overflow mediante resumen y truncamiento.
    """
    
    def __init__(self, broker: ContextBroker, model: Optional[OpenAIChat] = None, **kwargs):
        redmine_tools = RedmineTools()
        redmine_kb_tools = RedmineKnowledgeTools(
            knowledge_base=broker.rules_kb,
            redmine_tools=redmine_tools
        )
        
        super().__init__(
            id="general-author-agent",
            name="GeneralAuthorAgent",
            role="Redactor Modular Dirigido por Reglas",
            model=model or OpenAIChat(id="gpt-4o"),
            knowledge=broker.rules_kb,
            search_knowledge=True,
            output_schema=SIC_DTO, # AGDR v5.0 Structured Output
            tools=[
                redmine_kb_tools,        # Find best practices & patterns
                ReasoningTools(add_instructions=True),
                KnowledgeTools(knowledge=broker.rules_kb)
            ],
            description=(
                "Genera contenido SIC (01-22) basándose estrictamente en la Plantilla Maestra. "
                "Produce salidas estructuradas SIC_DTO para optimizar la ventana de contexto."
            ),
            instructions=[
                "Eres el GeneralAuthorAgent (Maker) v5.0.",
                "Tu objetivo es producir el contenido para los 22 SIC siguiendo la 'PLANTILLA_MAESTRA_SIC_GENERICO.md'.",
                
                "═══════════════════════════════════════════════════════════",
                "MANDATO AGDR v5.0:",
                "1. ADHERENCIA ESTRUCTURAL: No alteres índices ni títulos de tablas. Si falta un dato, usa [PENDIENTE].",
                "2. SALIDA ESTRUCTURADA (SIC_DTO):",
                "   - `metadata`: Lista de objetos `KeyValue` {key, value} con parámetros técnicos clave.",
                "   - `key_tables_markdown`: Representa las tablas críticas (ej. Tabla 14-3) en formato Markdown.",
                "   - `summary_markdown`: Aquí debes poner el contenido COMPLETO de la sección en formato Markdown.",
                "     * NOTA: Aunque el nombre diga 'summary', para la generación final requerimos el texto íntegro aquí.",
                
                "3. MITIGACIÓN DE CONTEXTO:",
                "   - No incluyas preámbulos ni explicaciones fuera del Markdown solicitado.",
                "   - Cita fuentes Redmine (issue #ID) directamente en el texto.",
                
                "4. COHERENCIA SECUENCIAL:",
                "   - Si se te pide una sección específica (ej. SIC 16), asume que las métricas financieras necesarias ya fueron extraídas por el MetricExtractorAgent.",
                
                "5. EXCLUSIONES FORMALES (MANDATO AGDR): Para las secciones SIC 07, SIC 08, SIC 09, SIC 13 y SIC 18, si el alcance es de Infraestructura/Servicios, genera el contenido declarando 'No Aplicable' e incluye una justificación formal en el 'Resumen del Capítulo' (ej. 'no fue desarrollado' o 'no se generan variaciones en la base actual').",
                "6. RIESGO A COSTO (ETP): Asegúrate de que el SIC 16 (Costos) recupere y mencione explícitamente la Exposición Total del Proyecto (ETP) calculada en el SIC 03 para justificar la Contingencia.",
                "═══════════════════════════════════════════════════════════",
                "PROHIBIDO: Alucinar datos financieros. Si no hay CAPEX, indica que está en estudio. NUNCA omitas ninguno de los 22 SICs.",
                "═══════════════════════════════════════════════════════════"
            ],
            markdown=True,
            **kwargs
        )

# (ReviewerAgent and PersistAgent removed as they are legacy/redundant with ExpertJudgeAgent)
