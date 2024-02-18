import re
from typing import Any
import chat
import textsearch
import asyncio

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

async def call_func(response: str, notify_callback = None):
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
                    if notify_callback:
                        await notify_callback(code)
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

async def main(q, notify_callback = None):

    chat_instance = chat.Chat()

    r = chat_instance.chat(q)
    while True:
        if "USER_OUTPUT:" in r:
            #     print(r)
            idx_of_response = r.index("USER_OUTPUT:")
            final_response = r[idx_of_response + len("USER_OUTPUT:") :]
            if "n/a" not in final_response:
                print("\n" * 10)
                print(final_response)
                return 0, final_response, ["citation 1", "citation 2"]  # exit with success
                # else:
                return 1, final_response, None  # exit with no success
        code, output = await call_func(r, notify_callback)
        if output:
            new_input = ""

            for i in range(len(code)):
                new_input += f"Output of {code[i]}:\n{output[i]}\n\n"

            # new_input += "The persona notepad should be used for storing fast facts . For example, add birthdays, hobbies, etc. "
            new_input += f"Please respond with further API_CALLS or USER_OUTPUT (cite sources, provide good reasoning, summarize steps) to answer the query. Be very verbose and friendly in your USER_OUTPUT, providing as much information as possible.: {q}"
            print(new_input)
            r = chat_instance.chat(new_input)
        else:
            print("am confused", r)
            break
    return 2, r, None  # exit with error

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main("When is Clement's birthday?"))