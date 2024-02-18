import json
import os
import re
from datetime import datetime

import chat
import textsearch
from contacts import Contact, get_contacts
from messages import read_imessages

db_path = os.path.expanduser("~/Downloads/chat.db")
contacts = get_contacts()
messages = read_imessages(db_path)

dir_path = os.path.dirname(os.path.realpath(__file__))
persona_notepad_file = os.path.join(dir_path, "persona_notepad.json")
with open(persona_notepad_file, "r") as f:
    persona_notepad = json.loads(f.read())

audit = ["+16505189339"]

"""
Arjun - Nov 21, 2019 12:49 pm: yo gonna grab my bag around 4 if that's cool
Tony - Nov 21, 2019, 1:15: sg
Arjun - Nov 21, 2019, 3:49 pm: im here
Tony - Nov 21, 2019, 3:55 pm: shoot sry im not here
Tony - Nov 21, 2019, 3:55 pm: uhhhhh you can prob just come in a grab it
Tony - Nov 21, 2019, 3:56 pm: my door code is 9218
Arjun - Nov 21, 2019, 3:56 pm: thanks
Arjun - Jan 13, 2023, 12:01 am: u better let me crash at ur place big dog
Tony - Jan 13, 2023, 12:15 am: yea ofc
Tony - Jan 13, 2023, 12:15 am: 4993
"""


# What is Tony's door code?
# What did I do in Hawaii last summer?
# Can you suggest gifts for Gaurav Chak for his birthday?


def retrieve_persona_notepad(phone_number: str):
    if phone_number not in messages:
        return "Expected a valid phone number of a contact."

    if phone_number not in persona_notepad:
        return f"Persona notepad for {phone_number} currently empty. Please add to it when you acquire new information"

    return "\n".join(persona_notepad[phone_number])


def save_to_persona_notepad(phone_number: str, info: str):
    if phone_number not in persona_notepad:
        persona_notepad[phone_number] = []

    persona_notepad[phone_number].append(info)

    with open(persona_notepad_file, "w") as f:
        f.write(json.dumps(persona_notepad))

    return "Succesfully saved to persona notepad."


def format_datetime(dt):
    """
    Formats a datetime object into a string with the format 'dd MMM yyyy at hh:mm AM/PM'.

    Args:
    dt (datetime): A datetime object to be formatted.

    Returns:
    str: The formatted datetime string.
    """
    return dt.strftime("%d %b %Y at %I:%M %p")


def query_contacts_by_name(name: str):
    potential_contact_list = []
    # TODO: can be improved, ask to list multiple spellings
    name = name.strip().lower().split(" ")

    for con in contacts:
        keywords = [con.first_name.lower(), con.last_name.lower()]
        keywords = [e for e in keywords if e is not None and e != ""]

        for i in range(len(name)):
            for j in range(len(keywords)):
                if name[i] in keywords[j] or keywords[j] in name[i]:
                    potential_contact_list.append(con)

    return "\n".join([str(c) for c in potential_contact_list])


def remove_non_numbers(s):
    # Use a list comprehension to filter out non-digit characters
    filtered_chars = [char for char in s if char.isdigit()]
    # Join the list back into a string
    return "".join(filtered_chars)


def get_contact_from_phone_number(phone_number: str) -> list[Contact]:
    potential_contact_list = []

    for con in contacts:

        pns = [remove_non_numbers(c) for c in con.phone_numbers if isinstance(c, str)]
        # if con.first_name == "Stephan":
        # print(remove_non_numbers(phone_number), pns)
        if any([remove_non_numbers(phone_number) == c for c in pns]):
            potential_contact_list.append(con)

    return potential_contact_list


""" def query_all_text_messages_from_contact(phone_number: str):

    if phone_number not in messages:
        return "Could not find any messages with this phone number"

    contact_list = get_contact_from_phone_number(phone_number)

    assert len(contact_list) > 0
    contact = contact_list[0]
    contact_name = f"{contact.first_name} {contact.last_name}"

    msg_list = ""

    for msg in messages[phone_number].messages:
        date_str = format_datetime(msg.date)
        person = contact_name if msg.sender == phone_number else msg.sender

        msg_list += f"{person} - {date_str}: {msg.text}\n"

    return msg_list
 """


def query_text_messages_from_contact(phone_number: str, query: str):
    if phone_number not in messages:
        return "Could not find any messages with this phone number"

    contact_list = get_contact_from_phone_number(phone_number)

    assert len(contact_list) > 0
    contact = contact_list[0]
    contact_name = f"{contact.first_name} {contact.last_name}"

    indices = set()

    query = query.strip().split(" ")
    msg_list = messages[phone_number].messages
    # filter messages with the relevant query
    for i in range(len(msg_list)):
        for j in range(len(query)):
            if query[j].lower() in msg_list[i].text.lower():
                # grab 7 around each relevant
                lower = max(0, i - 7)
                upper = min(i + 7 + 1, len(msg_list))
                indices.update(list(range(lower, upper)))

    # grab those messages
    # print(indices)
    msg_str = ""
    for idx in indices:
        msg = messages[phone_number].messages[idx]
        date_str = format_datetime(msg.date)
        person = contact_name if msg.sender == phone_number else msg.sender

        msg_str += f"({idx}) {person} - {date_str}: {msg.text}\n"

    # return msg_str
    if False:
        return """
1. Arjun - Nov 21, 2019 12:49 pm: yo gonna grab my bag around 4 if that's cool
2. Tony - Nov 21, 2019, 1:15: sg
3. Arjun - Nov 21, 2019, 3:49 pm: im here
4. Tony - Nov 21, 2019, 3:55 pm: shoot sry im not here
5. Tony - Nov 21, 2019, 3:55 pm: uhhhhh you can prob just come in a grab it
6. Tony - Nov 21, 2019, 3:56 pm: my door code is 9218
7. Arjun - Nov 21, 2019, 3:56 pm: thanks
8. Arjun - Jan 13, 2023, 12:01 am: u better let me crash at ur place big dog
9. Tony - Jan 13, 2023, 12:15 am: yea ofc
10. Tony - Jan 13, 2023, 12:15 am: 4993
"""
    else:
        searcher = textsearch.TextSearcher()
        searcher.load(messages[phone_number].messages, phone_number)
        resp = searcher.search(query)
        return resp


def call_func(response: str):
    code_parser = re.compile(
        r"((?:query).*|(?:save).*|(?:retrieve).*)\(.*\)", re.MULTILINE
    )
    # if m := parser.match(response.splitlines()[-1]):
    parts = response.split("\n\n")
    for part in parts:
        lines = [l.strip() for l in part.strip().splitlines()]
        codelines = []
        results = []
        if "API_CALLS" in lines[0]:
            for line in lines[1:]:
                if code_match := code_parser.search(line):
                    code = code_match.group(0)
                    codelines.append(code)
                    # super secure 😎
                    try:
                        results.append(eval(code))
                    except Exception as e:
                        results.append(str(e))
                else:
                    results.append("(error: api not recognized)")
            return codelines, results
    else:
        return None, False


def main(query=""):
    query = "When is Tony's door code?"
    if query.strip() == "":
        return ""
    # result = query_contacts_by_name("Tony")
    # print(result)
    # print("\n" * 10)
    # result = query_text_messages_from_contact("+16505189339", "birthday")
    # print(result)
    # result = query_text_messages_from_contact("+16504956014", "birthday")
    # print(result)
    # return

    chat_instance = chat.Chat()

    r = chat_instance.chat(query)
    while True:
        print(r)
        if "USER_OUTPUT:" in r:
            #     print(r)
            idx_of_response = r.index("USER_OUTPUT:")
            final_response = r[idx_of_response + len("USER_OUTPUT:") :]
            if "n/a" not in final_response:
                print("\n" * 10)
                print(final_response)
                return 0, final_response  # exit with success
            # else:
            #     return 1, final_response  # exit with no success
        code, output = call_func(r)
        if output:
            new_input = ""

            for i in range(len(code)):
                new_input += f"Output of {code[i]}:\n{output[i]}\n\n"

            # new_input += "The persona notepad should be used for storing fast facts . For example, add birthdays, hobbies, etc. "
            new_input += f"Please respond with further API_CALLS or USER_OUTPUT (cite sources, provide good reasoning, summarize steps) to answer the query. Be very verbose and friendly in your USER_OUTPUT, providing as much information as possible.: {query}"
            print(new_input)
            r = chat_instance.chat(new_input)
        else:
            print("am confused", r)
            break
    return 2, r  # exit with error


if __name__ == "__main__":
    main()
