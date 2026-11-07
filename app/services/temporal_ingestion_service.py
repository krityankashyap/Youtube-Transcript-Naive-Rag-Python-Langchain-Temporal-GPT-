from app.utils.logger import get_logger
from dataclasses import asdict
from app.configs.settings import get_settings
from app.services.ingestionService import IngestionService
from app.temporal.workflow.ingestion import FileIngestInput
from app.temporal.client import temporal_client
from app.temporal.workflow.ingestion import BatchIngestionWorkflow

logger= get_logger(__name__)

class TemporalIngestionService:
  """Service to handle ingesting documents into the vector store using Temporal workflows."""

  def __init__(self):
    self.settings= get_settings()
    self.ingestionService= IngestionService()

  async def start_batch_ingestion(self, files: list[tuple[str, bytes]]) -> dict:
    """Start a Temporal workflow to ingest a batch of files."""
    batch_id, paths= self.ingestionService.save_batch_upload(files)

    file_inputs= [
      FileIngestInput(filename= path.name, local_path= str(path)) for path in paths
    ]

    client= await temporal_client()
    workflow= await client.start_workflow(
      BatchIngestionWorkflow.run,
      file_inputs,
      id= f"batch_ingest_{batch_id}",
      task_queue= self.settings.temporal_task_queue,

    )

    logger.info("Started batch ingestion workflow with ID: %s", workflow.id)

    return (
      {
        "workflow_id": workflow.id,
        "run_id": workflow.run_id,
        "batch_id": batch_id,
        "files_total": len(files),
        "files_name": [file_inputs.filename for file_inputs in file_inputs],
        "message": f"Started batch ingestion workflow for {len(files)} files.",
      }
    )
  
  async def get_ingestion_status(self, workflow_id: str) -> dict:
    """Get the status of a Temporal workflow."""
    client= await temporal_client()
    handle= client.get_workflow_handle(workflow_id)  # Get a workflow handle to an existing workflow by its ID.

    progress= 0

    try:
      progress= await handle.query(BatchIngestionWorkflow.get_progress)
    except Exception as e:
      logger.error("Error querying workflow progress for ID %s: %s", workflow_id, str(e))
      return {"workflow_id": workflow_id, "error": str(e)}
    
    if progress:
      data= asdict(progress)
      return {
        "workflow_id": workflow_id,
        "status": data.get("status"),
        "files_completed": data.get("files_completed"),
        "files_total": data.get("files_total"),
        "current_filename": data.get("current_filename"),
        "file_result": data.get("file_result"),
      }

