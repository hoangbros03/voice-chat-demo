from settings import Settings
from superlinked import framework as sl

settings = Settings()
openai_config = sl.OpenAIClientConfig(
    api_key=settings.openai_api.key,
    model=settings.openai_api.model,
    base_url=settings.openai_api.base_url,
)
