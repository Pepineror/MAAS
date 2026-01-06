import unittest
from unittest.mock import MagicMock, patch
from agno.workflow import StepOutput
from backend.agents.base_agents import ExtractorAgent, AuthorAgent, ReviewerAgent
from backend.workflows.document_workflow import DocumentCreationWorkflow

class TestMAASWorkflow(unittest.TestCase):
    def setUp(self):
        # Mock agents
        self.mock_extractor = MagicMock(spec=ExtractorAgent)
        self.mock_author = MagicMock(spec=AuthorAgent)
        self.mock_reviewer = MagicMock(spec=ReviewerAgent)
        
        # Initialize workflow with mocks
        self.workflow = DocumentCreationWorkflow(
            extractor=self.mock_extractor,
            author=self.mock_author,
            reviewer=self.mock_reviewer,
            workspace_id="test-workspace"
        )

    def test_workflow_logic_success(self):
        # Setup mock returns
        self.mock_extractor.run.return_value = StepOutput(content="Risk ETP: High", success=True)
        self.mock_author.run.side_effect = [
            StepOutput(content="SIC 16 Content", success=True),
            StepOutput(content="SIC 14 Content", success=True),
            StepOutput(content="SSO Section Content", success=True)
        ]
        self.mock_reviewer.run.return_value = StepOutput(content={"score": 85}, success=True)

        # Run workflow with additional_data
        result = self.workflow.run(
            additional_data={"project_id": 123, "initial_context": "Project Alpha"}
        )

        # Assertions
        self.assertTrue(result.success)
        self.assertEqual(result.content, "SIC Document generated successfully")
        self.assertEqual(self.mock_extractor.run.call_count, 1)
        
    def test_workflow_logic_failure_score(self):
        # Setup mock returns
        self.mock_extractor.run.return_value = StepOutput(content="Risk ETP: Low", success=True)
        self.mock_author.run.return_value = StepOutput(content="Mixed Content", success=True)
        self.mock_reviewer.run.return_value = StepOutput(content={"score": 40}, success=True)

        # Run workflow
        result = self.workflow.run(
            additional_data={"project_id": 123, "initial_context": "Project Beta"}
        )

        # Assertions
        self.assertFalse(result.success)
        self.assertEqual(result.content, "Rollback initiated due to low score")

if __name__ == "__main__":
    unittest.main()
