import chromadb

from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_DIMENSIONS, TOP_K
from src.local_embeddings import LocalHashEmbeddingFunction


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    embedder = LocalHashEmbeddingFunction(dimensions=EMBEDDING_DIMENSIONS)
    return client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embedder)


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    collection = get_collection()
    if collection.count() == 0:
        return []
    result = collection.query(query_texts=[query], n_results=min(top_k, collection.count()))
    chunks = []
    for text, metadata, distance in zip(
        result.get("documents", [[]])[0],
        result.get("metadatas", [[]])[0],
        result.get("distances", [[]])[0],
    ):
        chunks.append({"text": text, "metadata": metadata or {}, "distance": distance})
    return chunks
