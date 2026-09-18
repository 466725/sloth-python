from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import cast

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from robot.libraries.BuiltIn import BuiltIn

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    # Ensure local imports resolve when Robot runs this suite directly.
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.config import settings

ROBOT_LIBRARY_SCOPE = "GLOBAL"


def call_deepseek_chat_completion_demo() -> str:
    """Run the same DeepSeek demo call as pytest and return a non-failing status string."""
    try:
        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=settings.urls.deep_seek,
        )

        # Keep strict typing happy for OpenAI message params while still using a custom model name.
        messages: list[ChatCompletionMessageParam] = [
            cast(ChatCompletionMessageParam, {"role": "user", "content": "Hello"})
        ]
        model_name = cast(str, os.getenv("DEEPSEEK_MODEL", "deepseek-chat"))

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=False,
        )
        BuiltIn().log(f"DeepSeek call succeeded with id: {response.id}")
        return "success"
    except KeyError:
        BuiltIn().log("Please set the OPENAI_API_KEY environment variable", level="WARN")
        return "missing_api_key"
    except Exception as exc:  # pragma: no cover - external API/network behavior
        BuiltIn().log(f"DeepSeek call failed but treated as demo pass: {exc}", level="WARN")
        return "error"
