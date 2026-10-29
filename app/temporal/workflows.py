from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from app.temporal.types import IngestionWorkflowInput, IngestionWorkflowResult, FileIngestionResult

with workflow.unsafe.imports_passed_through():
  from app.temporal.activities import parse_document_activity, chunk_document_activity, index_document_activity


@workflow.defn(name="ingestion_workflow")
class IngestionWorkFlow:

  @workflow.run
  async def run(self, input: IngestionWorkflowInput) -> IngestionWorkflowResult:
    """Run the ingestion workflow."""
    # Step 1:- Reusable retry policy + timeout
    retry_policy= RetryPolicy(maximum_attempts=5)
    timeout= timedelta(minutes=5)

    # Step 2:- accumulate results 
    results: list[FileIngestionResult]= []
    total= 0

    # Step 3: process each file through parse -> chunk -> index
    for item in input.files:
      try:
        docs= await workflow.execute_activity(
          parse_document_activity,
          args= [item.local_path, item.filename],
          start_to_close_timeout= timeout,
          retry_policy= retry_policy
        )

        chunks= await workflow.execute_activity(
          chunk_document_activity,
          args= [docs],
          start_to_close_timeout= timeout,
          retry_policy= retry_policy
        )

        count= await workflow.execute_activity(
          index_document_activity,
          args= [chunks],
          start_to_close_timeout= timeout,
          retry_policy= retry_policy
        )

        results.append(FileIngestionResult(source= item.filename, chunks_added= count))
        total+= count
        workflow.logger.info("Successfully ingested file '%s' with %d chunks", item.filename, count)

      except Exception as e:
        workflow.logger.error("Error ingesting file '%s': %s", item.filename, str(e))
        results.append(FileIngestionResult(source= item.filename, chunks_added= 0, status= "failed", error= str(e)))

    # step 4: aggregate and return
    return IngestionWorkflowResult(
      total_chunks= total,
      files_uploaded= len(input.files),
      files= results,
      message= f"Ingested {len(results)} files with a total of {total} chunks."
    )
    