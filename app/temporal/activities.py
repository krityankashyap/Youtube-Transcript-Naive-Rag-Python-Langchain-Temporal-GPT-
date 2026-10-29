from app.services.documentService import DocumentService
from temporalio import activity
from langchain_core.documents import Document
from pathlib import Path


async def _to_dicts(documents: list[Document])-> list[dict]:
  """Convert a list of Document objects to a list of dictionaries."""
  return [doc.to_dict() for doc in documents]



@activity.defn(name="parse_document_activity", description="Parse a document and return its chunks")
async def parse_document_activity(local_path: str, filename: str) -> list[dict]:
  service= DocumentService()
  docs= service.load_file(Path(local_path), source_name= filename)
  return await _to_dicts(docs)