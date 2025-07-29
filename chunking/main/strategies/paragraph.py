from chunking.main.base import ChunkMetadata

def chunk_paragraphs(text, source_id, tokenizer, max_tokens, inject_headers, find_headers, get_nearest_header, overlap_fn):
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    headers = find_headers(text) if inject_headers else []
    chunks = []
    buf, buf_tokens, start_char, chunk_id = "", 0, 0, 0
    for para in paragraphs:
        para_tokens = len(tokenizer(para))
        if buf_tokens + para_tokens > max_tokens:
            end_char = start_char + len(buf)
            header = get_nearest_header(headers, start_char) if inject_headers else None
            chunks.append(ChunkMetadata(
                chunk_id, source_id, "paragraph", header, start_char, end_char, buf_tokens, buf.strip()
            ))
            chunk_id += 1
            buf, buf_tokens, start_char = "", 0, end_char
        if not buf and inject_headers and headers:
            header = get_nearest_header(headers, start_char)
            if header:
                hint = header[:80]
                buf += f"{hint}\n\n"
                buf_tokens += len(tokenizer(hint))
        buf += (" " if buf else "") + para
        buf_tokens += para_tokens
    if buf.strip():
        end_char = start_char + len(buf)
        header = get_nearest_header(headers, start_char) if inject_headers else None
        chunks.append(ChunkMetadata(
            chunk_id, source_id, "paragraph", header, start_char, end_char, buf_tokens, buf.strip()
        ))
    return overlap_fn(chunks)