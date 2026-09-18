# ReliableRAG

### Evaluation-Driven Retrieval-Augmented Generation System

ReliableRAG is a locally deployable Retrieval-Augmented Generation (RAG) system designed to combine semantic document retrieval with large-language-model generation while measuring retrieval quality, contextual relevance, faithfulness, answer correctness, and response latency.

The system transforms unstructured PDF documents into searchable vector representations, retrieves relevant evidence for a user query, and generates grounded responses using a locally hosted LLM.

---

## Overview

Traditional LLM applications can generate fluent answers without having access to domain-specific documents.

ReliableRAG addresses this limitation by introducing a retrieval layer between the user query and the language model:

```text
User Query
    │
    ▼
Query Embedding
    │
    ▼
Semantic Retrieval
    │
    ▼
Relevant Document Chunks
    │
    ▼
Context Construction
    │
    ▼
Local LLM — Llama 3.2
    │
    ▼
Grounded Answer
    │
    ▼
Evaluation Pipeline



Key Features


PDF document ingestion and text extraction
Configurable text chunking with overlap
Semantic embeddings using Sentence Transformers
Persistent vector storage with ChromaDB
Top-k semantic document retrieval
Local LLM inference using Ollama and Llama 3.2
Context-grounded response generation
Retrieved evidence/source display
Automated evaluation benchmark
Retrieval quality measurement
Context relevance measurement
Faithfulness measurement
Answer correctness measurement
Response latency measurement
Interactive Streamlit interface
FastAPI backend architecture

System Architecture

                         ┌─────────────────────┐
                         │      PDF Input      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Text Extraction   │
                         │       PyPDF         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Text Chunking      │
                         │  Size + Overlap     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Embeddings      │
                         │ all-MiniLM-L6-v2    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     ChromaDB        │
                         │   Vector Storage    │
                         └──────────┬──────────┘
                                    │
                         User Query │
                                    ▼
                         ┌─────────────────────┐
                         │ Semantic Retrieval  │
                         │       Top-K          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Context Construction│
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Ollama / Llama 3.2  │
                         │    Local Inference  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Grounded Response   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Evaluation Pipeline │
                         └─────────────────────┘
Technology Stack

Layer	Technology
Language	Python 3.11
Backend	FastAPI
Frontend	Streamlit
Document Processing	PyPDF
Embeddings	Sentence Transformers
Vector Database	ChromaDB
LLM Runtime	Ollama
LLM	Llama 3.2
Data Validation	Pydantic
Testing	Python tests
Evaluation	Custom evaluation pipeline

How It Works

1. Document Ingestion

PDF files are uploaded through the application.

The ingestion pipeline extracts readable text using PyPDF.

2. Text Chunking

Extracted text is divided into overlapping chunks.

The overlap helps preserve contextual continuity between neighboring chunks.

3. Semantic Embeddings

Each chunk is converted into a vector representation using:

all-MiniLM-L6-v2

These embeddings allow the system to retrieve semantically related content rather than relying only on exact keyword matches.

4. Vector Storage

Embeddings and their corresponding document chunks are stored in ChromaDB.

5. Retrieval

When a user submits a question, the query is embedded and compared against stored document vectors.

The system retrieves the top relevant chunks.

6. Context-Grounded Generation

The retrieved chunks are supplied to Llama 3.2 through Ollama.

The generation prompt instructs the model to use the provided document context and avoid unsupported answers.

7. Evaluation

The evaluation pipeline runs predefined benchmark questions and records:

Retrieval Score
Context Relevance
Faithfulness
Answer Correctness
Response Latency

Results are stored as structured JSON for reproducibility.

Evaluation Framework

ReliableRAG includes a lightweight automated evaluation framework.

Metrics
Metric	Purpose
Retrieval Score	Measures whether expected information appears in retrieved context
Context Relevance	Measures lexical overlap between query terms and retrieved context
Faithfulness	Estimates how much generated-answer vocabulary is supported by retrieved context
Answer Correctness	Measures presence of expected benchmark keywords in the generated answer
Latency	Measures end-to-end retrieval and generation time

Note: The current evaluation implementation uses lightweight lexical metrics. It is intended as a reproducible project benchmark rather than a research-grade semantic evaluation framework.

Project Structure
ReliableRAG/
│
├── app/
│   ├── ingestion.py
│   ├── llm.py
│   ├── vector_store.py
│   ├── test_ingestion.py
│   └── test_vector_store.py
│
├── data/
│   └── test_document.pdf
│
├── evaluation/
│   ├── dataset.py
│   ├── evaluator.py
│   ├── run_evaluation.py
│   └── results/
│       └── evaluation_results.json
│
├── tests/
│
├── frontend.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
Installation
1. Clone the repository
git clone https://github.com/VaniSharma06/ReliableRAG.git
cd ReliableRAG
2. Create a virtual environment
python -m venv .venv
3. Activate the environment

Windows PowerShell:

.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Install Ollama

Install Ollama and make sure the required model is available:

ollama pull llama3.2:3b
Running the Application
Start the FastAPI backend
uvicorn main:app --reload

The API will be available locally at:

http://127.0.0.1:8000
Start the Streamlit frontend

Open another terminal:

streamlit run frontend.py

The interactive application will open in your browser.

Running the Evaluation

From the project root:

python -m evaluation.run_evaluation

The benchmark results are saved to:

evaluation/results/evaluation_results.json
Example Evaluation Questions

The included benchmark evaluates questions such as:

What is ReliableRAG?

What does Retrieval-Augmented Generation combine?

What happens before an answer is generated?

What evaluation metrics can ReliableRAG use?
Engineering Highlights
Local-first LLM Architecture

The project uses Ollama for local LLM inference, avoiding dependency on a paid hosted inference API for the core generation pipeline.

Retrieval-Grounded Generation

Instead of directly prompting an LLM with a question, ReliableRAG first retrieves relevant evidence and incorporates it into the generation context.

Reproducible Evaluation

Benchmark questions and expected keywords are maintained as structured evaluation data, allowing the system to be evaluated repeatedly after implementation changes.

Separation of Concerns

The project separates:

ingestion
vector storage
generation
evaluation
API
frontend

This makes individual components easier to test and modify.

Current Limitations
Current evaluation metrics are primarily lexical rather than semantic.
PDF extraction quality depends on the document structure.
The local Llama 3.2 model has smaller capacity than larger hosted models.
Retrieval quality depends on chunking and embedding configuration.
The current prototype is optimized for local experimentation rather than distributed production deployment.
Future Improvements

Potential extensions include:

Hybrid keyword + vector retrieval
Reranking models
Semantic evaluation metrics
Automated hallucination detection
Citation-aware generation
Document metadata filtering
Multi-document retrieval
Retrieval caching
Experiment tracking
Production deployment
Automated CI/CD evaluation
Author

Vani Sharma

Computer Science & Engineering

GitHub:
https://github.com/VaniSharma06
