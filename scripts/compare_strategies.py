from main.chunking_embedder import ChunkingEmbedder
from embeddings.openai_embedder import openai_embed_fn

text = "## Header\nSome text. More text.\n\n## Another Header\nEven more text."

for method in ["line", "sentence", "paragraph", "header"]:
    ce = ChunkingEmbedder(chunk_method=method, max_tokens=20, overlap_tokens=5, inject_headers=True)
    chunks = ce.chunk(text, source_id="doc1")
    results = ce.embed_chunks(chunks, openai_embed_fn, embed_metadata={"model": "text-embedding-3-small"})
    print(f"--- {method} ---")
    for r in results:
        print(r)