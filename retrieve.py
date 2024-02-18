import getpass
import os

from dotenv import load_dotenv
from llama_index import Document, ServiceContext, SimpleDirectoryReader, StorageContext
from llama_index.indices.vector_store import VectorStoreIndex
from llama_iris import IRISVectorStore

load_dotenv(override=True)

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

import os

from contacts import get_contacts
from messages import read_imessages

username = "SUPERUSER"
password = "SYS2"  # Replace password with password you set
hostname = "localhost"
port = "1972"
namespace = "USER"
CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"

db_path = os.path.expanduser("~/Downloads/chat.db")
# contacts = get_contacts()
# chats = read_imessages(db_path)

documents = []

chats = {
    "a": [
        "hello there",
        "do you know when we're going",
        "sooooo excited for the beach",
    ],
    "b": [
        "hey just letting you know my party is tomorrow",
        "ayyy that's sick i'll see you at The Tower, gotta be a lot of fun",
        "yup yup see you at 9",
    ],
}

for k, v in chats.items():
    # text = "\n".join([msg.text for msg in v.messages])
    text = "\n".join(v)
    documents.append(Document(text=text))
print(documents)

vector_store = IRISVectorStore.from_params(
    connection_string=CONNECTION_STRING,
    table_name="texts",
    embed_dim=1536,  # openai embedding dimension
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
# service_context = ServiceContext.from_defaults(
#     embed_model=embed_model, llm=None
# )

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    show_progress=True,
    # service_context=service_context,
)
# index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

query_engine = index.as_query_engine()

response = query_engine.query("Where is the event occuring?")
print(response)
