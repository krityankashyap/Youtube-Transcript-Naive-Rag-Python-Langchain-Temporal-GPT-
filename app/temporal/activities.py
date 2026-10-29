from app.services.documentService import DocumentService
from temporalio import activity
from langchain_core.documents import Document
from pathlib import Path
from app.repositories.vector_store_repository import VectorStoreRepository


async def _to_dicts(documents: list[Document])-> list[dict]:
  """Convert a list of Document objects to a list of dictionaries."""
  return [doc.to_dict() for doc in documents]

async def _to_documents(payload: list[dict]) -> list[Document]:
  """Convert a list of dictionaries to a list of Document objects."""
  return [Document.from_dict(doc) for doc in payload]

@activity.defn(name="parse_document_activity")
async def parse_document_activity(local_path: str, filename: str) -> list[dict]:
  service= DocumentService()
  docs= service.load_file(Path(local_path), source_name= filename)
  return await _to_dicts(docs)

@activity.defn(name="split_text_activity")
async def chunk_document_activity(documents: list[dict])-> list[dict]:
  """Split text in documents into chunks and return them."""
  service= DocumentService()
  chunks= service.split_documents(documents=await _to_documents(documents))
  return await _to_dicts(chunks)

@activity.defn(name="index_document_activity")
async def index_document_activity(chunks: list[dict]) -> int:
  """Index documents into the vector store and return their IDs."""
  if not chunks:
    return 0
  repoService= VectorStoreRepository()
  chnks= await _to_documents(chunks)
  ids= repoService.add_documents(chnks)
  activity.logger.info("Indexed %d chunks into the vector store", len(ids))
  return len(ids)

  