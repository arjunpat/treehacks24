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
save_to_persona_notepad(phone_number: str, info: str) -> None
retrieve_persona_notepad(phone_number: str) -> str
"""

PROMPT_2 = """
You are a super helpful personal AI assistant. You can use the following API calls in order to gather information about the user to answer the user's question.

You will have access to all of their text messages and their contacts.

query_contacts_by_name(name: str) -> list[Contact]
query_text_messages_from_contact(phone_number: str, query: str) -> list[Message]


Please format your response as follows.

API_CALLS:
List the API calls, one per line. Must be valid Python syntax. For most queries, you will first need to query_contacts_by_name to get the users phone number. Feel free to query_text_messages_from_contact with multiple query words that may be relevant, all in one go. YOU ONLY HAVE ACCESS TO THESE API CALLS.

USER_OUTPUT:
OUTPUT n/a IF YOU DO NOT YET KNOW THE ANSWER. If you give up, please also state that here. It may take a few rounds of back and forth with APIs in order to accumulate the information needed for a response. In USER_OUTPUT, please cite the relevant text message used to get that result using [text_msg_idx] after the message. If there is any ambiguity, please give a well written response explaining it and possible answers.
"""


EMAIL_PROMPT = """
I have the following email sent to me. Please read it and output a JSON document in the following format. For help parsing the due_date, today's date is Sun Feb 18, 2024. If there are no action items, return a blank JSON array. Reason through due_date in a step-by-step fashion and write a string that is parseable by Python datetime.
```json{
    "action_items": [ // ok to leave empty if none
        {
            "name": "Example Action Item Name",
            "brief_description":"Example action item description of exactly what you need to do.", // HIGHLY CONCISE. just a link OR exact thing to do (<a></a> for links)
            "due_date":"datetime(...)" // include time (like 11:59 PM if necessary)
        }
    ]
}```
"""


class Chat:
    def __init__(self, email=False):
        self.client = OpenAI()
        self.email = email
        if email:
            self.history = [{"role": "system", "content": EMAIL_PROMPT}]
        else:
            self.history = [{"role": "system", "content": PROMPT_2}]

    def chat(self, query: str):
        if self.email:
            return self.chat_without_history(query)
        self.history.append({"role": "user", "content": query})
        return self._get_chat()

    def chat_without_history(self, query: str):
        completion = self.client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": EMAIL_PROMPT},
                {"role": "user", "content": query},
            ],
            temperature=0,
        )
        message = completion.choices[0].message.content

        return message

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

    # unused for now
    # def generate(self, query: str):
    #     self.history.append({"role": "user", "content": query})
    #     stream = self.client.chat.completions.create(
    #         # model="gpt-3.5-turbo",
    #         model="gpt-4-turbo-preview",
    #         messages=self.history,
    #         temperature=0,
    #         stream=True
    #     )
    #     for event in stream:
    #         if "content" in event["choices"][0].delta:
    #             current_response = event["choices"][0].delta.content
    #             yield "data: " + current_response + "\n\n"
