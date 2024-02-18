import os
import re
from datetime import datetime

import chat
from contacts import Contact, get_contacts
from messages import read_imessages

db_path = os.path.expanduser("~/Downloads/chat.db")
contacts = get_contacts()
messages = read_imessages(db_path)


def format_datetime(dt):
    # Dictionary to hold day suffixes
    suffixes = {1: "st", 2: "nd", 3: "rd"}

    # Get the day of the month and the suffix
    day = dt.day
    # Use the suffix for 1st, 2nd, 3rd; otherwise, use 'th'
    suffix = suffixes.get(day if day < 20 else day % 10, "th")

    # Format the datetime string
    formatted_date = dt.strftime(f"%d{suffix} %B, %Y at %I:%M %p")

    # Replace the zero-padded day with the day without leading zero
    return formatted_date.replace(f"0{day}{suffix}", f"{day}{suffix}")


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


def query_all_text_messages_from_contact(phone_number: str):

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


def query_text_messages_from_contact(phone_number: str, query: str):
    if phone_number not in messages:
        return "Could not find any messages with this phone number"

    contact_list = get_contact_from_phone_number(phone_number)

    assert len(contact_list) > 0
    contact = contact_list[0]
    contact_name = f"{contact.first_name} {contact.last_name}"

    indices = set()

    msg_list = messages[phone_number].messages
    # filter messages with the relevant query
    for i in range(len(msg_list)):
        if query.lower() in msg_list[i].text.lower():
            # grab 7 around each relevant
            lower = max(0, i - 7)
            upper = min(i + 7 + 1, len(msg_list))
            indices.update(list(range(lower, upper)))

    # grab those messages
    print(indices)
    msg_str = ""
    for idx in indices:
        msg = messages[phone_number].messages[idx]
        date_str = format_datetime(msg.date)
        person = contact_name if msg.sender == phone_number else msg.sender

        msg_str += f"{person} - {date_str}: {msg.text}\n"

    return msg_str


def call_func(response: str):
    # parser = re.compile(r"^((?:query).*|(?:save).*|(?:retrieve).*)\((.*)\)")
    # if m := parser.match(response.splitlines()[-1]):
    parts = response.split("\n\n")
    for part in parts:
        lines = [l.strip() for l in part.strip().splitlines()]
        results = []
        if "API_CALLS" in lines[0]:
            for code in lines[1:]:
                # super secure 😎
                try:
                    results.append(eval(code))
                except:
                    results.append("(error)")
            return lines[1:], results
    else:
        return None, False

def main(q):
    q = "When is Tony's birthday?"
    if q.strip() == "":
        return
    # result = query_contacts_by_name("Tony")
    # print(result)
    # print("\n" * 10)
    # result = query_text_messages_from_contact("+16505189339", "birthday")
    # print(result)

    chat_instance = chat.Chat()

    r = chat_instance.chat(q)

    while True:
        if "USER_OUTPUT:" in r:
            print(r)
            return r
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

    # output = call_func(r)
    # print(output)
    # r = chat_instance.chat(output)
    # output = call_func(r)
    # print(r)
    # r = chat_instance.chat(output)
    # print(r)

    # print("ENTIRE HISTORY")
    # print(chat_instance.history)


if __name__ == "__main__":
    main()
