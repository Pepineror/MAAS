"""
Backend Agents Package

Contiene agentes especializados para el sistema MAAS v4.0:
- GenericDataAgent: Extracción de datos desde Redmine
- MetricExtractorAgent: Transformación a métricas estructuradas
- GeneralAuthorAgent: Redacción de documentos técnicos
- ExpertJudgeAgent: Auditoría y validación de calidad
- MasterPlannerAgent: Planificación estratégica
- DependencyManagerAgent: Gestión de dependencias

Cada agente está especializado en una función específica dentro del 
flujo de creación de documentos de preinversión (SIC).
"""

from backend.agents.generic_data_agent import GenericDataAgent
from backend.agents.metric_extractor_agent import MetricExtractorAgent
from backend.agents.author_agent import GeneralAuthorAgent
from backend.agents.judge_agent import ExpertJudgeAgent
from backend.agents.planner_agent import MasterPlannerAgent, DependencyManagerAgent
from backend.agents.extractor_agent import DataIngestorAgent, ExtractorAgent

__all__ = [
    "GenericDataAgent",
    "MetricExtractorAgent",
    "GeneralAuthorAgent",
    "ExpertJudgeAgent",
    "MasterPlannerAgent",
    "DependencyManagerAgent",
    "DataIngestorAgent",
    "ExtractorAgent",
]
