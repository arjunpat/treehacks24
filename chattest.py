import re

import chat

parser = re.compile(r"(query.*)\((.*)\)")

r = """I will first need to retrieve Stephan's contact information in order to find his phone number. Let me query the contacts for Stephan. 

query_contacts_by_name("Stephan")"""


def fake_query(s: str):
    print(f"Querying {s}")


def call_func(response: str):
    if m := parser.match(response.splitlines()[-1]):
        print(m.group(0))
        func = m.group(1)
        params = m.group(2)
        if func == "query_contacts_by_name":
            fake_query(params.strip('"'))


chatter = chat.Chat()
res = chatter.chat("What is Stephan's phone number?")
print(res)
