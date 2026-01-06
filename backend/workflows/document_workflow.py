from typing import Optional, List, Dict, Any, Union
import asyncio
import json
from agno.workflow import Workflow, StepOutput, StepInput
from agno.utils.log import logger
from backend.agents.metric_extractor_agent import MetricExtractorAgent
from backend.agents.author_agent import GeneralAuthorAgent
from backend.agents.judge_agent import ExpertJudgeAgent
from backend.agents.schemas import SIC_DTO, FeedbackCritiqueSchema

class DocumentCreationWorkflow(Workflow):
    """
    FASE V5.0: Graph Orchestrator with Self-Correction (Maker-Checker)
    Hardening AGDR: Context Mitigation and DTO Serialization.
    """
    def __init__(
        self,
        planner: Any,
        extractor: MetricExtractorAgent,
        author: GeneralAuthorAgent,
        reviewer: ExpertJudgeAgent,
        workspace_id: str = "default",
        pdf_tool: Any = None,
        **kwargs
    ):
        super().__init__(
            id=f"doc-graph-v5-{workspace_id}",
            name="MAAS v5.0 Directed Agent Graph",
            description="Orquestador DAG con Bucle Maker-Checker (AGDR v5.0)",
            steps=[self.main_execution], 
            **kwargs
        )
        self.planner = planner
        self.extractor = extractor
        self.author = author
        self.reviewer = reviewer
        self.pdf_tool = pdf_tool

    async def main_execution(
        self,
        step_input: StepInput,
        **kwargs
    ) -> StepOutput:
        """
        Main execution logic for the workflow.
        """
        input_data = step_input.input or {}
        if isinstance(input_data, str):
            try:
                input_data = json.loads(input_data)
            except:
                input_data = {}
        
        project_id = input_data.get("project_id", 9)
        document_type = input_data.get("document_type", "SIC")
        

        logger.info(f"🚀 [AGDR v5.0] Executing Hardened Workflow for Project {project_id}")

        try:
            # ============================================================
            # NODE 1: DATA INGESTION & PLANNING
            # ============================================================
            planner_run = await self.planner.arun(
                f"Genera el Plan Maestro AGDR (22 SIC) para proyecto {project_id}."
            )
            plan: DocumentPlan = planner_run.content
            if not isinstance(plan, DocumentPlan):
                if isinstance(plan, dict):
                    plan = DocumentPlan(**plan)
                else:
                    raise ValueError("Planner no devolvió DocumentPlan válido")

            logger.info(f"📋 [DAG] Plan de 22 secciones cargado. Iniciando ejecución secuencial/paralela.")

            # ============================================================
            # NODE 2: SEQUENTIAL DAG EXECUTION (22 NODES)
            # ============================================================
            completed_sections: Dict[str, SIC_DTO] = {}
            qc_scores: Dict[str, float] = {}
            last_critique_per_section: Dict[str, FeedbackCritiqueSchema] = {}

            # Ordenamos las secciones para respetar dependencias básicas (simplificado a lineal por seguridad en runtime)
            # Aunque el Planner da un DAG, aquí forzamos la ejecución de los 22 nodos.
            for section in plan.sections:
                s_id = section.section_id
                logger.info(f"🏗️ [NODE {s_id}] Procesando: {section.title}...")

                # Propagación de Dependencias Críticas (ETP SIC 03 -> SIC 16)
                extra_context = ""
                if s_id == "SIC_16" and "SIC_03" in completed_sections:
                    sic03_data = completed_sections["SIC_03"]
                    # Buscamos ETP en metadatos
                    etp_val = next((kv.value for kv in sic03_data.metadata if "ETP" in kv.key.upper()), "PENDIENTE")
                    extra_context = f"\n⚠️ DATO CRÍTICO (ETP SIC 03): {etp_val}. Úsalo para justificar la Contingencia en Tabla 1611."

                # Maker-Checker Loop for this specific section
                approved = False
                current_dto = None
                last_critique: Optional[FeedbackCritiqueSchema] = None

                for attempt in range(2): # 2 intentos por sección para no extender el runtime infinitamente
                    # 1. TRUNCAMIENTO DE HISTORIAL (Mandato AGDR)
                    # Limpiamos la memoria de los agentes en cada iteración para evitar Context Overflow
                    if attempt > 0:
                        logger.info(f"🧹 [Attempt {attempt+1}] Truncando historial de conversación para {s_id}...")
                        if hasattr(self.author, 'memory') and self.author.memory:
                            self.author.memory.clear()
                        if hasattr(self.reviewer, 'memory') and self.reviewer.memory:
                            self.reviewer.memory.clear()

                    # Author (Maker)
                    author_prompt = (
                        f"Genera el contenido para {s_id}: {section.title} del proyecto {project_id}.\n"
                        f"DEPENDE DE: {', '.join(section.dependencies)}\n"
                        f"CONTEXTO ADICIONAL: {extra_context}\n"
                        f"CRÍTICA PREVIA: {last_critique.actionable_recommendation if last_critique else 'INICIO'}\n"
                        "Sigue estrictamente la PLANTILLA_MAESTRA_SIC_GENERICO.md."
                    )
                    maker_run = await self.author.arun(author_prompt)
                    current_dto = maker_run.content
                    if not isinstance(current_dto, SIC_DTO):
                        if isinstance(current_dto, dict): current_dto = SIC_DTO(**current_dto)
                        else: continue

                    # Judge (Checker)
                    checker_prompt = (
                        f"Audita la sección {s_id} del proyecto {project_id}.\n"
                        f"TEXTO: {current_dto.summary_markdown[:10000]}\n"
                        "Verifica tablas obligatorias y cumplimiento PCB (si aplica SIC 04/05/10/11)."
                    )
                    checker_run = await self.reviewer.arun(checker_prompt)
                    last_critique = checker_run.content
                    if not isinstance(last_critique, FeedbackCritiqueSchema):
                        if isinstance(last_critique, dict): last_critique = FeedbackCritiqueSchema(**last_critique)

                    logger.info(f"   ∟ Attempt {attempt+1} | QC: {last_critique.qc_score} | Approved: {last_critique.approved}")
                    if last_critique.approved or last_critique.qc_score > 85: # Umbral de paso por sección
                        approved = True
                        break

                completed_sections[s_id] = current_dto
                qc_scores[s_id] = last_critique.qc_score if last_critique else 0
                last_critique_per_section[s_id] = last_critique

            # ============================================================
            # NODE 3: ASSEMBLY & FINAL VALIDATION
            # ============================================================
            logger.info("🔧 [NODE 23] Ensamblaje final de los 22 entregables...")

            full_markdown = "\n\n".join([
                f"# {completed_sections[s].sic_code}: {completed_sections[s].summary_markdown}"
                for s in completed_sections if completed_sections[s]
            ])

            # Verificación final de integridad
            final_qc_score = sum(qc_scores.values()) / len(qc_scores) if len(qc_scores) > 0 else 0
            is_complete = len(completed_sections) == 22

            if is_complete and final_qc_score > 95:
                logger.info(f"🏆 [AGDR] ¡Éxito! QC Score Final: {final_qc_score}% con 22/22 documentos.")
            else:
                logger.warning(f"⚠️ [AGDR] QC Score Final: {final_qc_score}%. Docs: {len(completed_sections)}/22.")

            # ============================================================
            # NODE 4: FINAL ASSEMBLY
            # ============================================================
            final_document = full_markdown

            # PDF Generation - Corrected method name
            pdf_filename = f"SIC_AIASECO_{project_id}.pdf"
            pdf_path = f"output_pdfs/{pdf_filename}"
            try:
                if self.pdf_tool:
                    logger.info(f"📄 Generando PDF en {pdf_path}...")
                    result_pdf = self.pdf_tool.convert_markdown_to_pdf(final_document, pdf_filename)
                    logger.info(f"✅ Resultado PDF: {result_pdf}")
            except Exception as e:
                logger.error(f"❌ Error en PDF: {e}")

            return StepOutput(
                content={
                    "document": final_document,
                    "project_id": project_id,
                    "approved": is_complete and final_qc_score > 95,
                    "qc_score": final_qc_score,
                    "audit_report": {
                        "is_complete": is_complete,
                        "sections_generated": len(completed_sections),
                        "details": {s: {"score": qc_scores[s]} for s in qc_scores}
                    },
                    "pdf_path": pdf_path,
                    "dto_metadata": {
                        f"{s_id}_{kv.key}": kv.value 
                        for s_id, dto in completed_sections.items() if dto 
                        for kv in dto.metadata
                    }
                },
                success=True
            )

        except Exception as e:
            logger.error(f"💥 [FATAL] Error en Workflow Hardened: {str(e)}", exc_info=True)
            return StepOutput(content=f"Error: {str(e)}", success=False)
