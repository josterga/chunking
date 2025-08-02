# `chunking` — Flexible Text Chunking & Embedding

- **Description:**  
  Config-driven library for splitting text into chunks and embedding them using various providers (OpenAI, HuggingFace, Ollama, Voyage, etc).
- **Entrypoint:**  
  `from chunking.pipeline import run_chunking`
- **Configurable Arguments:**
  - `input_path`: Path to input text file.
  - `config_path`: YAML config file for chunking/embedding.
  - `output_path`: Where to save results (optional).
  - `provider`: Embedding provider (`openai`, `huggingface`, `ollama`, `voyage`).
  - `model_name`: Model to use for embedding.
  - `host`: Custom host for embedding API.
  - `chunk_method`: Chunking strategy (`sentence`, `paragraph`, `line`, `header`, or custom).
  - `max_tokens`: Max tokens per chunk.
  - `overlap_tokens`: Overlap between chunks.
  - `inject_headers`: Whether to inject headers into chunks.
  - `header_regex`: Regex for header detection.
  - `tokenizer`: Custom tokenizer (optional).
  - `custom_chunk_fn`: Custom chunking function (optional).
  - `raw_text`: Provide text directly instead of file.

- **Example:**
  ```python
  from chunking.pipeline import run_chunking
  results = run_chunking(
      input_path="input/GTM AI Email Thread.md",
      config_path="config.yaml",
      provider="ollama",
      model_name="mxbai-embed-large:latest",
      host="http://localhost:11434"
  )
  ```