from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Setting(BaseSettings):
    """env Settings for the applications"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # GROQ_AI
    groq_api_key: str = ""

    # Qdrant
    qdrant_url: str = ""

    # Temporal
    temporal_host: str = ""
    temporal_namespace: str = ""
    temporal_task_queue: str = ""

    # Collections and models
    collection_name: str = ""
    embedding_model: str = ""
    llm_model: str = ""
    llm_temperature: float = 0.0
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_k: int = 5

    # API
    api_host: str = ""
    api_port: int = 8000
    log_level: str = "INFO"
    app_name: str = "YouTubeTransciptNaiveRAGDemo"

    # Upload limits
    max_files_per_upload: int = 10
    index_batch_size: int = 100

    # Ingestion mode: false = sync (Stage 4), true = Temporal worker required
    use_temporal_ingestion: bool = False

    # Optional RAGAS (Stage 6)
    enable_ragas_evaluation: bool = False

@lru_cache
def get_settings() -> Setting:
    """Get the settings for the application."""
    return Setting()
