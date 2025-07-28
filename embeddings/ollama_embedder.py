import os
import requests

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "nomic-embed-text")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def ollama_tokenizer(text):
    # Ollama does not provide a tokenizer endpoint; use a simple whitespace split as a placeholder.
    return text.split()

def ollama_embed_fn(texts):
    embeddings = []
    for text in texts:
        response = requests.post(
            f"{OLLAMA_HOST}/api/embeddings",
            json={"model": OLLAMA_MODEL, "prompt": text}
        )
        response.raise_for_status()
        embeddings.append(response.json()["embedding"])
    return embeddings