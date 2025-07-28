import re
from main.base import ChunkMetadata
from main.utils import get_default_tokenizer
from main.strategies.line import chunk_lines
from main.strategies.sentence import chunk_sentences
from main.strategies.paragraph import chunk_paragraphs
from main.strategies.header import chunk_headers
from main.strategies.custom import chunk_custom

class ChunkingEmbedder:
    def __init__(
        self,
        chunk_method: str = "sentence",
        max_tokens: int = 130,
        overlap_tokens: int = 20,
        inject_headers: bool = True,
        header_regex: str = r"^(#{1,6})\s+(.+?)\s*$",
        tokenizer=None,
        model_name: str = "text-embedding-3-small",
        custom_chunk_fn=None,
    ):
        self.chunk_method = chunk_method
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.inject_headers = inject_headers
        self.header_re = re.compile(header_regex, re.M)
        self.custom_chunk_fn = custom_chunk_fn
        self.model_name = model_name
        self.tokenizer = tokenizer if tokenizer else get_default_tokenizer(model_name)
        
    def _find_headers(self, text: str):
        return [
            {"start": m.start(), "level": len(m.group(1)), "header": m.group(2).strip()}
            for m in self.header_re.finditer(text)
        ]

    def _get_nearest_header(self, headers, char_idx):
        if not headers:
            return None
        for i in range(len(headers)-1, -1, -1):
            if headers[i]["start"] <= char_idx:
                return headers[i]["header"]
        return headers[0]["header"]

    def _apply_overlap(self, chunks):
        if self.overlap_tokens and len(chunks) > 1:
            overlapped_chunks = []
            for i, chunk in enumerate(chunks):
                text_tokens = self.tokenizer(chunk.chunk_text)
                if i > 0:
                    prev_chunk = overlapped_chunks[-1]
                    overlap = text_tokens[:self.overlap_tokens]
                    try:
                        import tiktoken
                        enc = tiktoken.encoding_for_model(self.model_name)
                        overlap_text = enc.decode(overlap)
                        prev_chunk.chunk_text += " " + overlap_text
                    except Exception:
                        pass
                overlapped_chunks.append(chunk)
            return overlapped_chunks
        return chunks

    def chunk(self, text: str, source_id: str = ""):
        if self.chunk_method == "line":
            return chunk_lines(text, source_id, self.tokenizer, self.max_tokens, self.inject_headers, self._find_headers, self._get_nearest_header, self._apply_overlap)
        elif self.chunk_method == "sentence":
            return chunk_sentences(text, source_id, self.tokenizer, self.max_tokens, self.inject_headers, self._find_headers, self._get_nearest_header, self._apply_overlap)
        elif self.chunk_method == "paragraph":
            return chunk_paragraphs(text, source_id, self.tokenizer, self.max_tokens, self.inject_headers, self._find_headers, self._get_nearest_header, self._apply_overlap)
        elif self.chunk_method == "header":
            return chunk_headers(text, source_id, self.tokenizer, self.max_tokens, self.inject_headers, self._find_headers, self._get_nearest_header, self._apply_overlap)
        elif self.chunk_method == "custom":
            return chunk_custom(text, source_id, self.custom_chunk_fn)
        else:
            raise ValueError(f"Unknown chunk_method: {self.chunk_method}")

    def embed_chunks(self, chunks, embed_fn, embed_metadata=None):
        texts = [c.chunk_text for c in chunks]
        embeddings = embed_fn(texts)
        results = []
        for c, emb in zip(chunks, embeddings):
            d = c.__dict__.copy()
            d["embedding"] = emb
            if embed_metadata:
                d.update(embed_metadata)
            results.append(d)
        return results