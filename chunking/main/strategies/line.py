from chunking.main.base import ChunkMetadata

def chunk_lines(text, source_id, tokenizer, max_tokens, inject_headers, find_headers, get_nearest_header, overlap_fn):
    lines = text.splitlines()
    headers = find_headers(text) if inject_headers else []
    chunks = []
    buf, buf_tokens, start_char, chunk_id = "", 0, 0, 0
    for idx, line in enumerate(lines):
        line_tokens = len(tokenizer(line))
        if buf_tokens + line_tokens > max_tokens:
            end_char = start_char + len(buf)
            header = get_nearest_header(headers, start_char) if inject_headers else None
            chunks.append(ChunkMetadata(
                chunk_id, source_id, "line", header, start_char, end_char, buf_tokens, buf.strip()
            ))
            chunk_id += 1
            buf, buf_tokens, start_char = "", 0, end_char
        buf += (line + "\n")
        buf_tokens += line_tokens
    if buf.strip():
        end_char = start_char + len(buf)
        header = get_nearest_header(headers, start_char) if inject_headers else None
        chunks.append(ChunkMetadata(
            chunk_id, source_id, "line", header, start_char, end_char, buf_tokens, buf.strip()
        ))
    return overlap_fn(chunks)