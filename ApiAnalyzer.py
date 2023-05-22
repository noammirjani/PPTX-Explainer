"""

            ApiAnalyzer.py
    --------------------------------
 A class that analyze text by openai API
 Enter your API key in the API_KEY variable
"""
import backoff
import openai

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
        system_prompt = "You're an AI text analyzer assisting with presentation summarization.For each slide's content"\
                        "you receive, generate a concise summary and additional explanation of the text.\n"
        return [{"role": "system", "content": system_prompt}]

    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    async def _get_explanation(self):
        """ analyze the text by request to the API, return the response
        :return: the response of the API
        """
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.chat, timeout=60)
        return completion.choices[0].message.content

    async def analyze(self, slide_content, index):
        """ process the text by request to the API, return the response
         :param slide_content: the content of the slide
         :param index: the index of the slide
         :return: the response of the API
        """
        # set instructions to the chat as a user
        self._add_msg("user", slide_content)
        # request and response
        chat_response = await self._get_explanation()
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
#  1. deside if the class should be singleton
