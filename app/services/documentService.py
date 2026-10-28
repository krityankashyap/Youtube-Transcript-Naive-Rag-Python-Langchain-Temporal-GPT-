from app.configs.settings import get_settings
from app.utils import get_logger
from pathlib import Path as PATH
import csv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


logger= get_logger(__name__)

class DocumentService:

  SUPPORTED_FILE_EXTENSIONS= {".csv"}

  TRANSCRIPT_CSV_COLUMNS= ["id", "start", "end", "text", "url", "channel_id", "title", "published"]

  def __init__(self, chunk_size: int | None = None, chunk_overlap: int | None = None):
    settings= get_settings()
    self.chunk_size= chunk_size or settings.chunk_size
    self.chunk_overlap= chunk_overlap or settings.chunk_overlap

    self.text_splitter= RecursiveCharacterTextSplitter(
      chunk_size=self.chunk_size,
      chunk_overlap=self.chunk_overlap,
      separators= ["\n\n", "\n", " ", ""],
      length_function= len
    )
  
  def _is_transcript_csv(self, file_path: PATH) -> bool:
    """Check if the given CSV file is a transcript CSV based on its columns."""
    with file_path.open(newline="", encoding="utf-8") as csvfile:
      reader= csv.DictReader(csvfile)
      if not reader.fieldnames:
        logger.warning("CSV file '%s' has no header; cannot determine if it's a transcript CSV", file_path)
        return False
      
      fields= set(reader.fieldnames)
      expected= set(self.TRANSCRIPT_CSV_COLUMNS)
      return expected.issubset(fields) and len(fields) == len(expected)


  def load_csv_documents(self, file_path: PATH, source_name: str | None= None) -> list[Document]:
    """Load CSV documents from the given file path."""

    documents: list[Document]= []

    with file_path.open(newline="", encoding="utf-8") as csvfile:
      reader= csv.DictReader(csvfile)
      
      for row in reader:
        text= row.get("text") 

        if not text:
          logger.warning("Row missing 'text' field; skipping row: %s", row)
          continue

        metadata= {
          "source": source_name,
          "id": row.get("id"),
          "start": row.get("start"),
          "end": row.get("end"),
          "url": row.get("url"),
          "channel_id": row.get("channel_id"),
          "title": row.get("title"),
          "published": row.get("published"),
        }

        documents.append(Document(page_content=text, metadata=metadata))

    return documents

  def load_file(self, file_path: PATH, source_name: str | None= None) -> list[Document]:
    """Load documents from a file based on its extension."""
    file_path= PATH(file_path)
    source= source_name or file_path.name
    extension= file_path.suffix.lower()

    if extension not in self.SUPPORTED_FILE_EXTENSIONS:
      raise ValueError(f"Unsupported file extension '{extension}' for file '{file_path}'")
    
    if extension == ".csv":
      if not self._is_transcript_csv(file_path):
        raise ValueError(f"CSV file '{file_path}' is not a valid transcript CSV")
      return self.load_csv_documents(file_path, source)
    

  
  def split_documents(self, documents: list[Document]) -> list[Document]:
    """Split documents into chunks using the text splitter."""
    return self.text_splitter.split_documents(documents)

  def process_file(self, file_path: PATH, source_name: str | None= None) -> list[Document]:
    """Load and split documents from a file."""
    documents= self.load_file(file_path, source_name)
    logger.info("Loaded %d documents from file '%s'", len(documents), file_path)
    
    split_documents= self.split_documents(documents)
    logger.info("Split documents into %d chunks", len(split_documents))
    
    return split_documents
    

