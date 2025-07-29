import os
import requests

VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")

def voyage_embed_fn(texts, model="voyage-3-large"):
    """
    Generate embeddings using the Voyage AI API.
    Args:
        texts (list of str): List of texts to embed.
        model (str): Voyage model name (default: "voyage-3-large").
    Returns:
        List of embedding vectors (list of list of floats).
    """
    if VOYAGE_API_KEY is None:
        raise ValueError("VOYAGE_API_KEY environment variable not set.")
    url = "https://api.voyageai.com/v1/embeddings"
    headers = {"Authorization": f"Bearer {VOYAGE_API_KEY}"}
    data = {"model": model, "input": texts}
    response = requests.post(url, json=data, headers=headers)
    if not response.ok:
        print("Voyage API error:", response.status_code, response.text)
    response.raise_for_status()
    return [item["embedding"] for item in response.json()["data"]]

def voyage_tokenizer(text):
    # Voyage API does not expose a tokenizer; use whitespace as a fallback.
    # For best results, use the same chunking as you would for OpenAI.
    return text.split()