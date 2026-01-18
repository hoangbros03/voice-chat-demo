from __future__ import annotations

import logging
import os

from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()


logging.basicConfig(level=logging.INFO)

ENV_API_KEY = os.getenv('OPENAI_API_KEY')
ENV_BASE_URL = os.getenv('OPENAI_API_BASE_URL')


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

        self.client = OpenAI(
            base_url=base_url or ENV_BASE_URL or 'https://api.openai.com/v1',
            api_key=api_key or ENV_API_KEY,
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
