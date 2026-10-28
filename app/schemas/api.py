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