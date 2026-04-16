import os
from litellm import completion

api_key = os.getenv("OPENAI_API_KEY", "").strip()
base_url = os.getenv("AI_GEN_BASE_URL", "").strip()
model = os.getenv("AI_GEN_MODEL", "").strip()

if not api_key or not model:
    raise ValueError("Missing required environment variables")

response = completion(
    model=model,
    messages=[{"role": "user", "content": "Hello, how are you?"}],
    api_key=api_key,
    base_url=base_url if base_url else None,  # optional
)

print(response["choices"][0]["message"]["content"])
