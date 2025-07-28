import os
import argparse
import yaml
from dotenv import load_dotenv

from main.chunking_embedder import ChunkingEmbedder
from embeddings.openai_embedder import openai_embed_fn
from embeddings.huggingface_embedder import huggingface_embed_fn, hf_tokenizer

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Chunk and embed text files.")
    parser.add_argument("--input", type=str, required=True, help="Path to input text/markdown file")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to YAML config file")
    parser.add_argument("--output", type=str, default=None, help="Optional: path to save output JSON")
    args = parser.parse_args()

    config = load_config(args.config)
    chunk_cfg = config.get("chunking", {})
    embed_cfg = config.get("embedding", {})

    # Load data
    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    # Select embedding function and tokenizer
    provider = embed_cfg.get("provider", "openai")
    if provider == "openai":
        embed_fn = openai_embed_fn
        tokenizer = None  # Use default tiktoken
        model_name = embed_cfg.get("openai_model", "text-embedding-3-small")
    elif provider == "huggingface":
        embed_fn = huggingface_embed_fn
        tokenizer = hf_tokenizer
        model_name = embed_cfg.get("huggingface_model", "sentence-transformers/all-MiniLM-L6-v2")
    else:
        raise ValueError("Unknown embedding provider")

    ce = ChunkingEmbedder(
        chunk_method=chunk_cfg.get("method", "sentence"),
        max_tokens=chunk_cfg.get("max_tokens", 100),
        overlap_tokens=chunk_cfg.get("overlap_tokens", 10),
        inject_headers=chunk_cfg.get("inject_headers", True),
        tokenizer=tokenizer
    )

    chunks = ce.chunk(text, source_id=os.path.basename(args.input))
    results = ce.embed_chunks(chunks, embed_fn, embed_metadata={"model": model_name})

    # Output
    import json
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {args.output}")
    else:
        for r in results:
            print(r)

if __name__ == "__main__":
    main()