from app.configs import get_settings
from qdrant_client import QdrantClient
from functools import lru_cache
from langchain_qdrant import QdrantVectorStore
from app.services.embeddings import get_embeddings


@lru_cache
def qdrant_client() -> QdrantClient:
  """Get the qdrant client for the application"""
  settings= get_settings()
  return QdrantClient(
    url=settings.qdrant_url,
  )


class VectorStoreRepository:
  def __init__(self, collection_name: str | None = None):
    settings= get_settings()
    self.collection_name= collection_name or settings.collection_name
    self.client= qdrant_client()
    self._vector_store= QdrantVectorStore | None= None


    def vector_store(self)-> QdrantVectorStore:
      if self._vector_store is None:
        self._vector_store= QdrantVectorStore(
          client=self.client,
          collection_name=self.collection_name,
          embedding= get_embeddings()
        )
      return self._vector_store