from dataclasses import dataclass
from typing import Optional

@dataclass
class ChunkMetadata:
    chunk_id: int
    source_id: str
    chunking_method: str
    header: Optional[str]
    start_char: int
    end_char: int
    token_count: int
    chunk_text: str