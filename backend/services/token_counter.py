def count_tokens(text: str, model: str = 'gpt-3.5-turbo') -> int:
    """
    Return an approximate token count for text.
    Uses tiktoken when available because it gives a close-enough estimate
    even for non-OpenAI providers such as Gemini/Groq.
    If tiktoken is unavailable or errors, falls back to the rough heuristic
    `len(text) // 4`.
    """
    try:
        import tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception:
        return len(text) // 4