from langchain_huggingface import HuggingFaceEmbeddings
from app.configs.settings import get_settings
from functools import lru_cache


@lru_cache
def get_embeddings() -> HuggingFaceEmbeddings:
  settings = get_settings()
  return HuggingFaceEmbeddings(
    model_name=settings.embedding_model,
  )
