import os
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class SemanticEngine:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.qdrant = QdrantClient(
            url=os.getenv("QDRANT_URL", "http://localhost:6333"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = "code_intelligence"
        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.qdrant.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)
        
        if not exists:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )

    def generate_embeddings(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def index_chunk(self, chunk_id: str, content: str, metadata: Dict[str, Any]):
        vector = self.generate_embeddings(content)
        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=chunk_id,
                    vector=vector,
                    payload={
                        "content": content,
                        **metadata
                    }
                )
            ]
        )

    def search(self, query: str, limit: int = 5, filters: Dict = None) -> List[Dict]:
        vector = self.generate_embeddings(query)
        
        results = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit,
            with_payload=True
        )
        
        return [
            {
                "id": r.id,
                "score": r.score,
                "content": r.payload["content"],
                "metadata": {k: v for k, v in r.payload.items() if k != "content"}
            }
            for r in results
        ]
