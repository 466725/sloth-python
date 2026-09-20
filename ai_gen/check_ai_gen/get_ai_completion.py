from __future__ import annotations

import os
from pathlib import Path

from ai_gen.ai_client import OpenAIChatScriptClient, OpenAIClientConfig
from ai_gen.paths import resolve_output_path
from config.config import settings


def generate_example(output_path: str | Path = "temps/ai/check_ai_gen/example.txt") -> Path:
	"""Ask the configured model for a short example and save its response."""

	api_key = os.getenv("OPENAI_API_KEY", "").strip()
	if not api_key:
		raise RuntimeError("OPENAI_API_KEY is required to run this example.")

	client = OpenAIChatScriptClient(
		OpenAIClientConfig(
			api_key=api_key,
			model=settings.ai_generation.model,
			base_url=settings.ai_generation.base_url,
		)
	)
	response = client.generate(
		system_prompt="You are a concise assistant that creates practical Python examples.",
		user_prompt="Write one short, useful tip for making automated tests reliable.",
	)

	destination = resolve_output_path(output_path)
	destination.parent.mkdir(parents=True, exist_ok=True)
	destination.write_text(response + "\n", encoding="utf-8")
	return destination


if __name__ == "__main__":
	print(f"Saved AI response to: {generate_example()}")
