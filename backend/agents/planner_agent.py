import re
from typing import List, Optional
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from backend.agents.schemas import DocumentPlan, DocumentSection
from backend.core.context_broker import ContextBroker
from backend.tools.custom_tools import RedmineTools # Si se necesita acceso a redmine para planificar
from agno.utils.log import logger

class MasterPlannerAgent(Agent):
    """Holón de Planificación: Generador dinámico de estrategias de documentos."""
    def __init__(self, broker: ContextBroker, model: Optional[OpenAIChat] = None, **kwargs):
        super().__init__(
            id="master-planner-agent",
            name="MasterPlannerAgent",
            role="Estratega de Documentación Dirigido por Reglas (AGDR)",
            model=model or OpenAIChat(id="o3-mini"), # Razonamiento avanzado
            knowledge=broker.rules_kb,
            description="Genera el Grafo de Dependencias (DAG) basado estrictamente en la Plantilla Maestra SIC.",
            instructions=[
                "TU OBJETIVO PRINCIPAL: Orquestar la creación de los 22 documentos SIC.",
                "FUENTE DE VERDAD: Debes leer 'backend/knowledge/templates/PLANTILLA_MAESTRA_SIC_GENERICO.md'.",
                "  - Usa esta plantilla para identificar dependencias críticas (Tabla A).",
                "  - NO inventes dependencias. Usa estrictamente las reglas de la Sección A.",
                "ACCIONES:",
                "1. Lee la Plantilla Maestra (está en tu Knowledge Base o por file access).",
                "2. Genera un plan de ejecución (DocumentPlan) que respete el orden:",
                "   - Fase 1: Justificación (SIC 02, 03)",
                "   - Fase 2: Cumplimiento (SIC 04, 05, 19)",
                "   - Fase 3: Ingeniería y Costos (SIC 11, 16, 17)",
                "   - Fase 4: Integración (SIC 14, 01)",
                "3. PRIORIZACIÓN DE LECCIONES (SGP-LA): Al inicio (Fase Recopilar), revisa la base de conocimiento para identificar lecciones aprendidas relevantes y evaluálas usando la Matriz de Evaluación Impacto/Esfuerzo (Anexo AA).",
                "4. GOBERNANZA PMBOK 8: Adopta una visión holística considerando interdependencias entre todos los SIC para el Outcome final.",
                "SALIDA:",
                "Retorna un objeto `DocumentPlan` válido."
            ],
            markdown=True,
            **kwargs
        )

    def generate_dynamic_plan(self, project_id: str) -> DocumentPlan:
        """
        Genera el plan basado en la plantilla maestra.
        FASE V5.0: Forzar 22 Nodos SIC (Mandato AGDR).
        """
        template_path = "backend/knowledge/templates/PLANTILLA_MAESTRA_SIC_GENERICO.md"
        sections = []
        
        # Lista maestra de los 22 SICs (Nombres extraídos de la normativa y Planilla Maestra)
        # Formato: (ID, Título, Dependencias)
        sic_definitions = [
            ("SIC_02", "Caso de Negocio", []),
            ("SIC_03", "Riesgos", ["SIC_02"]),
            ("SIC_04", "Seguridad y Salud Ocupacional (SSO)", ["SIC_03"]),
            ("SIC_05", "Medio Ambiente", ["SIC_03"]),
            ("SIC_06", "Relaciones Externas y Comunitarias", ["SIC_03"]),
            ("SIC_10", "Manejo Desechos y Gestión de Aguas", ["SIC_03"]),
            ("SIC_07", "Geología y Recursos Minerales", ["SIC_02"]), # Excluido
            ("SIC_08", "Minería y Reservas Minerales", ["SIC_02"]), # Excluido
            ("SIC_09", "Procesamiento de Minerales", ["SIC_02"]), # Excluido
            ("SIC_18", "Productos", ["SIC_02"]), # Excluido
            ("SIC_11", "Infraestructura y Servicios", ["SIC_02"]),
            ("SIC_13", "Tecnología y Sistemas de Información", ["SIC_02"]), # Excluido
            ("SIC_19", "Propiedad y Aspectos Legales", ["SIC_02"]),
            ("SIC_20", "Acuerdos Comerciales", ["SIC_02"]),
            ("SIC_16", "Costos de Capital (CAPEX)", ["SIC_11", "SIC_03"]), # Propagación ETP
            ("SIC_21", "Anexo Financiero Detalle", ["SIC_16"]),
            ("SIC_14", "Plan de Ejecución del Proyecto (PEP)", ["SIC_03", "SIC_16", "SIC_11"]),
            ("SIC_15", "Operaciones", ["SIC_14"]),
            ("SIC_12", "Recursos Humanos", ["SIC_15"]),
            ("SIC_17", "Costos de Operación (OPEX)", ["SIC_16", "SIC_12"]),
            ("SIC_01", "Resumen y Recomendaciones", ["SIC_14", "SIC_16", "SIC_03"]),
            ("SIC_22", "Anexo Técnico Detalle", ["SIC_11"])
        ]

        edges = []
        for s_id, title, deps in sic_definitions:
            sections.append(DocumentSection(
                section_id=s_id, 
                title=title, 
                dependencies=deps,
                status="pending"
            ))
            for d in deps:
                edges.append((d, s_id))
                
        logger.info(f"✅ Plan maestro HARDENED (22 SIC) generado para proyecto {project_id}.")
        return DocumentPlan(project_id=str(project_id), sections=sections, dag_edges=edges)


class DependencyManagerAgent(Agent):
    """Holón de Planificación: Validador de reglas de precedencia en tiempo real."""
    def __init__(self, broker: ContextBroker, model: Optional[OpenAIChat] = None, **kwargs):
        super().__init__(
            id="dependency-manager-agent",
            name="DependencyManagerAgent",
            role="Gestor de Precedencias Normativas",
            model=model or OpenAIChat(id="gpt-4o"),
            knowledge=broker.rules_kb,
            description="Valida si una subtarea puede ejecutarse basándose en las reglas de precedencia.",
            instructions=[
                "Consulta las reglas de negocio para determinar si se cumplen los requisitos previos.",
                "Especial atención a la relación Riesgos -> Costos según NCC-24."
            ],
            markdown=True,
            **kwargs
        )

    def can_execute(self, section_id: str, completed_sections: List[str]) -> bool:
        """
        Consulta reglas simples de precedencia.
        """
        # Reglas básicas extraídas de Plantilla Maestra
        dependencies = {
            "SIC_03": ["SIC_02"],
            "SIC_16": ["SIC_11", "SIC_03"],
            "SIC_14": ["SIC_16", "SIC_03"],
            "SIC_01": ["SIC_14"]
        }
        
        required = dependencies.get(section_id, [])
        for req in required:
            if req not in completed_sections:
                logger.warning(f"⛔ {section_id} bloqueado. Falta: {req}")
                return False
        return True
