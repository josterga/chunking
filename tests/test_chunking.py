from main.chunking_embedder import ChunkingEmbedder

def test_chunking_strategy(strategy, text, min_chunks=1):
    ce = ChunkingEmbedder(chunk_method=strategy, max_tokens=10)
    chunks = ce.chunk(text, source_id="test")
    assert isinstance(chunks, list), f"{strategy}: Output is not a list"
    assert len(chunks) >= min_chunks, f"{strategy}: Not enough chunks ({len(chunks)})"
    for c in chunks:
        assert hasattr(c, "chunk_text"), f"{strategy}: Chunk missing 'chunk_text'"
        assert c.chunk_text.strip(), f"{strategy}: Empty chunk text"
    print(f"{strategy.capitalize()} chunking test passed.")

def run_all_tests():
    text = (
        "Header 1\n"
        "# Section 1\n"
        "This is the first paragraph. It has two sentences.\n"
        "This is the second paragraph.\n"
        "## Subsection\n"
        "Another line.\n"
    )
    test_chunking_strategy("sentence", text, min_chunks=2)
    test_chunking_strategy("line", text, min_chunks=2)
    test_chunking_strategy("paragraph", text, min_chunks=1)
    test_chunking_strategy("header", text, min_chunks=1)
    # For custom, you would need to define a custom_chunk_fn and pass it to ChunkingEmbedder

    # Edge case: empty input
    ce = ChunkingEmbedder(chunk_method="sentence", max_tokens=10)
    empty_chunks = ce.chunk("", source_id="test")
    assert empty_chunks == [], "Empty input should return empty list"
    print("Empty input test passed.")

if __name__ == "__main__":
    run_all_tests()