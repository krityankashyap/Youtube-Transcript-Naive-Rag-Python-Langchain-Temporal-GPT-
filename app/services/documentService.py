from app.configs import Settings
from app.utils import get_logger
from pathlib import Path as PATH
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

    return documents

