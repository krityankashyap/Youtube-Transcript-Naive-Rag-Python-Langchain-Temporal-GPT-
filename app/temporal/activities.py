from app.services.documentService import DocumentService
from temporalio import activity
from langchain_core.documents import Document
from pathlib import Path


async def _to_dicts(documents: list[Document])-> list[dict]:
  """Convert a list of Document objects to a list of dictionaries."""
  return [doc.to_dict() for doc in documents]

async def _to_documents(payload: list[dict]) -> list[Document]:
  """Convert a list of dictionaries to a list of Document objects."""
  return [Document.from_dict(doc) for doc in payload]

@activity.defn(name="parse_document_activity", description="Parse a document and return its chunks")
async def parse_document_activity(local_path: str, filename: str) -> list[dict]:
  service= DocumentService()
  docs= service.load_file(Path(local_path), source_name= filename)
  return await _to_dicts(docs)

@activity.defn(name="split_text_activity", description="Split text into chunks and return them")
async def chunk_document_activity(documents: list[dict])-> list[dict]:
  """Split text in documents into chunks and return them."""
  service= DocumentService()
  chunks= service.split_documents(documents=await _to_documents(documents))
  return await _to_dicts(chunks)