"""

                ApiAnalyzer.py
 a class that analyze text by openai API

"""

from openai.error import RateLimitError
import openai
import asyncio

API_KEY = "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"


class ApiAnalyzer:
    def __init__(self):
        self._api_key = API_KEY
        self.chat = self.set_connection_to_api()

    def set_connection_to_api(self):
        """  set the connection to the API
        :return: the system prompt
        """
        openai.api_key = self._api_key
        system_prompt = "You're an AI text analyzer assisting with presentation summarization.For each slide's content" \
                        "you receive, generate a concise summary of the text.\n User:'Slide content'\nAI:'Explanation'"
        return [{"role": "system", "content": system_prompt}]

    @staticmethod
    async def _get_explanation(self):
        """ analyze the text by request to the API, return the response
        :return: the response of the API
        """
        while True:
            try:
                completion = await openai.ChatCompletion.acreate(model="gpt-3.5-turbo", messages=self.chat)
                return completion.choices[0].message.content
            except RateLimitError:
                print("Rate limit error, waiting 20 seconds")
                await asyncio.sleep(20)
            except Exception as e:
                raise e

    async def analyze(self, slide_content, index):
        """ process the text by request to the API, return the response
         :param slide_content: the content of the slide
         :param index: the index of the slide
         :return: the response of the API
        """
        # set instructions to the chat as a user
        self._add_msg("user", slide_content)
        # request and response
        chat_response = await self._get_explanation(self)
        # keeping the history of the chat
        self._add_msg("assistant", chat_response)
        return {"slide_id": index, "analyze": chat_response + "\n"}

    def _add_msg(self, role, content):
        """ add message to the chat
        :param role: the role of the message
        :param content: the content of the message
        """
        self.chat.append({"role": role, "content": content})

# TODO:
#  1. change the rate time error handling
#  2. deside if the class should be singleton
