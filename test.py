import os
from chunking.pipeline import run_chunking  # Updated import

input_path = "input/GTM AI Email Thread.md"
config_path = "config.yaml"

providers = [
    {"provider": "openai", "model_name": "text-embedding-3-small", "host": None},
    {"provider": "voyage", "model_name": "voyage-3-large", "host": "https://api.voyageai.com/v1/embeddings"},
    {"provider": "ollama", "model_name": "mxbai-embed-large:latest", "host": "http://localhost:11434"},
]

chunking_strategies = [
    {"chunk_method": "sentence", "max_tokens": 100, "overlap_tokens": 10, "inject_headers": True},
    {"chunk_method": "paragraph", "max_tokens": 150, "overlap_tokens": 20, "inject_headers": False},
    {"chunk_method": "line", "max_tokens": 50, "overlap_tokens": 5, "inject_headers": True},
    # Add more strategies as needed
]

for p in providers:
    for strat in chunking_strategies:
        print(f"\n=== Running with provider: {p['provider']} and strategy: {strat['chunk_method']} ===")
        try:
            results = run_chunking(
                input_path=input_path,
                config_path=config_path,
                output_path=None,
                provider=p["provider"],
                model_name=p["model_name"],
                host=p["host"],
                chunk_method=strat["chunk_method"],
                max_tokens=strat["max_tokens"],
                overlap_tokens=strat["overlap_tokens"],
                inject_headers=strat["inject_headers"],
            )
            print(f"Provider {p['provider']} with {strat['chunk_method']} produced {len(results)} results.")
        except Exception as e:
            print(f"Provider {p['provider']} with {strat['chunk_method']} failed: {e}")