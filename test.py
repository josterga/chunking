import os
from scripts.run_chunking import run_chunking

input_path = "input/GTM AI Email Thread.md"
config_path = "config.yaml"

providers = [
    {"provider": "openai", "model_name": "text-embedding-3-small", "host": None},
    {"provider": "voyage", "model_name": "voyage-3-large", "host": "https://api.voyageai.com/v1/embeddings"},
    {"provider": "ollama", "model_name": "mxbai-embed-large:latest", "host": "http://localhost:11434"},
]

for p in providers:
    print(f"\n=== Running with provider: {p['provider']} ===")
    try:
        results = run_chunking(
            input_path=input_path,
            config_path=config_path,
            output_path=None,
            provider=p["provider"],
            model_name=p["model_name"],
            host=p["host"]
        )
        print(f"Provider {p['provider']} produced {len(results)} results.")
    except Exception as e:
        print(f"Provider {p['provider']} failed: {e}")