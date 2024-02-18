import asyncio
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime

import chat
import textsearch
from contacts import Contact, get_contacts
from messages import Message, read_imessages

db_path = os.path.expanduser("~/Downloads/chat.db")
contacts = get_contacts()
messages = read_imessages(db_path)

dir_path = os.path.dirname(os.path.realpath(__file__))
persona_notepad_file = os.path.join(dir_path, "persona_notepad.json")
with open(persona_notepad_file, "r") as f:
    persona_notepad = json.loads(f.read())

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
    CONTEXT_LEN = 4

    if "code" in query:
        code_convo = """(1) Arjun - Nov 21, 2019 12:49 pm: yo gonna grab my bag around 4 if that's cool
(2) Tony - Nov 21, 2019, 1:15: sg
(3) Arjun - Nov 21, 2019, 3:49 pm: im here
(4) Tony - Nov 21, 2019, 3:55 pm: shoot sry im not here
(5) Tony - Nov 21, 2019, 3:55 pm: uhhhhh you can prob just come in a grab it
(6) Tony - Nov 21, 2019, 3:56 pm: my door code is 9218
(7) Arjun - Nov 21, 2019, 3:56 pm: thanks
(8) Arjun - Jan 13, 2023, 12:01 am: u better let me crash at ur place big dog
(9) Tony - Jan 13, 2023, 12:15 am: yea ofc
(10) Tony - Jan 13, 2023, 12:15 am: 4993"""
        code_str_list = [(m.split()[0], m.split()[1:], "Arjun" not in m) for m in code_convo.splitlines()]
        return code_convo, code_str_list

    query = query.strip().replace(",", "").split(" ")
    msg_list = messages[phone_number].messages
    # filter messages with the relevant query
    for i in range(len(msg_list)):
        for j in range(len(query)):
            if query[j].lower() in msg_list[i].text.lower():
                # grab 7 around each relevant
                lower = max(0, i - CONTEXT_LEN)
                upper = min(i + CONTEXT_LEN + 1, len(msg_list))
                indices.update(list(range(lower, upper)))

    # grab those messages
    # print(indices)
    msg_str = ""
    msg_str_list: list[tuple[int, Message]] = []
    for idx in indices:
        msg = messages[phone_number].messages[idx]
        if len(msg.text) > 5 and len(msg.text) < 125:
            date_str = format_datetime(msg.date)
            person = contact_name if msg.sender == phone_number else msg.sender

            msg_str += f"({idx}) {person} - {date_str}: {msg.text}\n"

            msg_str_list.append((idx, msg, msg.sender == phone_number))
        # lower = max(0, idx - CONTEXT_LEN)
        # upper = min(idx + CONTEXT_LEN + 1, len(msg_list))
        # msgs = []
        # for i in range(lower, upper):
        #     m = messages[phone_number].messages[i]
        #     msgs.append((m.sender == phone_number, m))
        # msg_str_list.append((idx, msgs))
    # msg_str_list is [(citationId, [(bool, text)])]

    return msg_str, msg_str_list
    if False:
        searcher = textsearch.TextSearcher()
        searcher.load([m.text for m in msg_list], phone_number)
        resp = searcher.search(query)
        return resp


async def call_func(response: str, notify_callback=None):
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
                    if notify_callback:
                        await notify_callback(code)
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


# Further refined function to handle citations with multiple numbers, replacing them with a standardized format for each number
# Adjusting the code to correctly handle citations with multiple numbers and ensure that each citation is replaced with a standardized format for each number, separated by spaces, including handling complex citation formats


def std_citations(text):
    # Find all citations in the text
    citations = re.findall(r"\[([^\]]+)\]", text)

    # This will store the standardized text
    standardized_text = text

    for citation in citations:
        # Extract numbers from the current citation
        citation_numbers = re.findall(r"\d+", citation)

        # Prepare the standardized citation format by including each number
        standardized_citation = " ".join(
            f"{{{{{number}}}}}" for number in citation_numbers
        )

        # Replace the original citation with its standardized format in the text
        # Using `re.escape` to avoid issues with special characters in `citation`
        standardized_text = re.sub(
            r"\[" + re.escape(citation) + r"\]",
            standardized_citation,
            standardized_text,
            count=1,
        )

    # Extract unique numbers from all citations for reference
    all_numbers = re.findall(r"\d+", standardized_text)
    return sorted(set(all_numbers), key=int), standardized_text


response_text = """ Based on the text messages, it appears Tony Xin has expressed romantic interest in at least one individual named Olivia. This is evidenced by a message where Tony mentions hanging out with Olivia because it is their "2 year" [2414], indicating a significant anniversary that suggests a romantic relationship. Additionally, there's another instance where Tony mentions that Olivia is staying over, which could imply a close personal relationship [2002].

However, there isn't clear evidence in the provided messages to confidently identify a second individual Tony Xin might be romantically interested in. The messages mostly revolve around plans with friends, casual conversations, and logistical coordination. While Tony uses affectionate language like "Ok papa" [1650] and "Ok beautiful" [1128], these instances seem more indicative of a playful or affectionate tone rather than clear expressions of romantic interest towards specific individuals other than Olivia.

Therefore, based on the available information:
1. **Olivia** - Tony Xin has mentioned celebrating a two-year anniversary with Olivia [2414], which strongly suggests a romantic relationship.
2. **Unknown** - There isn't sufficient evidence in the messages to identify a second individual Tony Xin is romantically interested in.

It's important to note that the absence of clear evidence for a second individual could be due to the nature of the messages reviewed or the specific queries used. Further investigation with different queries or additional context might reveal more about Tony Xin's romantic interests. """

# Apply the refined function to the original response text
# numbers_v4, standardized_response_v4 = std_citations(response_text)

# print(numbers_v4, standardized_response_v4)


async def main(query="When is Tony Xin's birthday?", notify_callback=None):
    # query = "When was my last skiing trip with Amira and what did we do?"
    # query = "What are Tony's love interests? List two."
    # query = "What is Akash's birthday?"
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
    text_msgs_citations = []
    while True:
        print(r)
        if "USER_OUTPUT:" in r:
            #     print(r)
            idx_of_response = r.index("USER_OUTPUT:")
            final_response = r[idx_of_response + len("USER_OUTPUT:") :]
            if "n/a" not in final_response:
                cits, ff_reponse = std_citations(final_response)
                print("\n" * 10)
                print(ff_reponse)

                get_cits = set()
                for num_str in cits:
                    c = int(num_str)
                    get_cits.update((c - 1, c, c + 1))

                final_cits = {}
                for c, m, isOther in text_msgs_citations:
                    if c in get_cits:
                        final_cits[c] = {
                            "speaker": "other" if isOther else "self",
                            "text": m.text,
                        }

                print(final_cits)

                return 0, ff_reponse, final_cits  # exit with success
                # else:
                return 1, final_response, None  # exit with no success
        code, output = await call_func(r, notify_callback)
        if output:
            new_input = ""

            for i in range(len(code)):
                if isinstance(output[i], tuple):
                    text_msgs_citations += output[i][1]
                    new_input += f"Output of {code[i]}:\n{output[i][0]}\n\n"
                else:
                    new_input += f"Output of {code[i]}:\n{output[i]}\n\n"

            # new_input += "The persona notepad should be used for storing fast facts . For example, add birthdays, hobbies, etc. "
            new_input += f"Please respond with further API_CALLS or USER_OUTPUT (cite sources, provide good reasoning, summarize steps) to answer the query. Be very verbose and friendly in your USER_OUTPUT, providing as much information as possible.: {query}"
            print(new_input)
            r = chat_instance.chat(new_input)
        else:
            print("am confused", r)
            break
    return 2, r, None  # exit with error


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
