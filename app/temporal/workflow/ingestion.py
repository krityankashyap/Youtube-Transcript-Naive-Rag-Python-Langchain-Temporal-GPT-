from dataclasses import dataclass
from dataclasses import field
from typing import Any
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
  from app.temporal.activity.Ingestion import (
    parse_document_activity,
    chunk_document_activity,
    index_document_activity
  )

DEFAULT_INDEX_BATCH_SIZE = 100

@dataclass
class FileIngestInput:
  filename: str
  local_path: str

@dataclass
class BatchIngestProgress:
  status: str= "RUNNING"
  files_completed: int= 0
  files_total: int= 0
  current_filename: str= ""
  file_result: list[dict[str, Any]]= field(default_factory=list)

@workflow.defn(name="batch_ingest_workflow")
class BatchIngestionWorkflow:
  """A workflow to ingest a batch of files into the vector store."""

  def __init__(self):
    self.progress= BatchIngestProgress()
  
  @workflow.query(name="get_progress")
  def get_progress(self) -> BatchIngestProgress:
    """Get the current progress of the workflow."""
    return self.progress
  
  @workflow.run
  async def run(self, files: list[FileIngestInput]) -> BatchIngestProgress:
    """Workflow to ingest the batch of file into the vector store"""

    batch_size: int= DEFAULT_INDEX_BATCH_SIZE
    self.progress.files_total= len(files)
    self.progress.status= "RUNNING"

    for file_input in files:
      self.progress.current_filename= file_input.filename

      doc_dicts = await workflow.execute_activity(
        parse_document_activity,
        args= (file_input.local_path, file_input.filename),
        start_to_close_timeout= 60
      )

      chunk_dicts = await workflow.execute_activity(
        chunk_document_activity,
        args= (doc_dicts,),
        start_to_close_timeout= 60
      )

      indexed= 0

      for start in range(0, len(chunk_dicts), batch_size):
        batch= chunk_dicts[start: start + batch_size]
        count= await workflow.execute_activity(
          index_document_activity,
          args= (batch,),
          start_to_close_timeout= 60,
          heartbeat_timeout=5
        )

        indexed += count

      self.progress.files_completed+= 1
      self.progress.file_result.append({
        "filename": file_input.filename,
        "chunk_size": indexed,
        "document_ids": []
      })

    self.progress.status= "COMPLETED"
    self.progress.current_filename= ""
    return self.progress


      
      



