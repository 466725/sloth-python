import os

from openai import OpenAI
# KeyError: 'OPENAI_API_KEY' happens, because you didn't set OPENAI_API_KEY environment variable'
try:
    client = OpenAI(api_key = os.environ["OPENAI_API_KEY"]),
except KeyError:
    print("Please set the OPENAI_API_KEY environment variable")
    exit(1)
base_url = "https://api.deepseek.com"

response = (client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "Hello"}
    ],
    stream=False
))

print(response.choices[0].message.content)

def test_response():

    """Base test function for response validation."""

    assert response.choices[0].message.content is None

def test_response_content_length():

    """Base test function for response content length validation."""

    assert len(response.choices[0].message.content) > 0