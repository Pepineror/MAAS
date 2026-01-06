from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector, SearchType
from agno.knowledge.embedder.openai import OpenAIEmbedder
from typing import Optional, List

class RedmineKnowledgeBase(Knowledge):
    def __init__(
        self,
        table_name: str = "redmine_knowledge",
        db_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/maas",
        api_key: Optional[str] = None,
    ):
        super().__init__(
            vector_db=PgVector(
                table_name=table_name,
                db_url=db_url,
                search_type=SearchType.hybrid,
                embedder=OpenAIEmbedder(id="text-embedding-3-small", api_key=api_key),
            ),
        )

    def search_with_metadata(self, query: str, project_id: Optional[int] = None, issue_type: Optional[str] = None, limit: int = 5):
        """
        Search with metadata filtering (Requirement 1.1)
        """
        filters = {}
        if project_id:
            filters["project_id"] = project_id
        if issue_type:
            filters["issue_type"] = issue_type
        
        return self.vector_db.search(query=query, limit=limit, filters=filters)
