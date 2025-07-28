import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

def openai_embed_fn(texts):
    response = openai.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in response.data]