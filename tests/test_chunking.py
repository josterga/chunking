from main.chunking_embedder import ChunkingEmbedder

def test_sentence_chunking():
    ce = ChunkingEmbedder(chunk_method="sentence", max_tokens=10)
    text = "This is a sentence. This is another one."
    chunks = ce.chunk(text, source_id="test")
    assert len(chunks) > 0
    print("Sentence chunking test passed.")

if __name__ == "__main__":
    test_sentence_chunking()