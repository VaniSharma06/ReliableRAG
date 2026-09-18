from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from evaluation.evaluator import evaluate_response
from evaluation.dataset import EVALUATION_DATASET

from app.ingestion import load_pdf, chunk_text
from app.vector_store import VectorStore
from app.llm import generate_answer


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="ReliableRAG",
    description=(
        "Evaluation-Driven Retrieval-Augmented "
        "Generation System"
    ),
    version="1.0.0"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class QueryRequest(BaseModel):
    question: str


# ============================================================
# VECTOR STORE
# ============================================================

vector_store = VectorStore()


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "project": "ReliableRAG",
        "status": "running",
        "description": (
            "Evaluation-Driven "
            "Retrieval-Augmented Generation"
        )
    }


# ============================================================
# PDF UPLOAD
# ============================================================

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename:
        return {
            "success": False,
            "message": "No file provided."
        }

    if not file.filename.lower().endswith(".pdf"):
        return {
            "success": False,
            "message": "Only PDF files are supported."
        }

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(
        file_path,
        "wb"
    ) as output_file:

        output_file.write(contents)

    text = load_pdf(
        str(file_path)
    )

    chunks = chunk_text(text)

    if not chunks:

        return {
            "success": False,
            "message": (
                "No readable text was found in the PDF."
            )
        }

    vector_store.add_documents(chunks)

    return {
        "success": True,
        "filename": file.filename,
        "chunks_indexed": len(chunks),
        "message": "Document indexed successfully."
    }


# ============================================================
# QUERY
# ============================================================

@app.post("/query")
def query(request: QueryRequest):
    results = vector_store.search(request.question, top_k=3)

    documents = results["documents"][0]
    context = "\n\n".join(documents)

    answer = generate_answer(
        request.question,
        context
    )

    # Find matching evaluation question
    expected_keywords = []

    for item in EVALUATION_DATASET:
        if item["question"].strip().lower() == request.question.strip().lower():
            expected_keywords = item["expected_keywords"]
            break

    evaluation = evaluate_response(
        question=request.question,
        answer=answer,
        retrieved_chunks=documents,
        expected_keywords=expected_keywords
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": documents,
        "evaluation": evaluation
    }