import os
import asyncio
import logging
from typing import Optional
from agno.db.postgres import PostgresDb
from backend.core.async_postgres_db import AsyncPostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector, SearchType
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.knowledge.reader.text_reader import TextReader

logger = logging.getLogger(__name__)

class ContextBroker:
    """
    The Context Broker acts as the Single Source of Truth for all Holons.
    FASE II CAMBIO 2.1: True AsyncPostgresDb with asyncpg for non-blocking I/O.
    
    Manages three repositories:
    1. Session Storage (Facts + Memory) - AsyncPostgresDb
    2. Project Knowledge (Dynamic, Vector) - PgVector
    3. Business Rules (Static, Vector + Contents) - PgVector + PostgresDb
    
    Performance improvements:
    - Connection pooling (concurrent connections)
    - Non-blocking I/O (no greenlet hacks)
    - Better resource utilization
    - -5-10s latency for DB queries
    """
    def __init__(
        self,
        db_url: str = "postgresql://postgres:postgres@localhost:5434/maas",
        openai_api_key: Optional[str] = None,
        openai_base_url: Optional[str] = None
    ):
        self.db_url = db_url
        self.embedder = OpenAIEmbedder(
            id="text-embedding-3-small", 
            api_key=openai_api_key,
            base_url=openai_base_url
        )
        
        self.session_db = AsyncPostgresDb(
            id="maas_async_db_v5",  # Stable ID for Agno OS compatibility
            db_url=db_url,
            session_table="maas_sessions",
            max_connections=20  # Support up to 20 concurrent connections
        )
        
        # 2. Project Knowledge Base (Dynamic Data) - Uses PgVector (async-compatible)
        self.project_kb = Knowledge(
            vector_db=PgVector(
                table_name="project_knowledge",
                db_url=db_url,
                search_type=SearchType.hybrid,
                embedder=self.embedder
            )
        )
        
        # 3. Rules Knowledge Base (Static Business Rules) - Uses PostgresDb for Agno compatibility
        # TODO: CAMBIO 2.5: Migrate to AsyncPostgresDb once Agno Knowledge supports async contents_db
        self.rules_kb = Knowledge(
            vector_db=PgVector(
                table_name="business_rules",
                db_url=db_url,
                search_type=SearchType.hybrid,
                embedder=self.embedder
            ),
            contents_db=PostgresDb(
                db_url=db_url,
                knowledge_table="business_rules_contents"
            )
        )

    async def load_rules(self):
        """
        Automates the ingestion of standard templates and NCC rules.
        FASE 0: Robust error handling with logging.
        """
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            templates_path = os.path.join(base_path, "knowledge", "templates")
            rules_file = os.path.join(base_path, "knowledge", "rules_ncc24.txt")
            unified_kb_file = os.path.join(base_path, "knowledge", "KNOWLEDGE_BASE_UNIFIED.md")
            template_guide_file = os.path.join(base_path, "knowledge", "TEMPLATE_USAGE_GUIDE.md")

            # Load Templates (Markdown)
            if os.path.exists(templates_path):
                logger.info(f"📚 Loading templates from {templates_path}")
                await self.rules_kb.add_content_async(
                    path=templates_path,
                    reader=MarkdownReader()
                )
                logger.info("✅ Templates loaded successfully")
            else:
                logger.warning(f"⚠️ Templates path not found: {templates_path}")
            
            # Load NCC Rules (Text)
            if os.path.exists(rules_file):
                logger.info(f"📚 Loading rules from {rules_file}")
                await self.rules_kb.add_content_async(
                    path=rules_file,
                    reader=TextReader()
                )
                logger.info("✅ NCC Rules loaded successfully")
            else:
                logger.warning(f"⚠️ Rules file not found: {rules_file}")

            # Load Unified Knowledge Base (Markdown) - Contains workflow, field mapping, agent instructions
            if os.path.exists(unified_kb_file):
                logger.info(f"📚 Loading unified knowledge base from {unified_kb_file}")
                await self.rules_kb.add_content_async(
                    path=unified_kb_file,
                    reader=MarkdownReader()
                )
                logger.info("✅ Unified Knowledge Base loaded successfully")
            else:
                logger.warning(f"⚠️ Unified KB file not found: {unified_kb_file}")

            # Load Template Usage Guide (Markdown) - Contains step-by-step template instructions
            if os.path.exists(template_guide_file):
                logger.info(f"📚 Loading template usage guide from {template_guide_file}")
                await self.rules_kb.add_content_async(
                    path=template_guide_file,
                    reader=MarkdownReader()
                )
                logger.info("✅ Template Usage Guide loaded successfully")
            else:
                logger.warning(f"⚠️ Template guide file not found: {template_guide_file}")
                
            logger.info("✅ All rules loaded successfully")
        except Exception as e:
            logger.error(f"❌ Error loading rules: {str(e)}", exc_info=True)
            raise

    async def publish_finding(self, findings: str, project_id: int):
        """
        Allows agents to publish new findings to the project knowledge base.
        FASE 0: Async implementation.
        """
        try:
            return await self.rules_kb.vector_db.async_search(
                query=query, 
                limit=limit
            )
        except Exception as e:
            logger.error(f"❌ Error searching rules for '{query}': {str(e)}")
            return []

    async def get_project_context(self, query: str, project_id: int, limit: int = 5):
        """
        Query the project repository for specific facts.
        FASE 0: Async implementation with filtering.
        """
        try:
            filters = {"project_id": project_id}
            return await self.project_kb.vector_db.async_search(
                query=query, 
                limit=limit, 
                filters=filters
            )
        except Exception as e:
            logger.error(f"❌ Error searching project {project_id} for '{query}': {str(e)}")
            return []
