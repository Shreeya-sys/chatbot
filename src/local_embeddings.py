import hashlib
import math
import re


TOKEN_RE = re.compile(r"[a-z0-9]+")


class LocalHashEmbeddingFunction:
    """Small offline embedding function for demos when no HF model is cached."""

    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions

    @staticmethod
    def name() -> str:
        return "local_hash_embedding"

    @staticmethod
    def default_space() -> str:
        return "cosine"

    def __call__(self, input):
        return [self._embed(text) for text in input]

    def embed_query(self, input):
        return self(input)

    def embed_documents(self, input):
        return self(input)

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = TOKEN_RE.findall(text.lower())
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "little") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]
