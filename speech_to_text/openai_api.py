import httpx
import openai
import os
from openai import OpenAI
from urllib.parse import urljoin



class OpenAIAPI:
    def __init__(self):
        self.base_url = os.getenv("OPENAI_BASE_URL")


    def text_proofreading(self, text: str):
        CHAT_COMPLETION_PATH = 'audio/completions/text'
        response = httpx.post(
            urljoin(self.base_url, CHAT_COMPLETION_PATH),
            data={'content',text}
        )
        return response.choices[0]["message"]["content"].strip()

    # def file_proofreading(self, fd: File):
    #     self.base_url = os.getenv("OPENAI_BASE_URL")
    #     self.openai_client = OpenAI(base_url=f"{self.base_url}", api_key=f"{self.api_key}")
    #     self.MODEL_NAME = "gpt-3.5-turbo"
    #     response = self.openai_client.post(
    #         OPENAI_BASE_URL + CHAT_COMPLETION_PATH,
    #         files={"file": fd},
    #         data=REQUEST_KWARGS,
    #     )
    #     return response.choices[0]["message"]["content"].strip()



