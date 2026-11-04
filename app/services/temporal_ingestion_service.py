from app.utils.logger import get_logger
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
        "message": f"Started batch ingestion workflow for {len(files)} files.",
      }
    )
