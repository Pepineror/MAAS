import asyncio
import sys
import os
from pathlib import Path

# Fix sys.path
root_dir = str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.agents.planner_agent import MasterPlannerAgent
from backend.core.context_broker import ContextBroker
from backend.agents.schemas import DocumentPlan
from backend.auth import create_test_token, jwt_manager

async def test_22_node_plan():
    print("--- Testing 22-Node DAG Generation ---")
    
    # Mock components that try to connect to DB
    from unittest.mock import MagicMock, patch
    with patch('backend.core.context_broker.AsyncPostgresDb'), \
         patch('backend.core.context_broker.PgVector'), \
         patch('backend.core.context_broker.OpenAIEmbedder'), \
         patch('backend.core.context_broker.PostgresDb'):
        
        broker = ContextBroker(db_url="postgresql://localhost:5432/test", openai_api_key="test")
        planner = MasterPlannerAgent(broker=broker)
        
        plan = planner.generate_dynamic_plan(project_id="AIASeco")
    
    print(f"Total sections: {len(plan.sections)}")
    for s in plan.sections:
        print(f" - {s.section_id}: {s.title} (Deps: {s.dependencies})")
    
    assert len(plan.sections) == 22, f"Expected 22 sections, got {len(plan.sections)}"
    
    # Check ETP dependency
    sic16 = next(s for s in plan.sections if s.section_id == "SIC_16")
    assert "SIC_03" in sic16.dependencies, "SIC_16 must depend on SIC_03 for ETP propagation"
    print("✅ 22-Node Plan Verified")

def test_scope_validation():
    print("\n--- Testing PoLP Scope Validation ---")
    
    # 1. Valid Token with all scopes
    token_all = create_test_token(role="ADMIN")
    payload_all = jwt_manager.validate_token(token_all)
    assert jwt_manager.verify_scope(payload_all, "workflows:DocumentCreationWorkflow:run")
    print("✅ Admin Scope Verified")
    
    # 2. Operator Token with specific workflow scope
    token_op = create_test_token(role="OPERATOR")
    payload_op = jwt_manager.validate_token(token_op)
    assert jwt_manager.verify_scope(payload_op, "workflows:DocumentCreationWorkflow:run")
    print("✅ Operator Scope Verified")
    
    # 3. Viewer Token (should fail workflow run)
    token_view = create_test_token(role="VIEWER")
    payload_view = jwt_manager.validate_token(token_view)
    has_wf_scope = jwt_manager.verify_scope(payload_view, "workflows:DocumentCreationWorkflow:run")
    assert not has_wf_scope, "Viewer should not have workflow:run scope"
    print("✅ Viewer Restricted Access Verified")

if __name__ == "__main__":
    asyncio.run(test_22_node_plan())
    test_scope_validation()
