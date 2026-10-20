from langchain_huggingface import HuggingFaceEmbeddings
from app.configs.settings import get_settings
from app.utils import get_logger
from functools import lru_cache

logger = get_logger(__name__)


@lru_cache
def get_embeddings() -> HuggingFaceEmbeddings:
  settings = get_settings()
  logger.info("Loading embedding model: %s", settings.embedding_model)
  return HuggingFaceEmbeddings(
    model_name=settings.embedding_model,
  )
