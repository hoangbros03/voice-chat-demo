from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class OpenAISettings(BaseModel):
    key: str
    base_url: str
    model: str


class SearchAPISettings(BaseModel):
    key: str


class MCPSettings(BaseModel):
    server_url: str = ''


class DatasetSettings(BaseModel):
    path: str


class Settings(BaseSettings):
    openai_api: OpenAISettings
    search: SearchAPISettings
    mcp: MCPSettings
    dataset: DatasetSettings

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file='../../.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_nested_delimiter='__',
        case_sensitive=False,
        frozen=True,
    )
