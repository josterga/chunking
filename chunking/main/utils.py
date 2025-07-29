import tiktoken
from typing import Callable

def get_default_tokenizer(model_name: str = "text-embedding-3-small"):
    try:
        enc = tiktoken.encoding_for_model(model_name)
    except Exception:
        enc = tiktoken.encoding_for_model("text-embedding-3-small")
    return enc.encode