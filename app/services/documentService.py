from app.configs import Settings
from app.utils import get_logger
from pathlib import Path as PATH
import csv
from langchain_core.documents import Documents
from langchain_text_splitters import RecursiveCharaterTextSplitter


logger= get_logger(__name__)

class DocumentService:

  SUPPORTED_FILE_EXTENSIONS= {".csv"}

  def __init__(slef, chunk_size: int | None = None, chunk_overlap: int | None = None):
    settings= Settings()
    self.chunk_size= chunk_size or settings.chunk_size
    self.chunk_overlap= chunk_overlap or settings.chunk_overlap

    self.text_splitter= RecursiveCharaterTextSplitter(
      chunk_size=self.chunk_size,
      chunk_overlap=self.chunk_overlap,
      seperator= ["/n/n", "/n", " ", ""],
      length_function= len
    )

  def load_csv_documents(self, file_path: PATH) -> list[Documents]:
    """Load CSV documents from the given file path."""

    documents: list[Documents]= []

    with file_path.open(newline="", encoding="utf-8") as csvfile:
      reader= csv.DictReader(csvfile)
      
      for row in reader:
        text= row.get("text") 

        if not text:
          logger.warning("Row missing 'text' field; skipping row: %s", row)
          continue

        metadata= {
          "id": row.get("id"),
          "start": row.get("start"),
          "end": row.get("end"),
          "url": row.get("url"),
          "channel_id": row.get("channel_id"),
          "title": row.get("title"),
          "published": row.get("published"),
        }

        documents.append(Documents(page_content=text, metadata=metadata))

    return documents

