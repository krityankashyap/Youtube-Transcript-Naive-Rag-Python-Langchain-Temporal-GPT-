from app.configs.settings import get_settings
from qdrant_client import QdrantClient
from functools import lru_cache
from langchain_qdrant import QdrantVectorStore
from app.services.embeddings import get_embeddings
from app.utils import get_logger
from langchain_core.documents import Document
import uuid

logger = get_logger(__name__)


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
    self._vector_store: QdrantVectorStore | None= None

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
      _ = self.vector_store

  
  def add_documents(self, documents: list[Document]) -> list[str]:
    """Add documents to the vector store."""
    if not documents:
      logger.debug("add_documents called with no documents; skipping")
      return []

    ids= [str(uuid.uuid4()) for _ in documents]
    logger.info("Adding %d documents to collection '%s'", len(documents), self.collection_name)
    self.vector_store.add_documents(documents=documents, ids=ids)
    return ids


  def delete_documents(self) -> None:
    logger.warning("Deleting collection '%s'", self.collection_name)
    self.client.delete_collection(collection_name=self.collection_name)
  


  def search_with_score(self, query: str, k: int | None = None) -> list[tuple[Document, float]]:
    """Search the vector store with a query and return documents with scores."""
    settings= get_settings()
    k= k or settings.retrieval_k
    logger.info("Similarity search (with score) k=%d for query: %r", k, query)
    return self.vector_store.similarity_search_with_score(query=query, k=k)
  
  
  def search(self, query: str, k: int | None = None) -> list[Document]:
    """Search the vector store with a query and return documents."""
    settings= get_settings()
    k= k or settings.retrieval_k
    logger.info("Similarity search k=%d for query: %r", k, query)
    return self.vector_store.similarity_search(query=query, k=k)