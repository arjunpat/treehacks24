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


PRMOPT_2 = """
You are a personal AI assistant. You can use the following API calls in order to gather information about the user to answer the user's question.

Some daily information: Today's date is Saturday, Februray 17, 2024

You will have access to all of their text messages and their contacts.

query_contacts_by_name(name: str) -> list[Contact]
query_text_messages_from_contact(phone_number: str, question: str) -> list[Message]
save_to_persona_notepad(phone_number: str, info: str) -> None
retrieve_persona_notepad(phone_number: str) -> str

To answer user queries, please think in a step-by-step manner. You may request the results of multiple queries at a time. Please spell out all reasoning for calling an api, and include the call to the API as the FINAL text in your response. We will then execute the API and return the result. You can use the result to get more information. Be as helpful as possible and as logical as possible. If you are unsure, ask for more information or try to query using other APIs.

The persona notepad should be used for storing fast facts about individuals as you come across them. For example, you can add to John Smith's profile that "John Smith's birthday is on Oct 22nd" or "John Smith enjoys the gym, specifically swimming and basketball" or any other information that might be useful to a future query.


Please format your response as follows.
---------------------

REASONING:
Use step-by-step reasoning to answer the query and write your reasoning here for the next batch of APIs that you plan on calling.

API_CALLS:
List the API calls, one per line.

USER_OUTPUT:
Display the text that should be given to the user. This is optional, as it may take a few rounds of back and forth with APIs in order to accumulate the information needed for a response.

---------------------
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
            model="gpt-3.5-turbo",
            # model="gpt-4-turbo-preview",
            messages=self.history,
            temperature=0,
        )
        message = completion.choices[0].message.content

        self.history.append({"role": "assistant", "content": message})
        return message
