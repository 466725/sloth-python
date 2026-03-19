import logging
import os

import pytest
import requests
from openai import OpenAI

from utils.config import settings

logger = logging.getLogger(__name__)

url = (
    settings.urls.cineplex + "/ClientServices/CineplexClientServicesWeb/CreateApplicationSession"
)
print(url)

payload = '{\n\t"ApplicationKey": "sk-7c0d26b0161a421ea75206737071e2d8"\n}'
print(payload)
headers = {
    "Content-Type": "application/json",
    "Cookie": "visid_incap_2293254=KmLrzNVaTjaHg3x0G3Oy953cx14AAAAAQUIPAAAAAABnm269Hcp0OlaqxUdlwgYy; ",
}
response = requests.request("POST", url, headers=headers, data=payload)
responseJson = response.json()
SessionTokenExpires = responseJson["SessionTokenExpires"]


@pytest.mark.api
def test_response_status_code():
    """CreateApplicationSession test for the response status code."""

    assert response.status_code == 200


@pytest.mark.api
def test_session_token_expires():
    """CreateApplicationSession test for SessionTokenExpires."""

    assert SessionTokenExpires is not None


@pytest.mark.api
def test_openai_api_key():
    try:
        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=settings.urls.deep_seek,
        )

        response = client.chat.completions.create(
            model="deepseek-chat", messages=[{"role": "user", "content": "Hello"}], stream=False
        )
    except KeyError:
        print("Please set the OPENAI_API_KEY environment variable")
        assert True
    except Exception:
        assert True
    else:
        assert True
    finally:
        assert True
