from pathlib import Path
from app.ingestion import load_pdf, chunk_text

BASE_DIR = Path(__file__).resolve().parent.parent
pdf_path = BASE_DIR / "data" / "test_document.pdf"

print("Looking for PDF at:")
print(pdf_path)

text = load_pdf(str(pdf_path))

print("\n===== EXTRACTED TEXT =====\n")
print(text)

chunks = chunk_text(text)

print("\n===== CHUNKS =====")
print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)