
import asyncio
import os
import sys
from typing import Dict, Any

# Ensure backend modules are importable
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.core.context_broker import ContextBroker
from backend.agents.base_agents import MetricExtractorAgent, GeneralAuthorAgent, ExpertJudgeAgent
from backend.agents.planner_agent import MasterPlannerAgent
from backend.workflows.document_workflow import DocumentCreationWorkflow
from agno.utils.log import logger

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)

async def run_full_workflow_test():
    """
    Simulates the generation of all 22 SIC documents for a given project.
    """
    logger.info("🚀 Starting Full Workflow Test for 22 SIC Documents")

    # 1. Initialize Context Broker (Async Single Source of Truth)
    broker = ContextBroker()
    
    # 2. Check and Load Rules (Ensure knowledge base is populated)
    # In a real scenario, this might already be loaded, but for the script we ensure it.
    await broker.load_rules()

    # 3. Initialize Agents
    planner_agent = MasterPlannerAgent(broker=broker)
    extractor_agent = MetricExtractorAgent(broker=broker)
    author_agent = GeneralAuthorAgent(broker=broker)
    judge_agent = ExpertJudgeAgent(broker=broker)

    # 4. Initialize Workflow
    workflow = DocumentCreationWorkflow(
        planner=planner_agent,
        extractor=extractor_agent,
        author=author_agent,
        reviewer=judge_agent,
        workspace_id="test-workspace-full"
    )

    # 5. Define Metadata Project
    metadata_project = {
        "project_id": 999,
        "name": "Proyecto de Prueba Full SIC",
        "description": "Proyecto para validar la generación de los 22 documentos SIC.",
        "budget": 5000000,
        "currency": "USD",
        "start_date": "2024-01-01",
        "end_date": "2025-12-31"
    }

    # 6. List all 22 SIC Document Types
    # Note: SIC_06 and SIC_11 were noted as missing in templates, but we include them to test coverage.
    sic_documents = [f"SIC_{i:02d}" for i in range(1, 23)]
    
    results = {}

    for doc_type in sic_documents:
        logger.info(f"\n========================================")
        logger.info(f"📄 Processing {doc_type}...")
        logger.info(f"========================================")

        try:
            # Execute the workflow for the specific document type
            # We pass the document_type as an argument if the workflow supports it, 
            # otherwise we might need to adjust the input prompt or additional_data.
            # Looking at document_workflow.py: document_creation_execution takes document_type.
            # However, Workflow.run (or arun) passes *args, **kwargs to the step function.
            
            step_output = await workflow.run(
                project_id=metadata_project["project_id"],
                document_type=doc_type
            )

            if step_output and step_output.success:
                 results[doc_type] = "✅ SUCCESS"
                 logger.info(f"✅ {doc_type} generated successfully.")
            else:
                 error_msg = step_output.content.get("error") if step_output and step_output.content else "Unknown Error"
                 results[doc_type] = f"❌ FAILED: {error_msg}"
                 logger.error(f"❌ {doc_type} failed: {error_msg}")

        except Exception as e:
            results[doc_type] = f"❌ EXCEPTION: {str(e)}"
            logger.error(f"❌ {doc_type} exception: {str(e)}", exc_info=True)

    # 7. Print Final Summary
    logger.info("\n\n📊 FINAL SUMMARY 📊")
    print(f"{'Document':<15} | {'Status'}")
    print("-" * 30)
    for doc, status in results.items():
        print(f"{doc:<15} | {status}")

if __name__ == "__main__":
    asyncio.run(run_full_workflow_test())
