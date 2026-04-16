import os
from typing import List, Dict, Any, Optional
from litellm import completion


class LitellmClient:
    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            model: Optional[str] = None,
    ):
        self.api_key = (api_key or os.getenv("OPENAI_API_KEY", "")).strip()
        self.base_url = (base_url or os.getenv("AI_GEN_BASE_URL", "")).strip() or None
        self.model = (model or os.getenv("AI_GEN_MODEL", "")).strip()

        if not self.api_key or not self.model:
            raise ValueError("Missing required configuration: api_key or model")

    def chat(
            self,
            messages: List[Dict[str, str]],
            model: Optional[str] = None,
            **kwargs: Any,
    ) -> str:
        """
            Send a chat completion request.

            :param messages: List of messages [{"role": "...", "content": "..."}]
            messages example: [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi! How can I help?"},
                {"role": "user", "content": "Tell me a joke"}
            ]
            :param model: Optional override model
            :param kwargs: Additional LiteLLM parameters (temperature, max_tokens, etc.)
            :return: Response text
        """
        response = completion(
            model=model or self.model,
            messages=messages,
            api_key=self.api_key,
            base_url=self.base_url,
            **kwargs,
        )

        return response["choices"][0]["message"]["content"]

    def simple_chat(self, prompt: str, **kwargs: Any) -> str:
        """
            Convenience wrapper for single user prompt.
        """
        return self.chat(
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )


if __name__ == "__main__":
    aiclient = LitellmClient()

    response = aiclient.simple_chat("How are you?")
    print(response)

    response = aiclient.chat(messages=[{"role": "user", "content": "How are you?"}])
    print(response)
