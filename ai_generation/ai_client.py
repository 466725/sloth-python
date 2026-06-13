from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


@dataclass(frozen=True)
class OpenAIClientConfig:
    api_key: str
    model: str
    base_url: str | None = None
    timeout_seconds: int = 60


class OpenAIChatScriptClient:
    def __init__(self, config: OpenAIClientConfig):
        self.config = config
        self._client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout_seconds,
        )

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        messages: list[ChatCompletionMessageParam] = [
            cast(ChatCompletionMessageParam, {"role": "system", "content": system_prompt}),
            cast(ChatCompletionMessageParam, {"role": "user", "content": user_prompt}),
        ]
        response = self._client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=0.2,
        )
        return (response.choices[0].message.content or "").strip()

