import chromadb
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="./data/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="reliablerag_documents"
        )

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def add_documents(self, chunks: list[str]):
        if not chunks:
            return

        embeddings = self.embedding_model.encode(
            chunks
        ).tolist()

        ids = [
            f"chunk_{i}"
            for i in range(len(chunks))
        ]

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings
        )

    def search(self, query: str, top_k: int = 3):
        query_embedding = self.embedding_model.encode(
            [query]
        ).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )

        return results