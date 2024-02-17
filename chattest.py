import re
from typing import Any
import chat

# fake modeled class aaa
class Contact:
    def __init__(
        self, first_name: str, last_name: str, phone_numbers: list[str]
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.phone_numbers = phone_numbers

    def __repr__(self) -> str:
        return f"Contact(first_name={self.first_name}, last_name={self.last_name}, phone_numbers={self.phone_numbers})"

    def __str__(self):
        return repr(self)

r = """I will first need to retrieve Stephan's contact information in order to find his phone number. Let me query the contacts for Stephan. 

query_contacts_by_name("Stephan")"""


def fake_query(s: str):
    print(f"Querying {s}")

def query_contacts_by_name(name: str) -> list[Contact]:
    print("query_contacts_by_name")
    return Contact("First", "Last", ["+1234567890","+12223334444"])
    
def query_text_messages_from_contact(phone_number: str, query: str) -> str: # list[Message]
    # *query must be a singular word*
    print("query_text_messages_from_contact")
    person = "Person"
    date_str = "02/17/2024"
    msg = "message"
    return f"{person} - {date_str}: {msg}\n" + f"{person} - {date_str}: 'you're invited to my birthday party on 10/22'"

def save_to_persona_notepad(phone_number: str, info: str) -> None:
    print("save_to_persona_notepad")

def retrieve_persona_notepad(phone_number: str) -> str:
    print("retrieve_persona_notepad")
    return "Persona {}"

def call_func(response: str):
    code_parser = re.compile(r"((?:query).*|(?:save).*|(?:retrieve).*)\(.*\)", re.MULTILINE)
    # if m := parser.match(response.splitlines()[-1]):
    parts = response.split("\n\n")
    for part in parts:
        lines = [l.strip() for l in part.strip().splitlines()]
        results = []
        if "API_CALLS" in lines[0]:
            for line in lines[1:]:
                if code_match := code_parser.search(line):
                    code = code_match.group(0)
                    # super secure 😎
                    try:
                        results.append(eval(code))
                    except:
                        results.append("(error)")
                else:
                    results.append("(error: api not recognized)")
            return lines[1:], results
    else:
        return None, False


chat_instance = chat.Chat()
r = chat_instance.chat("When is Tony's birthday?")

while True:
    if "USER_OUTPUT:" in r:
        print(r)
        break
    code, output = call_func(r)
    if output:
        print(r)
        print(output)
        r = chat_instance.chat(
            f"Here is the output of calling the following api function {code}:\n\n\n\n{output}"
        )
    else:
        print("am confused", r)
        break