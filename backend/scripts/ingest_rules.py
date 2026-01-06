import os
from agno.knowledge.reader.text_reader import TextReader
from backend.core.context_broker import ContextBroker
from dotenv import load_dotenv

load_dotenv()

def ingest_business_rules():
    # 1. Initialize Broker
    broker = ContextBroker(
        db_url=os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/maas")
    )
    
    # 2. Define source files
    rules_dir = "backend/knowledge"
    if not os.path.exists(rules_dir):
        print(f"Directory {rules_dir} not found.")
        return

    # 3. Create Reader and Load
    reader = TextReader()
    documents = reader.read(rules_dir)
    
    # 4. Load into Rules Knowledge Base
    print(f"Ingesting {len(documents)} rule documents into rules_kb...")
    broker.rules_kb.load(documents=documents, upsert=True)
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_business_rules()
