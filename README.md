# ReliableRAG

### Evaluation-Driven Retrieval-Augmented Generation System

ReliableRAG is a production-oriented Retrieval-Augmented Generation (RAG) system designed to answer questions from user-provided documents while measuring retrieval quality, context relevance, faithfulness, answer correctness, and response latency.

Instead of treating a RAG application as simply:

> PDF → LLM → Answer

ReliableRAG treats **evaluation as a first-class component of the architecture**.

The system combines semantic retrieval, persistent vector storage, local LLM inference, document-grounded generation, source transparency, and automated benchmarking into one end-to-end pipeline.

---

## Project Overview

Large Language Models can generate fluent answers but may produce information that is unsupported by the provided documents.

ReliableRAG addresses this problem by introducing an evaluation layer around the complete retrieval and generation pipeline.

### Core Pipeline

```text
                         RELIABLERAG ARCHITECTURE

 ┌─────────────────┐
 │   PDF Document  │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Text Extraction │
 │     PyPDF       │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │    Chunking     │
 │ 1000 / 200 chars│
 │     overlap     │
 └────────┬────────┘
          │
          ▼
 ┌──────────────────────────┐
 │ Semantic Embedding Model │
 │  all-MiniLM-L6-v2        │
 └────────────┬─────────────┘
              │
              ▼
 ┌──────────────────────────┐
 │       ChromaDB           │
 │ Persistent Vector Store  │
 └────────────┬─────────────┘
              │
              │
        User Question
              │
              ▼
 ┌──────────────────────────┐
 │ Semantic Retrieval       │
 │       Top-K = 3          │
 └────────────┬─────────────┘
              │
              ▼
 ┌──────────────────────────┐
 │ Retrieved Context        │
 └────────────┬─────────────┘
              │
              ▼
 ┌──────────────────────────┐
 │ Local LLM Inference      │
 │ Ollama / Llama 3.2 3B    │
 └────────────┬─────────────┘
              │
              ▼
 ┌──────────────────────────┐
 │ Grounded Answer          │
 │ + Retrieved Sources      │
 └────────────┬─────────────┘
              │
              ▼
 ┌─────────────────────────────────────┐
 │          Evaluation Layer           │
 │                                     │
 │ Retrieval Score                     │
 │ Context Relevance                   │
 │ Faithfulness                        │
 │ Answer Correctness                  │
 │ Response Latency                    │
 └─────────────────────────────────────┘

# ReliableRAG

### Evaluation-Driven Retrieval-Augmented Generation System

ReliableRAG is a production-oriented Retrieval-Augmented Generation (RAG) system designed to answer questions from user-provided documents while measuring retrieval quality, context relevance, faithfulness, answer correctness, and response latency.

Instead of treating a RAG application as simply:

> PDF → LLM → Answer

ReliableRAG treats **evaluation as a first-class component of the architecture**.

The system combines semantic retrieval, persistent vector storage, local LLM inference, document-grounded generation, source transparency, and automated benchmarking into one end-to-end pipeline.

---

## Project Overview

Large Language Models can generate fluent answers but may produce information that is unsupported by the provided documents.

ReliableRAG addresses this problem by introducing an evaluation layer around the complete retrieval and generation pipeline.

### Core Pipeline

```text
                         RELIABLERAG ARCHITECTURE

 ┌─────────────────┐
 │   PDF Document  │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Text Extraction │
 │     PyPDF       │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │    Chunking     │
 │ 1000 / 200 chars│
 │     overlap     │
 └────────┬────────┘
          │
          ▼
 ┌──────────────────────────┐
 │ Semantic Embedding Model │
 │  all-MiniLM-L6-v2        │
 └────────────┬─────────────┘
              │
              ▼
 ┌──────────────────────────┐
 │       ChromaDB           │
 │ Persistent Vector Store  │
 └────────────┬─────────────┘
              │
              │
        User Question
              │
              ▼
 ┌──────────────────────────┐
 │ Semantic Retrieval       │
 │       Top-K = 3          │
 └────────────┬─────────────┘
              │
              ▼
 ┌──────────────────────────┐
 │ Retrieved Context        │
 └────────────┬─────────────┘
              │
              ▼
 ┌──────────────────────────┐
 │ Local LLM Inference      │
 │ Ollama / Llama 3.2 3B    │
 └────────────┬─────────────┘
              │
              ▼
 ┌──────────────────────────┐
 │ Grounded Answer          │
 │ + Retrieved Sources      │
 └────────────┬─────────────┘
              │
              ▼
 ┌─────────────────────────────────────┐
 │          Evaluation Layer           │
 │                                     │
 │ Retrieval Score                     │
 │ Context Relevance                   │
 │ Faithfulness                        │
 │ Answer Correctness                  │
 │ Response Latency                    │
 └─────────────────────────────────────┘

Why ReliableRAG?

A basic RAG application can retrieve documents and generate an answer.

ReliableRAG goes one step further by asking:

Did the retriever find the relevant information?
Was the retrieved context relevant to the question?
Was the generated answer supported by the retrieved context?
Did the answer contain the expected information?
How long did the system take?
Can the system be benchmarked repeatedly?

This transforms the project from a simple chatbot into an evaluation-driven AI system.

Key Features
1. Document Ingestion

Supports PDF documents through:

PyPDF
Text extraction
Validation
Automatic chunk generation
2. Configurable Text Chunking

Documents are divided into overlapping chunks.

Current configuration:

Chunk size  = 1000 characters
Overlap     = 200 characters

The overlap helps preserve contextual continuity between neighboring chunks.

3. Semantic Retrieval

ReliableRAG uses:

Sentence Transformers
all-MiniLM-L6-v2

to convert document chunks and queries into vector representations.

This enables semantic similarity-based retrieval rather than relying only on exact keyword matching.

4. Persistent Vector Database

Retrieved document chunks are stored using:

ChromaDB

with persistent local storage.

This allows the application to reuse indexed documents without rebuilding the entire vector database every time.

5. Local LLM Inference

The project uses:

Ollama
Llama 3.2 3B

for local answer generation.

This design provides:

Local inference
No dependency on paid LLM APIs
Reduced external data exposure
Reproducible development environment
6. Grounded Answer Generation

The LLM receives the retrieved context together with the user's question.

The prompt explicitly instructs the model to:

Use ONLY the provided context.

If the information cannot be found, the system is instructed not to invent an answer.

7. Source Transparency

Every query returns the retrieved source chunks used to construct the answer.

This makes the retrieval process inspectable instead of treating the LLM output as a black box.

Evaluation Framework

One of the main engineering goals of ReliableRAG is to evaluate the system rather than simply demonstrate that it works.

The project contains a benchmark dataset and automated evaluation pipeline.

Current evaluation dimensions:

Metric	Purpose
Retrieval Score	Measures whether expected information was retrieved
Context Relevance	Measures lexical relevance between question and retrieved context
Faithfulness	Estimates how much of the answer is supported by retrieved context
Answer Correctness	Measures expected keyword coverage in generated answers
Response Latency	Measures end-to-end response generation time
Source Count	Number of retrieved chunks used for generation
Benchmark Dataset

The evaluation suite contains 4 benchmark questions covering:

System definition
RAG fundamentals
Retrieval workflow
Evaluation metrics

Example benchmark question:

What is ReliableRAG?

Expected concept:

ReliableRAG is an evaluation-driven retrieval augmented
generation system.
Actual Evaluation Results

The project includes an automatically generated evaluation report:

evaluation/results/evaluation_results.json

The benchmark was executed using:

python -m evaluation.run_evaluation

The evaluation pipeline records:

Retrieval Score
Context Relevance
Faithfulness
Answer Correctness
Response Latency

The results are displayed in the Streamlit dashboard under:

Quality Benchmark
Example Result Structure
{
  "question": "What is ReliableRAG?",
  "evaluation": {
    "retrieval_score": 1.0,
    "context_relevance": 0.75,
    "faithfulness": 0.89,
    "answer_correctness": 1.0,
    "source_count": 3
  }
}

The exact aggregate values are generated from the local benchmark run and are stored in evaluation/results/evaluation_results.json. This avoids hard-coding benchmark numbers into the documentation.

Engineering Decisions

ReliableRAG was designed around several deliberate engineering decisions.

Decision 1 — Local LLM Instead of Paid API
Chosen
Ollama + Llama 3.2 3B
Reason

The project should remain usable without requiring a paid API key or external inference service.

Result

The complete RAG pipeline can run locally.

Decision 2 — Semantic Retrieval Instead of Keyword Search
Chosen
Sentence Transformers
all-MiniLM-L6-v2
Reason

Questions and relevant passages may use different wording.

Semantic embeddings allow retrieval based on meaning rather than exact word matching.

Decision 3 — Persistent Vector Storage
Chosen
ChromaDB PersistentClient
Reason

The indexed representation should survive application restarts.

This also separates the ingestion/indexing stage from repeated query execution.

Decision 4 — Top-K Retrieval
Chosen
Top K = 3
Reason

Returning a small number of highly relevant chunks keeps the LLM context focused while limiting unnecessary context.

This parameter can be changed as part of future retrieval experiments.

Decision 5 — Evaluation as a Separate Module

Evaluation logic is isolated under:

evaluation/

rather than being tightly coupled to the API.

This makes it easier to:

Add new metrics
Run repeatable benchmarks
Compare system configurations
Track future improvements
System Architecture
                 ┌───────────────────────┐
                 │      Streamlit UI     │
                 └───────────┬───────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │   FastAPI API  │
                    └───────┬────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        Ingestion       Retrieval       Evaluation
             │              │              │
             ▼              ▼              ▼
          PyPDF         ChromaDB       Metrics Engine
             │              │              │
             ▼              ▼              │
        Chunking       Sentence           │
                         Transformer      │
                            │              │
                            ▼              │
                         Context          │
                            │              │
                            ▼              │
                     Ollama / Llama       │
                            │              │
                            ▼              │
                         Answer           │
                            │              │
                            └──────┬───────┘
                                   ▼
                           Benchmark Results
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
│   ├── test_document.pdf
│   └── uploads/
│
├── evaluation/
│   ├── dataset.py
│   ├── evaluator.py
│   ├── run_evaluation.py
│   └── results/
│       └── evaluation_results.json
│
├── main.py
├── frontend.py
├── requirements.txt
├── .gitignore
└── README.md
Technology Stack
Backend
Python 3.11
FastAPI
Pydantic
Uvicorn
AI / ML
Sentence Transformers
all-MiniLM-L6-v2
Ollama
Llama 3.2 3B
Retrieval
ChromaDB
Vector embeddings
Top-K semantic retrieval
Document Processing
PyPDF
Frontend
Streamlit
Evaluation
Python evaluation framework
Retrieval scoring
Context relevance
Faithfulness
Answer correctness
Response latency
API Design
Health / Root Endpoint
GET /

Returns system information and application status.

Upload Document
POST /upload

Accepts:

PDF

Processing flow:

PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embedding Generation
 ↓
ChromaDB
Query
POST /query

Example request:

{
  "question": "What is Retrieval-Augmented Generation?"
}

The system:

Question
 ↓
Embedding
 ↓
Semantic Search
 ↓
Top-3 Chunks
 ↓
Context Construction
 ↓
Llama 3.2
 ↓
Answer + Sources
Running the Project Locally
1. Clone Repository
git clone https://github.com/VaniSharma06/ReliableRAG.git
cd ReliableRAG
2. Create Virtual Environment
python -m venv .venv
Windows
.venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Install Ollama

Install Ollama and pull the required model:

ollama pull llama3.2:3b

Verify:

ollama list
5. Start Backend
uvicorn main:app --reload

The FastAPI service will be available locally.

6. Start Frontend

In another terminal:

streamlit run frontend.py
Running the Evaluation

Run:

python -m evaluation.run_evaluation

The benchmark results are saved to:

evaluation/results/evaluation_results.json

The Streamlit dashboard reads the generated results and displays them in the:

Quality Benchmark

section.

Example Workflow
Step 1 — Upload

Upload a PDF through the application.

Step 2 — Index

ReliableRAG extracts and chunks the document.

Step 3 — Embed

Each chunk is converted into a semantic vector.

Step 4 — Store

Vectors are persisted in ChromaDB.

Step 5 — Query

The user asks a natural-language question.

Step 6 — Retrieve

The system retrieves the top 3 semantically relevant chunks.

Step 7 — Generate

Llama 3.2 generates an answer using the retrieved context.

Step 8 — Evaluate

The answer and retrieval pipeline can be evaluated against the benchmark dataset.

Reliability-Oriented Design

ReliableRAG focuses on reducing unsupported generation by constraining the model's information source.

The generation prompt follows this principle:

Retrieved Context
        ↓
       LLM
        ↓
Grounded Answer

rather than:

User Question
        ↓
LLM's General Knowledge
        ↓
Potentially Unsupported Answer

The evaluation framework then provides measurable signals for improving the retrieval and generation pipeline.

Testing

The repository includes tests for core components:

app/test_ingestion.py
app/test_vector_store.py

These tests help validate:

PDF ingestion
Text chunking
Vector-store behavior
Retrieval functionality
Current Limitations

ReliableRAG is intentionally transparent about its current limitations.

1. Lightweight Evaluation

The current evaluation metrics are primarily lexical/heuristic rather than full semantic judge-based evaluation.

2. Small Benchmark

The current benchmark contains 4 questions and is intended as a reproducible demonstration dataset.

3. Local LLM Size

Llama 3.2 3B provides lightweight local inference, but larger models may produce different quality/latency trade-offs.

4. Retrieval Strategy

The current system uses dense semantic retrieval without a dedicated reranking stage.

5. Document Scope

The current ingestion pipeline focuses on text-based PDFs.

Future Improvements

Potential engineering extensions include:

Cross-encoder reranking
Hybrid BM25 + dense retrieval
Larger evaluation datasets
Semantic answer evaluation
LLM-as-a-judge evaluation
RAGAS-style evaluation
Retrieval precision / recall measurement
Query latency monitoring
Experiment tracking
Multi-document metadata filtering
Streaming LLM responses
Authentication and user isolation
Docker deployment
CI/CD pipeline
Automated regression testing
Evaluation dashboards
Retrieval configuration experiments
What This Project Demonstrates

ReliableRAG demonstrates practical experience with:

Python
│
├── Backend API Development
├── REST API Design
├── Document Processing
├── NLP
├── Embeddings
├── Vector Databases
├── Semantic Search
├── Retrieval-Augmented Generation
├── Local LLM Inference
├── Evaluation Engineering
├── Automated Benchmarking
├── Testing
└── Full-Stack AI Application Development

More importantly, the project demonstrates an engineering workflow of:

Build
  ↓
Measure
  ↓
Inspect
  ↓
Evaluate
  ↓
Identify Limitations
  ↓
Improve
Resume-Ready Project Summary
ReliableRAG — Evaluation-Driven RAG System

Built an end-to-end Retrieval-Augmented Generation system using Python, FastAPI, ChromaDB, Sentence Transformers, Ollama and Llama 3.2, implementing PDF ingestion, overlapping text chunking, semantic vector retrieval and context-grounded response generation.

Developed an automated evaluation pipeline measuring retrieval quality, context relevance, faithfulness, answer correctness and response latency across a reproducible benchmark dataset.

Designed a Streamlit monitoring interface exposing retrieved sources, system pipeline stages and benchmark results, with persistent vector storage and local LLM inference for reproducible, API-independent experimentation.

Author

Vani Sharma

Computer Science & Engineering

LNCT, Bhopal

GitHub:
https://github.com/VaniSharma06

Project Status

Completed — Core RAG + Evaluation Pipeline

The current implementation provides:

PDF ingestion
Text chunking
Semantic embeddings
Persistent vector storage
Semantic retrieval
Local LLM inference
Grounded generation
Source transparency
Automated evaluation
Benchmark result persistence
Streamlit visualization
FastAPI backend
Automated tests
License

This project is intended for educational, research and portfolio purposes.
