from app.core.config import settings
from app.ai.base import AIProvider
from app.ai.mock import MockProvider
from app.ai.gemini import GeminiProvider

def get_ai_provider() -> AIProvider:
    if settings.AI_PROVIDER == "gemini" and settings.GEMINI_API_KEY:
        return GeminiProvider(api_key=settings.GEMINI_API_KEY)
    else:
        # Defaults to MockProvider if no key is provided
        return MockProvider()
