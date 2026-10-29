from temporalio.client import Client
from app.configs.settings import get_settings

async def tempral_client() -> Client:
  """Get the temporal client for the application"""
  settings= get_settings()
  client= await Client.connect(
    address=settings.temporal_url,
    namespace=settings.temporal_namespace
  )
  return client
