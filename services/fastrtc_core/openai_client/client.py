from __future__ import annotations

import logging
import os

from openai import OpenAI
from settings import Settings

logging.basicConfig(level=logging.INFO)
settings = Settings()


class OpenAIClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, base_url=None, api_key=None, model='gpt-4'):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.settings = settings.openai_api

        self.client = OpenAI(
            base_url=base_url or self.settings.base_url or \
                'https://api.openai.com/v1',
            api_key=api_key or self.settings.key,
        )
        self.model = os.getenv('OPENAI_API_MODEL', model)

    def completions(self, messages: list[dict]) -> str:
        try:
            response = self.client.chat.completions.create(
                # ignore: noqa
                model=self.model, messages=messages,
            ).choices[0].message.content
            return str(response)
        except Exception as e:
            logging.error(f"Error during completion: {e}")
            return ''
