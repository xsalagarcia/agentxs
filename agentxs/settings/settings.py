import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

_config_dict = SettingsConfigDict(env_file=Path(__file__).parent.parent.parent.joinpath(".env"))


class EnvSettings(BaseSettings):
    api_key_openai: str

    model_config = _config_dict


class Settings(BaseModel):
    data_folder: Path = Path(__file__).parent.parent.joinpath("data_folder")
    env_settings: EnvSettings = EnvSettings()


settings = Settings()

settings.data_folder.mkdir(exist_ok=True)
