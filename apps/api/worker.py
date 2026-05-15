import os
from celery import Celery
from .ingestion import IngestionEngine
from .semantic import SemanticEngine
from .graph import GraphEngine
from packages.parser.core import CodeParser
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "aether_worker",
    broker=os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

@celery_app.task(name="index_repository")
def index_repository(repo_id: str, repo_url: str):
    ingestion = IngestionEngine()
    parser = CodeParser()
    semantic = SemanticEngine()
    graph = GraphEngine()
    
    # 1. Clone
    local_path = ingestion.clone_repository(repo_url)
    
    # 2. Walk & Parse
    files = ingestion.walk_repository(local_path)
    
    for file_meta in files:
        # Parse file
        parsed_data = parser.parse_file(file_meta["full_path"])
        
        # Add to graph
        graph.add_file(file_meta["path"], file_meta)
        
        # Index symbols and chunks
        for symbol in parsed_data["symbols"]:
            # Index in vector DB
            semantic.index_chunk(
                chunk_id=f"{repo_id}:{file_meta['path']}:{symbol['name']}",
                content=symbol["content"],
                metadata={
                    "repo_id": repo_id,
                    "file_path": file_meta["path"],
                    "symbol_name": symbol["name"],
                    "symbol_type": symbol["type"]
                }
            )
            # Add to graph
            graph.add_symbol(symbol["name"], file_meta["path"], symbol)
            
    # 3. Cleanup
    ingestion.cleanup(local_path)
    
    return {"status": "completed", "repo_id": repo_id}
