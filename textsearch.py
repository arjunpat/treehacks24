from llama_index import SimpleDirectoryReader, StorageContext, ServiceContext, Document
from llama_index.indices.vector_store import VectorStoreIndex
from llama_iris import IRISVectorStore

import getpass
import os
from dotenv import load_dotenv

load_dotenv(override=True)

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

username = 'SUPERUSER'
password = 'SYS2' # Replace password with password you set
hostname = 'localhost' 
port = '1972' 
namespace = 'USER'
CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"

# semantics searcher
class TextSearcher:
    def __init__(self):
        self.documents = []
    
    # load a chat from a person into the vector database
    def load(self, chat, name):
        for message in chat:
            doc = Document(text=message, metadata={"name": name} or {})
            self.documents.append(doc)


    def search(self, query):
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
            self.documents, 
            storage_context=storage_context, 
            show_progress=True, 
            # service_context=service_context,
        )
        query_engine = index.as_query_engine()

        response = query_engine.query(query)
        print(str(response))
        return str(response)