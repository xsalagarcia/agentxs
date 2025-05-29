from agents import set_default_openai_key

from agentxs.settings.settings import settings

set_default_openai_key(settings.env_settings.api_key_openai)