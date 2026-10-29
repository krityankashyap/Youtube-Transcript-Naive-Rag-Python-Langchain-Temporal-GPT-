import asyncio
from temporalio.worker import Worker
from app.temporal.client import temporal_client
from app.configs.settings import get_settings
from app.temporal.workflows import IngestionWorkFlow
from app.temporal.activities import parse_document_activity, chunk_document_activity, index_document_activity

from app.utils.logger import get_logger

logger= get_logger(__name__)

async def main():
  """Run the temporal worker for document ingestion"""
  settings= get_settings()
  client = await temporal_client()

  worker= Worker(
    client,
    task_queue= settings.temporal_task_queue,
    workflows=[IngestionWorkFlow],
    activities=[parse_document_activity, chunk_document_activity, index_document_activity],
  )
  logger.info("Starting Temporal worker for task queue '%s'", settings.temporal_task_queue)
  await worker.run()


if __name__ == "__main__":
  asyncio.run(main())


