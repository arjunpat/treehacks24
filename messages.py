import sqlite3
from datetime import datetime
from typing import Union

import typedstream


class Thread:
    def __init__(self, display_name: Union[str, None]) -> None:
        self.messages: list[Message] = []
        self.display_name = display_name
        self.participants: set[str] = set()

    def __str__(self):
        if self.display_name:
            return f"Thread: {self.display_name}"
        elif len(self.participants) == 2:
            for participant in self.participants:
                if participant != "Me":
                    return f"Thread: {participant}"
        return f"Thread: with {len(self.participants)} contacts"

    def __repr__(self) -> str:
        return str(self)


class Message:
    text: str
    date: datetime
    sender: str

    def __init__(self, text: str, date: datetime, sender: str) -> None:
        self.text = text
        self.date = date
        self.sender = sender

    def __repr__(self) -> str:
        return f"Message(sender={self.sender}, date={self.date}, text={self.text and self.text[:50]})"

    def __str__(self):
        return repr(self)


def apple_timestamp_to_datetime(apple_timestamp: int) -> datetime:
    apple_epoch = datetime(2001, 1, 1)
    unix_epoch = datetime(1970, 1, 1)
    epoch_offset = apple_epoch - unix_epoch
    unix_timestamp = (apple_timestamp / 1e9) + epoch_offset.total_seconds()
    return datetime.utcfromtimestamp(unix_timestamp)


def read_imessages(db_path) -> dict:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT 
        chat.chat_identifier,
        chat.display_name,
        message.text,
        message.date,
        message.is_from_me,
        message.attributedBody,
        handle.id
    FROM 
        chat 
        JOIN chat_message_join ON chat.ROWID = chat_message_join.chat_id
        JOIN message ON chat_message_join.message_id = message.ROWID
        LEFT JOIN handle ON message.handle_id = handle.ROWID
    """

    cursor.execute(query)

    chats: dict[str, Thread] = {}

    for row in cursor.fetchall():
        chat_id, display_name, text, date, is_from_me, attributedBody, sender = row
        if chat_id not in chats:
            chats[chat_id] = Thread(display_name or None)

        # Identify the sender
        sender_info = "Me" if is_from_me else sender

        # Ensure the text field is captured correctly
        if text is None and attributedBody:
            decoded = typedstream.unarchive_from_data(attributedBody)
            try:
                text = decoded.contents[0].value.value
            except Exception as e:
                print("failed")
                print(decoded)
                raise e

        chats[chat_id].messages.append(
            Message(text, apple_timestamp_to_datetime(date), sender_info)
        )

        chats[chat_id].participants.add(sender_info)

    cursor.close()
    conn.close()

    # sort all the messages by time
    for chat_id in chats:
        chats[chat_id].messages = sorted(chats[chat_id].messages, key=lambda e: e.date)

    return chats
