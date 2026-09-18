from ingestion import load_pdf, chunk_text
from vector_store import VectorStore


pdf_path = "../data/test_document.pdf"

text = load_pdf(pdf_path)
chunks = chunk_text(text)

print(f"Loaded {len(chunks)} chunks.")

store = VectorStore()

store.add_documents(chunks)

print("Documents added to vector database.")

query = "What is Retrieval-Augmented Generation?"

results = store.search(query, top_k=3)

print("\n===== SEARCH RESULTS =====")

for document in results["documents"][0]:
    print("\n---")
    print(document)