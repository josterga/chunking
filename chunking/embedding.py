# chunking/embedding.py

import os
from dotenv import load_dotenv

from chunking.embeddings.openai_embedder import openai_embed_fn
from chunking.embeddings.huggingface_embedder import huggingface_embed_fn
from chunking.embeddings.ollama_embedder import ollama_embed_fn
from chunking.embeddings.voyage_embedder import voyage_embed_fn

def get_embedding(text, provider="openai", model_name=None, host=None):
    load_dotenv()
    if provider == "openai":
        return openai_embed_fn([text])[0]
    elif provider == "huggingface":
        return huggingface_embed_fn([text])[0]
    elif provider == "voyage":
        return voyage_embed_fn([text], model=model_name)[0]
    elif provider == "ollama":
        if model_name:
            os.environ["OLLAMA_MODEL"] = model_name
        if host:
            os.environ["OLLAMA_HOST"] = host
        return ollama_embed_fn([text])[0]
    else:
        raise ValueError(f"Unknown embedding provider: {provider}")