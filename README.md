# Modular Chunking and Embedding Framework

- Supports line, sentence, paragraph, header/section, and custom chunking.
- Pluggable embedding models (OpenAI, HuggingFace, custom).
- Uses `.env` for API keys and model config.
- See `scripts/` for usage examples.

5. End Results
Output: A list of chunk dictionaries, each with text, metadata, and embedding.
Usage: Can be saved as JSON, indexed for search, or used in RAG pipelines.



     1. Chunking Options
All chunking options are set under the chunking: section in config.yaml.
Available Chunking Strategies
Strategy	Description	Use Case Example
sentence	Splits text into sentences, then groups into chunks up to max_tokens.	Most common for natural language text.
line	Splits text by lines, then groups into chunks up to max_tokens.	Code, logs, or line-oriented data.
paragraph	Splits text by paragraphs (double newlines), then groups into chunks up to max_tokens.	Articles, documentation, prose.
header	Splits text at headers (e.g., Markdown #), grouping under each header up to max_tokens.	Structured docs, Markdown, outlines.
custom	Use your own chunking function (see advanced usage).	Special formats, custom logic.
Chunking Parameters
Key	Type	Default	Description
method	string	sentence	Which chunking strategy to use (sentence, line, paragraph, header, custom).
max_tokens	int	100	Maximum tokens per chunk. Chunks will not exceed this size.
overlap_tokens	int	10	Number of tokens to overlap between consecutive chunks (for context preservation).
inject_headers	bool	true	If true, prepends header text to each chunk (for header strategy, or if headers detected).


Available Embedding Providers
Provider	Description	Model Example	Notes
openai	Uses OpenAI’s API for embeddings.	text-embedding-3-small	Requires API key.
huggingface	Uses HuggingFace Transformers locally.	sentence-transformers/all-MiniLM-L6-v2	Requires local model files.
ollama	(Planned) Local LLMs via Ollama.	mxbai-embed-large	Not yet supported.


1. Sign up at [Voyage AI](https://www.voyageai.com/) and get your API key.
2. Set your API key in your environment:
   ```
   export VOYAGE_API_KEY=sk-...
   ```
3. In `config.yaml`:
   ```yaml
   embedding:
     provider: voyage
     model: voyage-context-3
   ```
4. Run your pipeline as usual. The first 200 million tokens are free!



python -m scripts.run_chunking --input 'input/GTM AI Email Thread.md' --config config.yaml --output results.json
