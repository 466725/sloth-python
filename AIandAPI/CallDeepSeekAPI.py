import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"]),
base_url = "https://api.deepseek.com"

response = client.chat.completions.create(
    model = "deepseek-chat",
    messages = [
        {"role": "user", "content": "Hello"}
    ],
    stream = False
)

print(response.choices[0].message.content)
