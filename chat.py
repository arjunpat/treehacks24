import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

PROMPT = """You are a personal AI assistant. You can use the following API calls in order to gather information about the user to answer the user's question.

Some daily information: Today's date is Saturday, Februray 17, 2024

You will have access to all of their text messages and their contacts.


You can query for a list of contacts by using the followinng query.

query_contacts_by_name(name: str)

ex: To answer "What is Stephan's address?" -> query_contacts_by_name("Stephan")

If there are duplicate contacts, reply "RESPONSE TO USER: There are a few contacts matching Stephan. Which one would you like: {list contacts with numbers}"

You can query messages that include certain words by using the following query:

query_text_messages_from_contact(phone_number: str, query: str)

This query will return all messages from this contact with the query string plus the 7 messages before and after the matches messages.


For more complex queries that require contextual information, you can query the entire chat history with another user by using the following query:

query_all_text_messages_from_contact(phone_number: str) To answer "What would be a good gift for user?"

This would be good for scenarios such as asking what gift someone would appreciate. 

To answer user queries, please think in a step-by-step manner and use ONE query at a time. Please spell out all reasoning for calling an api, and include the call to the API as the FINAL text in your response. We will then execute the API and return the result. You can use the result to get more information. When you are ready to respond to the user, start your reponse with "RESPONSE TO USER:" and we will display the output to the user you are trying to help. Be as helpful as possible and as logical as possible. If you are unsure, ask for more information or try to query using other APIs."""

REMOVED = """
"""

PRMOPT_2 = """
You are a personal AI assistant. You can use the following API calls in order to gather information about the user to answer the user's question.

You will have access to all of their text messages and their contacts.

query_contacts_by_name(name: str) -> list[Contact]
query_text_messages_from_contact(phone_number: str, query: str) -> list[Message]
save_to_persona_notepad(phone_number: str, info: str) -> None
retrieve_persona_notepad(phone_number: str) -> str

Please format your response as follows.

API_CALLS:
List the API calls, one per line. Must be valid Python syntax. For most queries, you will first need to query_contacts_by_name to get the users phone number. Feel free to query_text_messages_from_contact with multiple query words that may be relevant, all in one go. YOU ONLY HAVE ACCESS TO THESE API CALLS.

USER_OUTPUT:
OUTPUT n/a IF YOU DO NOT YET KNOW THE ANSWER. If you give up, please also state that here. It may take a few rounds of back and forth with APIs in order to accumulate the information needed for a response. In USER_OUTPUT, please cite the relevant text message used to get that result using [text_msg_idx] after the message. If there is any ambiguity, please give a well written response explaining it and possible answers.
"""


class Chat:
    def __init__(self):
        self.client = OpenAI()
        self.history = [{"role": "system", "content": PRMOPT_2}]

    def chat(self, query: str):
        self.history.append({"role": "user", "content": query})
        return self._get_chat()

    def _get_chat(self):
        completion = self.client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4-turbo-preview",
            messages=self.history,
            temperature=0,
        )
        message = completion.choices[0].message.content

        self.history.append({"role": "assistant", "content": message})
        return message

    def _get_chat_2(self):
        """completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            # model="gpt-4-turbo-preview",
            messages=self.history,
            temperature=0,
        )
        message = completion.choices[0].message.content"""

        completion = self.client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=[each["content"] for each in self.history],
        )

        message = completion.choices[0].text

        self.history.append({"role": "assistant", "content": message})
        return message
