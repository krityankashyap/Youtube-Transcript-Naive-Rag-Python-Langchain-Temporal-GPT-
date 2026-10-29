from dataclasses import dataclass, field

@dataclass
class FileItem:
  """A single file to ingest, already saved to disk."""
  local_path: str
  filename: str

@dataclass
class IngestionWorkflowInput:
  """Input passed to the ingestion workflow."""

  batch_id: str
  files: list[FileItem] = field(default_factory=list)

@dataclass
class FileIngestionResult:
  """Result of ingesting a single file."""

  source: str
  chunks_added: int
  status: str = "success"
  error: str | None = None

@dataclass
class IngestionWorkflowResult:
  """Result of the ingestion workflow."""

  total_chunks: int
  files_uploaded: int
  files: list[FileIngestionResult] = field(default_factory=list)
  message: str= ""