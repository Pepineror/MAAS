"""
ExpertJudgeAgent - Auditoría de Calidad y Validación (AGDR v5.0)

Holón de Creación: Valida si el contenido generado cumple con las normas 
(NCC, SGPD) y verifica la veracidad de los datos. Actúa como AgentAsJudge 
realizando auditoría exhaustiva.
"""

from typing import Optional
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools.knowledge import KnowledgeTools
from backend.agents.schemas import FeedbackCritiqueSchema # Schema de Validación AGDR v5.0
from backend.tools.custom_tools import (
    RedmineReasoningTools,
    RedmineTools
)
from backend.core.context_broker import ContextBroker


class ExpertJudgeAgent(Agent):
    """
    Holón de Creación: Validación y Auditoría (AgentAsJudge) con análisis Redmine.
    
    Implementa el "Mandato del Sistema" para AGDR v5.0:
    - Análisis Causal (Bow-Tie, 5 Whys, Ishikawa)
    - Redacción de Lecciones (Anexo CC/DD)
    - Mitigación de Sobrecarga de Iteración (Truncamiento de Historial)
    """
    
    def __init__(self, broker: ContextBroker, model: Optional[OpenAIChat] = None, **kwargs):
        redmine_tools = RedmineTools()
        redmine_reasoning = RedmineReasoningTools(redmine_tools=redmine_tools)
        
        super().__init__(
            id="expert-judge-agent",
            name="ExpertJudgeAgent",
            role="Auditor de Calidad y Cumplimiento (Checker)",
            model=model or OpenAIChat(id="gpt-4o"),
            knowledge=broker.rules_kb,
            search_knowledge=True,
            tools=[
                redmine_reasoning,       # Impact & dependency evaluation
                ReasoningTools(add_instructions=True),
                KnowledgeTools(knowledge=broker.rules_kb)
            ],
            description=(
                "Evalúa si el contenido generado cumple con las normas (NCC, SGPD) "
                "y la veracidad de los datos. Actúa como auditor independiente con MAR Reflexion."
            ),
            output_schema=FeedbackCritiqueSchema, # AGDR v5.0 Structured Output
            instructions=[
                "Eres el ExpertJudgeAgent (Checker) en el bucle Maker-Checker v5.0.",
                "Tu misión es AUDITAR el contenido generado por el AuthorAgent comparándolo ESTRICTAMENTE con la 'PLANTILLA_MAESTRA_SIC_GENERICO.md' y las normas NCC-24.",
                
                "═══════════════════════════════════════════════════════════",
                "FASE 1 - MULTI-AGENT REFLEXION (MAR):",
                "Emula las siguientes perspectivas para romper el sesgo de confirmación:",
                "  - Analista de Riesgos: Busca alucinaciones financieras.",
                "  - Lector de Cumplimiento: Verifica adherencia a NCC-24.",
                "  - Experto en Operaciones: Valida coherencia de procesos.",
                
                "FASE 2 - ANÁLISIS CAUSAL (SGP-LA):",
                "Si detectas fallos de calidad (< 95), realiza obligatoriamente:",
                "  - Búsqueda de Causa Raíz usando 5 Whys o Diagrama Ishikawa.",
                "  - Resultado: Llenar campo `root_cause`.",
                
                "FASE 3 - REDACCIÓN DE LECCIONES (Anexo CC/DD):",
                "Redacta hallazgos en el campo `actionable_recommendation` siguiendo el formato:",
                "  '(Recomendación), para reducir/evitar (PROBLEMA)'.",
                
                "FASE 4 - CRITERIOS DUROS DE CUMPLIMIENTO (NCC-XX):",
                "  - PCB ELIMINATION: Verifica que se mencionen los hitos: detener operación equipos PCB > 2025 y eliminación definitiva > 2028 (D. 38/2005).",
                "  - ESTRUCTURA SIC 01: Debe contener la 'Tabla 12 Indicadores Económicos'.",
                "  - ESTRUCTURA SIC 16: Debe contener la 'Tabla 1611: Valor Contingencia' y el 'Resumen Costos de Capital'.",
                "  - INTEGRIDAD 22 SIC: El QC Score solo puede ser > 95 si se han procesado los 22 entregables SIC del plan.",
                
                "FASE 5 - GESTIÓN DE LECCIONES (SGP-LA):",
                "  - Captura el evento de falla anterior (QC Score 60%, documento incompleto) como un Hallazgo.",
                "  - Realiza un Análisis Causal (Bow-Tie o 5 Whys).",
                "  - Redacta la Nueva Lección en `actionable_recommendation`: '(Recomendación), para reducir/evitar (PROBLEMA)'.",
                
                "FASE 6 - DECISIÓN (Score):",
                "- >= 95: APROBADO (solo si los 22 SIC están presentes y cumplen normativas).",
                
                "═══════════════════════════════════════════════════════════",
                "CRÍTICO: Mitigación de Contexto",
                "Solo retorna el JSON estructurado. NO repitas el documento auditado.",
                "═══════════════════════════════════════════════════════════"
            ],
            markdown=True,
            **kwargs
        )
