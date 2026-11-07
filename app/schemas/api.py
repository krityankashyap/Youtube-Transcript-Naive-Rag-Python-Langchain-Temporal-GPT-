from pydantic import BaseModel, Field
from datetime import datetime

class HealthResponse(BaseModel):
    """Response for the health check endpoint."""

    status: str = Field(..., description="The status of the application.")
    timestamp: datetime = Field(..., description="The timestamp of the response.")

class DocumentBatchUploadDocumentResponse(BaseModel):
    """Schema for batch document upload response."""

    message: str = Field(..., description="A message summarizing the upload result.")
    total_chunks: int = Field(..., description="Total number of chunks added across all files.")
    files_uploaded: int = Field(..., description="Total number of files processed.")
    files: list[dict]= Field(..., description="List of files processed with their respective chunk counts.")

class AsyncStartedResponse(BaseModel):
    """Schema for asynchronous ingestion start response."""

    workflow_id: str = Field(..., description="The ID of the started workflow.")
    run_id: str = Field(..., description="The run ID of the started workflow.")
    batch_id: str = Field(..., description="The unique batch ID for the ingestion.")
    files_total: int = Field(..., description="Total number of files in the batch.")
    files_name: list[str] = Field(..., description="List of filenames in the batch.")
    message: str = Field(..., description="A message summarizing the workflow start result.")

class IngestionStatusResponse(BaseModel):
    """Schema for ingestion status response."""

    workflow_id: str = Field(..., description="The ID of the workflow.")
    status: str = Field(..., description="Current status of the workflow (e.g., RUNNING, COMPLETED).")
    files_completed: int = Field(..., description="Number of files completed in the workflow.")
    files_total: int = Field(..., description="Total number of files in the workflow.")
    current_filename: str = Field(..., description="The filename currently being processed.")
    file_result: list[dict] = Field(..., description="List of results for each file processed.")