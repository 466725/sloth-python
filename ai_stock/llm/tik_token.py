import tiktoken
from typing import List


class TokenUtils:
    """
    Utility class for working with tiktoken:
    - Load tokenizer for a model
    - Count tokens
    - Truncate safely
    - Split text into token-limited chunks
    """

    DEFAULT_ENCODING = "cl100k_base"

    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.encoding = self._load_encoding(model)

    @staticmethod
    def _load_encoding(model: str):
        try:
            return tiktoken.encoding_for_model(model)
        except KeyError:
            return tiktoken.get_encoding(TokenUtils.DEFAULT_ENCODING)

    def _encode(self, text: str) -> List[int]:
        if not text:
            return []
        return self.encoding.encode(text)

    def _decode(self, tokens: List[int]) -> str:
        if not tokens:
            return ""
        return self.encoding.decode(tokens)

    def count_tokens(self, text: str) -> int:
        """Return number of tokens in text."""
        return len(self._encode(text))

    def truncate_by_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to max token length."""
        if max_tokens <= 0:
            return ""

        tokens = self._encode(text)
        return self._decode(tokens[:max_tokens])

    def fits_in_limit(self, text: str, limit: int) -> bool:
        """Check if text fits within token limit."""
        return self.count_tokens(text) <= limit

    def split_by_token_limit(self, text: str, chunk_size: int) -> List[str]:
        """Split text into chunks by token size."""
        if chunk_size <= 0:
            return []

        tokens = self._encode(text)
        return [
            self._decode(tokens[i:i + chunk_size])
            for i in range(0, len(tokens), chunk_size)
        ]


# -----------------------
# Demo usage
# -----------------------
if __name__ == "__main__":
    token_utils = TokenUtils()

    text = "Hello world! This is a test sentence to demonstrate token utilities."

    print("Token count:")
    print(token_utils.count_tokens(text))

    print("\nTruncated (5 tokens):")
    print(token_utils.truncate_by_tokens(text, 5))

    print("\nFits in 10 tokens?")
    print(token_utils.fits_in_limit(text, 10))

    print("\nSplit into chunks of 5 tokens:")
    chunks = token_utils.split_by_token_limit(text, 5)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {chunk}")
