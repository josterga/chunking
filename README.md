# Modular Chunking and Embedding Framework

- Supports line, sentence, paragraph, header/section, and custom chunking.
- Pluggable embedding models (OpenAI, HuggingFace, custom).
- Uses `.env` for API keys and model config.
- See `scripts/` for usage examples.

## Using Ollama for Embeddings

1. Install and run Ollama: https://ollama.com/
2. Pull an embedding model, e.g.:
   ollama pull nomic-embed-text
3. Set your config.yaml:
   embedding:
     provider: ollama
     model: nomic-embed-text
     host: http://localhost:11434