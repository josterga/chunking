import os
import argparse
import yaml
from dotenv import load_dotenv

from main.chunking_embedder import ChunkingEmbedder
from embeddings.openai_embedder import openai_embed_fn
from embeddings.huggingface_embedder import huggingface_embed_fn, hf_tokenizer
from embeddings.ollama_embedder import ollama_embed_fn, ollama_tokenizer
from embeddings.voyage_embedder import voyage_embed_fn, voyage_tokenizer


def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def run_chunking(input_path, config_path, output_path=None, provider=None, model_name=None, host=None):
    load_dotenv()
    config = load_config(config_path)
    chunk_cfg = config.get("chunking", {})
    embed_cfg = config.get("embedding", {})

    # Allow override from function arguments
    if provider:
        embed_cfg["provider"] = provider
    if model_name:
        embed_cfg["model"] = model_name
    if host:
        embed_cfg["host"] = host

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    provider = embed_cfg.get("provider", "openai")
    model_name = embed_cfg.get("model")

    # --- Add this block ---
    if provider == "openai":
        embed_fn = openai_embed_fn
        tokenizer = None  # Use default tiktoken
    elif provider == "huggingface":
        embed_fn = huggingface_embed_fn
        tokenizer = hf_tokenizer
    elif provider == "voyage":
        embed_fn = lambda texts: voyage_embed_fn(texts, model=model_name)
        tokenizer = voyage_tokenizer
    elif provider == "ollama":
        embed_fn = ollama_embed_fn
        tokenizer = ollama_tokenizer
        if model_name:
            os.environ["OLLAMA_MODEL"] = model_name
        if embed_cfg.get("host"):
            os.environ["OLLAMA_HOST"] = embed_cfg["host"]
    else:
        raise ValueError("Unknown embedding provider")
    # --- End block ---

    ce = ChunkingEmbedder(
        chunk_method=chunk_cfg.get("method", "sentence"),
        max_tokens=chunk_cfg.get("max_tokens", 100),
        overlap_tokens=chunk_cfg.get("overlap_tokens", 10),
        inject_headers=chunk_cfg.get("inject_headers", True),
        tokenizer=tokenizer
    )
    chunks = ce.chunk(text, source_id=os.path.basename(input_path))
    results = ce.embed_chunks(chunks, embed_fn, embed_metadata={"model": model_name})

    if output_path:
        import json
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")
    return results

def main():
    parser = argparse.ArgumentParser(description="Chunk and embed text files.")
    parser.add_argument("--input", type=str, required=True, help="Path to input text/markdown file")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to YAML config file")
    parser.add_argument("--output", type=str, default=None, help="Optional: path to save output JSON")
    args = parser.parse_args()
    run_chunking(args.input, args.config, args.output)

if __name__ == "__main__":
    main()