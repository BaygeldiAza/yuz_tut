import chromadb
from sentence_transformers import SentenceTransformer

from ai.config import CHROMA_PATH, CHROMA_COLLECTION, EMBEDDING_MODEL, QUERY_PREFIX


class LocationSearch:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.client.get_collection(CHROMA_COLLECTION)

    def query(self, query_text: str, top_n: int, category: str | None = None) -> list[dict]:
        embedding = self.model.encode(QUERY_PREFIX + query_text).tolist()

        where = {"categories": category} if category else None

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_n,
            where=where,
        )

        return self._format_results(results)

    @staticmethod
    def _format_results(results: dict) -> list[dict]:
        formatted = []
        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for i in range(len(ids)):
            formatted.append({
                "id": ids[i],
                "embedding_text": documents[i],
                "metadata": metadatas[i],
                "score": 1 - distances[i],
            })

        return formatted
