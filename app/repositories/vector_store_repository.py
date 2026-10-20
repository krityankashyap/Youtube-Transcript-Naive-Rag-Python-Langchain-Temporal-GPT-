from app.configs import get_settings
from qdrant_client import QdrantClient
from functools import lru_cache
from langchain_qdrant import QdrantVectorStore
from app.services.embeddings import get_embeddings
from langchain_core.documents import Documents
import uuid


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

  @property
  def vector_store(self)-> QdrantVectorStore:
    if self._vector_store is None:
      self._vector_store= QdrantVectorStore(  
        client=self.client,
        collection_name=self.collection_name,
        embedding= get_embeddings()
      )
    return self._vector_store
    

  def _ensure_connection(self) -> None:
    """Ensure the connection to the vector store is established."""
    if self._vector_store is None:
      self.vector_store()

  
  def add_documents(self, documents: list[Documents]) -> list[str]:
    """Add documents to the vector store."""
    if not documents:
      return []
    
    ids= [str[uuid.uuid4()] for _ in documents]
    self.vector_store.add_documents(documents=documents, ids=ids)
    return ids
