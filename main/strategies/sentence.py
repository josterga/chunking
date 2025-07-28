from main.base import ChunkMetadata
from nltk.tokenize import sent_tokenize

def chunk_sentences(text, source_id, tokenizer, max_tokens, inject_headers, find_headers, get_nearest_header, overlap_fn):
    sentences = sent_tokenize(text)
    headers = find_headers(text) if inject_headers else []
    chunks = []
    char_idx = 0
    buf, buf_tokens, start_char, chunk_id = "", 0, 0, 0
    for sent in sentences:
        sent_tokens = len(tokenizer(sent))
        if buf_tokens + sent_tokens > max_tokens:
            end_char = start_char + len(buf)
            header = get_nearest_header(headers, start_char) if inject_headers else None
            chunks.append(ChunkMetadata(
                chunk_id, source_id, "sentence", header, start_char, end_char, buf_tokens, buf.strip()
            ))
            chunk_id += 1
            buf, buf_tokens, start_char = "", 0, char_idx
        if not buf and inject_headers and headers:
            header = get_nearest_header(headers, char_idx)
            if header:
                hint = header[:80]
                buf += f"{hint}\n\n"
                buf_tokens += len(tokenizer(hint))
        buf += (" " if buf else "") + sent
        buf_tokens += sent_tokens
        char_idx += len(sent) + 1
    if buf.strip():
        end_char = start_char + len(buf)
        header = get_nearest_header(headers, start_char) if inject_headers else None
        chunks.append(ChunkMetadata(
            chunk_id, source_id, "sentence", header, start_char, end_char, buf_tokens, buf.strip()
        ))
    return overlap_fn(chunks)