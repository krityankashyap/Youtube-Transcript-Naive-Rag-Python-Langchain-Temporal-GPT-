from app.services.documentService import DocumentService
from app.repositories.vector_store_repository import VectorStoreRepository
from app.configs.settings import get_settings
from pathlib import Path
import uuid
from app.utils import get_logger

logger= get_logger(__name__)

class IngestionService:

  def __self__(self):
    self.document_service= DocumentService()
    self.settings= get_settings()
    self.vector_store_repository= VectorStoreRepository()

  def save_batch_upload(self, file_pairs: list[tuple[str, bytes]]) -> tuple[str, list[Path]]:
    """Save a batch of uploaded files to the designated uploads directory."""
    batch_id= str(uuid.uuid4())
    batch_dir= Path(self.settings.uploads_dir) / batch_id

    paths: list[Path]= []

    for filename, content in file_pairs:
      safe_filename= Path(filename).name
      dest= batch_dir / safe_filename
      dest.write_bytes(content)
      paths.append(dest)
      logger.info("Saved file '%s' to '%s'", filename, dest)

    return batch_id, paths
  
  def ingest_file_at_paths(self, file_path: Path, socurce_name: str | None= None) -> dict:
    """Ingest a file at the given path into the vector store."""
    name= socurce_name or file_path.name 
    chunks= self.document_service.process_file(file_path, source_name=name)

    if not chunks:
      logger.warning("No chunks generated from file '%s'; skipping ingestion", file_path)
      return {"source": name, "chunks_added": 0}
    
    chunks_ids= self.vector_store_repository.add_documents(chunks)
    return {"source": name, "chunks_added": len(chunks_ids), "chunk_ids": chunks_ids}

    



