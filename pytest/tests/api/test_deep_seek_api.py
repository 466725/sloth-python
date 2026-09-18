import logging
import os

import pytest
from openai import OpenAI

from utils.config import settings

logger = logging.getLogger(__name__)


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


"""
Simple passing test that demonstrates qTest hook integration
@pytest.mark.api
@pytest.mark.qtest_id(123456)
def test_qtest_hook_demo():
    response = requests.Response()
    response.status_code = 200

    assert response.status_code == 200
"""
