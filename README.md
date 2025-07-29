chunking

A flexible, config-driven Python library for text chunking and embedding strategies.
Designed for use in RAG (Retrieval-Augmented Generation) and other NLP pipelines.
Features
Multiple chunking strategies: sentence, paragraph, line, header, and custom.
Pluggable embedding providers: OpenAI, HuggingFace, Ollama, Voyage, and more.
Configurable via YAML and .env files.
Easy integration: Use as a library in your own projects or as a CLI tool.
Extensible and tested.


Usage

- as a library
from chunking.pipeline import run_chunking

results = run_chunking(
    input_path="input/GTM AI Email Thread.md",
    config_path="config.yaml",
    provider="ollama",
    model_name="mxbai-embed-large:latest",
    host="http://localhost:11434"
)
for chunk in results:
    print(chunk["text"], chunk["embedding"])


Configuration
YAML config: Controls chunking and embedding parameters.
.env file: For secrets and API keys (e.g., OpenAI, Ollama).

Extending
Add new chunking strategies:
Implement in chunking/main/strategies/ and register in ChunkingEmbedder.
Add new embedding providers:
Implement in chunking/embeddings/ and update the provider logic in pipeline.py.

Testing
Tests are in the tests/ directory.