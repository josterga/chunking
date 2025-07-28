import tiktoken
from typing import Callable

def get_default_tokenizer(model_name: str = "text-embedding-3-small") -> Callable[[str], list]:
    return tiktoken.encoding_for_model(model_name).encode