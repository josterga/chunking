from main.base import ChunkMetadata
from main.strategies.paragraph import chunk_paragraphs

def chunk_headers(text, source_id, tokenizer, max_tokens, inject_headers, find_headers, get_nearest_header, overlap_fn):
    headers = find_headers(text)
    if not headers:
        return chunk_paragraphs(text, source_id, tokenizer, max_tokens, inject_headers, find_headers, get_nearest_header, overlap_fn)
    chunks = []
    chunk_id = 0
    for i, header in enumerate(headers):
        start = header["start"]
        end = headers[i+1]["start"] if i+1 < len(headers) else len(text)
        section = text[start:end].strip()
        section_tokens = len(tokenizer(section))
        if section_tokens > max_tokens:
            subchunks = chunk_paragraphs(section, source_id, tokenizer, max_tokens, inject_headers, find_headers, get_nearest_header, overlap_fn)
            for sub in subchunks:
                sub.chunk_id = chunk_id
                sub.chunking_method = "header"
                sub.header = header["header"]
                chunks.append(sub)
                chunk_id += 1
        else:
            chunks.append(ChunkMetadata(
                chunk_id, source_id, "header", header["header"], start, end, section_tokens, section
            ))
            chunk_id += 1
    return overlap_fn(chunks)