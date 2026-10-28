from app.utils.logger import get_logger
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.configs.settings import get_settings
from app.services.ingestionService import IngestionService
from app.schemas.api import DocumentBatchUploadDocumentResponse

logger= get_logger(__name__)

router= APIRouter(
  prefix="/documents",
  tags=["Documents"]
)

@router.post(
  "/upload",
  summary="Upload and ingest documents",
  description="Upload one or more documents for ingestion into the vector store.",
  response_model= None
)
async def upload_document(files: list[UploadFile]= File(..., description="The files to upload")):
  settings= get_settings()
  if not files:
    logger.warning("No files provided for upload")
    raise HTTPException(status_code=400, detail="No files provided for upload.")
    
  if len(files)> settings.max_files_per_upload:
    logger.warning("Too many files provided for upload: %d", len(files))
    raise HTTPException(status_code=400, detail=f"Too many files provided for upload. Maximum allowed is {settings.max_files_per_upload}.")
  
  file_pairs= list[tuple[str, bytes]]= []

  for file in files:
    if not file.filename:
      logger.warning("File with no filename provided")
      raise HTTPException(status_code=400, detail="One of the files has no filename.")
    content= await file.read()  # Read the file content
    if not content:
      logger.warning("File '%s' is empty", file.filename)
      raise HTTPException(status_code=400, detail=f"File '{file.filename}' is empty.")
    file_pairs.append((file.filename, content))

  ingestion_service= IngestionService()
  try:
    payload= ingestion_service.ingest_file_sync(file_pairs=file_pairs)
    logger.info("Successfully ingested %d files with a total of %d chunks", payload.get("filesUploaded", 0), payload.get("total_chunks", 0))
  except Exception as e:
    logger.error("Error during file ingestion: %s", str(e))
    raise HTTPException(status_code=500, detail=f"Error during file ingestion: {str(e)}")
  
  return DocumentBatchUploadDocumentResponse(
    message= payload.get("message", "Ingestion completed."),
    total_chunks= payload.get("total_chunks", 0),
    files_uploaded= payload.get("filesUploaded", 0),
    files= payload.get("files", [])
  )

