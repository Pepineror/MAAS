"""
MetricExtractorAgent - Transformación de Datos a Métricas Estructuradas

Holón de Extracción: Transforma datos no estructurados en métricas Pydantic 
siguiendo las reglas de negocio registradas. Integra extracción de Redmine con 
validación contra esquemas definidos.

RESPONSABILIDADES:
    1. Consultar Knowledge Base para esquemas y validaciones
    2. Extraer datos de Redmine (directamente)
    3. Analizar dependencias e impactos de datos
    4. Estructurar datos en objetos Pydantic válidos
    5. Extraer y citar evidencia
    6. Validar conformidad con reglas de negocio

PATRÓN DE EJECUCIÓN:
    SEARCH RULES → ANALYZE DATA → STRUCTURE → EXTRACT EVIDENCE → VALIDATE

HERRAMIENTAS UTILIZADAS:
    - RedmineTools: Extracción directa de datos de Redmine (CRÍTICO - faltaba en v1)
    - RedmineReasoningTools: Análisis de dependencias e impactos
    - SourceTextTools: Extracción de evidencia con citas exactas
    - ReasoningTools: Estructuración compleja de datos
    - KnowledgeTools: Validación contra esquemas y reglas

SALIDA DEL AGENTE:
    - Objetos Pydantic validados
    - Evidencia citada (source + línea)
    - Nivel de confianza por campo
    - Validación de cumplimiento normativo
"""

from typing import Optional, List, Dict, Any
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools.knowledge import KnowledgeTools
from backend.agents.schemas import FinancialMetricsSchema, ExtractedMetrics
from backend.core.context_broker import ContextBroker
from backend.tools.custom_tools import (
    SourceTextTools,
    RedmineTools,
    RedmineReasoningTools
)

class MetricExtractorAgent(Agent):
    """
    Holón de Extracción: Transformación de datos a métricas Pydantic (AGDR v5.0).
    
    Implementa el "Mandato del Sistema":
    - Forzar salida tipada para métricas críticas (CAPEX, OPEX, ETP).
    - Patrón: Ensemble Decision-Making (Ligero).
    - Almacenamiento en formato JSON.
    """
    
    def __init__(self, broker: ContextBroker, model: Optional[OpenAIChat] = None, **kwargs):
        redmine_tools = RedmineTools()
        redmine_reasoning = RedmineReasoningTools(redmine_tools=redmine_tools)
        
        super().__init__(
            id="metric-extractor-agent",
            name="MetricExtractorAgent",
            role="Extractor de Métricas Financieras (Ensemble)",
            model=model or OpenAIChat(id="gpt-4o"),
            knowledge=broker.rules_kb,
            search_knowledge=True,
            output_schema=ExtractedMetrics, # Forzar Schema Pydantic con FinancialMetricsSchema
            tools=[
                redmine_tools,           
                redmine_reasoning,       
                SourceTextTools(),       
                ReasoningTools(add_instructions=True),
                KnowledgeTools(knowledge=broker.rules_kb)
            ],
            description=(
                "Transforma datos no estructurados en métricas Pydantic (AGDR v5.0). "
                "Utiliza Ensemble Decision-Making para validar cifras críticas."
            ),
            instructions=[
                "Eres el MetricExtractorAgent (Ensemble) v5.0.",
                "Tu objetivo es garantizar que CADA CIFRA tenga una fuente y un nivel de confianza.",
                
                "═══════════════════════════════════════════════════════════",
                "MANDATO AGDR v5.0:",
                "1. EXTRACCIÓN TIPADA: No devuelvas texto narrativo en las métricas. Solo valores numéricos.",
                "2. ENSEMBLE CALCULUS: Si encuentras discrepancias entre issues, calcula un promedio ponderado o selecciona el valor del issue más reciente (mayor ID).",
                "3. ETP CALCULUS: Calcula la Exposición Total del Proyecto (ETP) basándote en la suma de riesgos vs CAPEX.",
                
                "4. FORMATO DE SALIDA (JSON):",
                "Usa estrictamente el `FinancialMetricsSchema` dentro de `ExtractedMetrics`.",
                "  - `van_kusd`, `tir_percent`, `capex_total`: Obligatorios.",
                "  - `op_costs_unit`: Debe ser extraído de proyecciones operativas.",
                
                "═══════════════════════════════════════════════════════════",
                "CRÍTICO: Evita alucinaciones. Si una cifra no existe en Redmine, usa 0.0 y marca confidence_score=0.",
                "═══════════════════════════════════════════════════════════"
            ],
            markdown=True,
            **kwargs
        )
