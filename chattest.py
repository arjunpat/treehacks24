import re
from typing import Any
import chat
import textsearch

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
    return Contact("Clement", "Chan", ["+1234567890","+12223334444"])
    
def query_text_messages_from_contact(phone_number: str, query: str) -> str: # list[Message]
    # *query must be a singular word*
    print("query_text_messages_from_contact")
    person = "Clement"
    date_str = "02/17/2024"
    msgs = [
        "heyyy",
        "What are you up to",
        "bro did you do the hw yet",
        "btw I've got a party tmr",
        "oh shoot what occasion?",
        "it's my birthday!",
        "yoooo no way, how old will you be?"
        "21",
        "congratssss"
    ]
    for i in range(len(msgs)):
        if i % 2 == 0:
            person = "Foobar"
        else:
            person = "Clement"
        msgs[i] = f"{person} - {date_str}: {msgs[i]}"
    print(msgs)
    searcher = textsearch.TextSearcher()
    searcher.load(msgs, person)
    resp = searcher.search(query)
    # return f"{person} - {date_str}: {msg}\n" + f"{person} - {date_str}: 'you're invited to my birthday party on 10/22'"
    print(resp)
    return resp

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

def main(q):
    chat_instance = chat.Chat()
    r = chat_instance.chat(q)

    while True:
        if "USER_OUTPUT:" in r:
            print(r)
            return 0, r
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
    return 2, r

if __name__ == "__main__":
    main("When is Clement's birthday?")