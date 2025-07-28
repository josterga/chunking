import yaml
from main.chunking_embedder import ChunkingEmbedder
from main.utils import get_default_tokenizer
from embeddings.openai_embedder import openai_embed_fn

# Load model from config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
embed_cfg = config.get("embedding", {})
model_name = embed_cfg.get("model", "text-embedding-3-small")

tokenizer = get_default_tokenizer(model_name)

text = "## Header\nSome text. More text.\n\n## Another Header\nEven more text."

for method in ["line", "sentence", "paragraph", "header"]:
    ce = ChunkingEmbedder(
        chunk_method=method,
        max_tokens=20,
        overlap_tokens=5,
        inject_headers=True,
        tokenizer=tokenizer,
        model_name=model_name,
    )
    chunks = ce.chunk(text, source_id="doc1")
    results = ce.embed_chunks(chunks, openai_embed_fn, embed_metadata={"model": model_name})
    print(f"--- {method} ---")
    for r in results:
        print(r)