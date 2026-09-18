from typing import Any
from pathlib import Path
import json
import time

import requests
import streamlit as st


# ============================================================
# CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000"

BASE_DIR = Path(__file__).resolve().parent

RESULTS_FILE = (
    BASE_DIR
    / "evaluation"
    / "results"
    / "evaluation_results.json"
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="ReliableRAG | AI Intelligence",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DARK THEME
# ============================================================

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #070a0f;
    }

    [data-testid="stSidebar"] {
        background-color: #090d13;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 5rem;
        padding-bottom: 4rem;
        margin-top:1rem;
    }

    h1, h2, h3 {
        color: #f1f5f9 !important;
    }

    p {
        color: #9aaabd;
    }

    [data-testid="stMetric"] {
        background-color: #0d141d;
        border: 1px solid #243447;
        padding: 18px;
        border-radius: 14px;
    }

    [data-testid="stMetricValue"] {
        color: #f1f5f9;
    }

    [data-testid="stMetricLabel"] {
        color: #7f92a8;
    }

    div.stButton > button {
        border-radius: 10px;
        min-height: 46px;
        font-weight: 700;
    }

    textarea {
        background-color: #0b1118 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNCTIONS
# ============================================================

def check_api() -> bool:
    try:
        response = requests.get(
            API_URL + "/",
            timeout=3,
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


def load_results() -> dict:
    if not RESULTS_FILE.exists():
        return {}

    try:
        with open(
            RESULTS_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

    except (
        OSError,
        json.JSONDecodeError,
    ):
        pass

    return {}


def number_value(
    data: dict,
    key: str,
) -> float:
    value = data.get(key, 0)

    if isinstance(value, (int, float)):
        return float(value)

    return 0.0


def percentage(value: float) -> str:
    return f"{value * 100:.1f}%"


# ============================================================
# API STATUS
# ============================================================

api_online = check_api()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("ReliableRAG")

    st.caption(
        "AI Retrieval Intelligence Platform"
    )

    st.divider()

    if api_online:
        st.success("● API ONLINE")
    else:
        st.error("● API OFFLINE")

    st.divider()

    st.subheader("SYSTEM")

    st.write("**Retrieval**")
    st.caption("Sentence Transformers")

    st.write("**Vector Database**")
    st.caption("ChromaDB")

    st.write("**Generation**")
    st.caption("Llama 3.2 · Ollama")

    st.write("**Backend**")
    st.caption("FastAPI")

    st.write("**Evaluation**")
    st.caption("Benchmark Pipeline")

    st.divider()

    st.subheader("ARCHITECTURE")

    st.code(
        """PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
 ↓
Semantic Retrieval
 ↓
Llama 3.2
 ↓
Evaluation""",
        language="text",
    )


# ============================================================
# HERO
# ============================================================

st.caption(
    "AI ENGINEERING  ·  RAG  ·  EVALUATION"
)

st.title("ReliableRAG")

st.write(
    "An evaluation-driven Retrieval-Augmented "
    "Generation system for grounded document intelligence."
)

st.write(
    "Retrieve relevant evidence, generate contextual "
    "answers, and measure response quality through an "
    "explicit evaluation pipeline."
)

if api_online:
    st.success(
        "● LOCAL AI INFERENCE ACTIVE"
    )
else:
    st.warning(
        "● START THE FASTAPI BACKEND TO ACTIVATE AI INFERENCE"
    )


st.divider()


# ============================================================
# PIPELINE
# ============================================================

st.subheader("Retrieval Pipeline")

st.caption(
    "From raw documents to grounded AI responses."
)

pipeline = st.columns(7)

pipeline_data = [
    ("01", "PDF", "Document"),
    ("02", "EXTRACT", "PyPDF"),
    ("03", "CHUNK", "1000 chars"),
    ("04", "EMBED", "MiniLM"),
    ("05", "RETRIEVE", "ChromaDB"),
    ("06", "GENERATE", "Llama 3.2"),
    ("07", "EVALUATE", "Metrics"),
]

for index, column in enumerate(pipeline):

    number, name, technology = pipeline_data[index]

    with column:

        st.info(
            f"**{number}**\n\n"
            f"**{name}**\n\n"
            f"{technology}"
        )


st.divider()


# ============================================================
# DOCUMENT INTELLIGENCE
# ============================================================

st.subheader("Document Intelligence")

st.caption(
    "Upload a PDF and index its content for semantic retrieval."
)


# Any avoids the incorrect PyCharm UploadedFile type warning.
uploaded_file: Any = st.file_uploader(
    "Upload PDF document",
    type=["pdf"],
    accept_multiple_files=False,
)


if uploaded_file is not None:

    filename = str(
        getattr(
            uploaded_file,
            "name",
            "document.pdf",
        )
    )

    file_bytes = bytes(
        uploaded_file.getvalue()
    )

    st.write(
        f"Selected document: **{filename}**"
    )

    if st.button(
        "INDEX DOCUMENT",
        use_container_width=True,
    ):

        if not api_online:

            st.error(
                "FastAPI is offline. Start main.py first."
            )

        else:

            try:

                with st.spinner(
                    "Extracting, chunking and indexing..."
                ):

                    response = requests.post(
                        API_URL + "/upload",
                        files={
                            "file": (
                                filename,
                                file_bytes,
                                "application/pdf",
                            )
                        },
                        timeout=180,
                    )

                if response.status_code == 200:

                    result = response.json()

                    if result.get("success"):

                        st.success(
                            "Document indexed successfully."
                        )

                        st.metric(
                            "CHUNKS INDEXED",
                            result.get(
                                "chunks_indexed",
                                0,
                            ),
                        )

                    else:

                        st.error(
                            result.get(
                                "message",
                                "Upload failed.",
                            )
                        )

                else:

                    st.error(
                        f"Backend returned HTTP "
                        f"{response.status_code}"
                    )

            except requests.RequestException as error:

                st.error(
                    f"Connection error: {error}"
                )


st.divider()


# ============================================================
# QUERY ENGINE
# ============================================================

st.subheader("Ask Your Documents")

st.caption(
    "Ask a question and receive a grounded answer "
    "with retrieved evidence."
)


question: str = st.text_area(
    "Question",
    placeholder=(
        "Example: What is the main purpose of this document?"
    ),
    height=120,
)


button1, button2 = st.columns(
    [5, 1]
)

with button1:

    generate_clicked = st.button(
        "GENERATE GROUNDED ANSWER",
        type="primary",
        use_container_width=True,
    )

with button2:

    clear_clicked = st.button(
        "CLEAR",
        use_container_width=True,
    )


if clear_clicked:
    st.rerun()


# ============================================================
# QUERY
# ============================================================

if generate_clicked:

    user_question = str(
        question
    ).strip()

    if not user_question:

        st.warning(
            "Please enter a question."
        )

    elif not api_online:

        st.error(
            "FastAPI is offline. Start main.py first."
        )

    else:

        start_time = time.perf_counter()

        try:

            with st.spinner(
                "Retrieving evidence and generating answer..."
            ):

                response = requests.post(
                    API_URL + "/query",
                    json={
                        "question": user_question
                    },
                    timeout=180,
                )

            elapsed = (
                time.perf_counter()
                - start_time
            )

            if response.status_code == 200:

                result = response.json()

                answer = str(
                    result.get(
                        "answer",
                        "No answer returned.",
                    )
                )

                sources = result.get(
                    "sources",
                    [],
                )

                evaluation = result.get(
                    "evaluation",
                    {},
                )

                # --------------------------------------------
                # ANSWER
                # --------------------------------------------

                st.subheader(
                    "Grounded Answer"
                )

                st.success(
                    answer
                )

                # --------------------------------------------
                # TELEMETRY
                # --------------------------------------------

                st.subheader(
                    "Response Telemetry"
                )

                metric1, metric2, metric3, metric4 = (
                    st.columns(4)
                )

                source_count = evaluation.get(
                    "source_count",
                    len(sources),
                )

                retrieval = evaluation.get(
                    "retrieval_score",
                    None,
                )

                relevance = evaluation.get(
                    "context_relevance",
                    None,
                )

                with metric1:

                    st.metric(
                        "SOURCES",
                        source_count,
                    )

                with metric2:

                    if isinstance(
                        retrieval,
                        (int, float),
                    ):

                        st.metric(
                            "RETRIEVAL",
                            percentage(
                                float(
                                    retrieval
                                )
                            ),
                        )

                    else:

                        st.metric(
                            "RETRIEVAL",
                            "—",
                        )

                with metric3:

                    if isinstance(
                        relevance,
                        (int, float),
                    ):

                        st.metric(
                            "RELEVANCE",
                            percentage(
                                float(
                                    relevance
                                )
                            ),
                        )

                    else:

                        st.metric(
                            "RELEVANCE",
                            "—",
                        )

                with metric4:

                    st.metric(
                        "LATENCY",
                        f"{elapsed:.2f}s",
                    )

                # --------------------------------------------
                # SOURCES
                # --------------------------------------------

                if sources:

                    st.subheader(
                        "Retrieved Evidence"
                    )

                    for index, source in enumerate(
                        sources,
                        start=1,
                    ):

                        with st.expander(
                            f"SOURCE {index}"
                        ):

                            st.write(
                                str(source)
                            )

            else:

                st.error(
                    f"Backend returned HTTP "
                    f"{response.status_code}"
                )

        except requests.RequestException as error:

            st.error(
                f"Could not connect to ReliableRAG API: "
                f"{error}"
            )


st.divider()


# ============================================================
# QUALITY BENCHMARK
# ============================================================

st.subheader(
    "Quality Benchmark"
)

st.caption(
    "Evaluation results generated from the benchmark dataset."
)


evaluation_data = load_results()


if not evaluation_data:

    st.info(
        "No evaluation results found. "
        "Run evaluation/run_evaluation.py first."
    )

else:

    summary = evaluation_data.get(
        "summary",
        {},
    )

    tests = evaluation_data.get(
        "tests",
        [],
    )

    if not isinstance(
        summary,
        dict,
    ):
        summary = {}

    if not isinstance(
        tests,
        list,
    ):
        tests = []


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    if summary:

        total_questions = summary.get(
            "total_questions",
            len(tests),
        )

        avg_retrieval = number_value(
            summary,
            "average_retrieval_score",
        )

        avg_relevance = number_value(
            summary,
            "average_context_relevance",
        )

        avg_faithfulness = number_value(
            summary,
            "average_faithfulness",
        )

        avg_correctness = number_value(
            summary,
            "average_answer_correctness",
        )

        avg_latency = number_value(
            summary,
            "average_latency_seconds",
        )


        b1, b2, b3, b4, b5, b6 = st.columns(6)

        with b1:
            st.metric(
                "QUESTIONS",
                total_questions,
            )

        with b2:
            st.metric(
                "RETRIEVAL",
                percentage(
                    avg_retrieval
                ),
            )

        with b3:
            st.metric(
                "RELEVANCE",
                percentage(
                    avg_relevance
                ),
            )

        with b4:
            st.metric(
                "FAITHFULNESS",
                percentage(
                    avg_faithfulness
                ),
            )

        with b5:
            st.metric(
                "CORRECTNESS",
                percentage(
                    avg_correctness
                ),
            )

        with b6:
            st.metric(
                "LATENCY",
                f"{avg_latency:.2f}s",
            )


    # --------------------------------------------------------
    # TEST RESULTS
    # --------------------------------------------------------

    if tests:

        st.write("")

        st.subheader(
            "Benchmark Test Results"
        )

        for test_number, test in enumerate(
            tests,
            start=1,
        ):

            if not isinstance(
                test,
                dict,
            ):
                continue

            test_question = str(
                test.get(
                    "question",
                    "Unknown question",
                )
            )

            expected_answer = str(
                test.get(
                    "expected_answer",
                    "",
                )
            )

            generated_answer = str(
                test.get(
                    "generated_answer",
                    "",
                )
            )

            metrics = test.get(
                "evaluation",
                {},
            )

            if not isinstance(
                metrics,
                dict,
            ):
                metrics = {}

            retrieval = number_value(
                metrics,
                "retrieval_score",
            )

            relevance = number_value(
                metrics,
                "context_relevance",
            )

            faithfulness = number_value(
                metrics,
                "faithfulness",
            )

            correctness = number_value(
                metrics,
                "answer_correctness",
            )

            with st.expander(
                f"TEST {test_number}  |  {test_question}"
            ):

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.metric(
                        "RETRIEVAL",
                        percentage(
                            retrieval
                        ),
                    )

                with c2:
                    st.metric(
                        "RELEVANCE",
                        percentage(
                            relevance
                        ),
                    )

                with c3:
                    st.metric(
                        "FAITHFULNESS",
                        percentage(
                            faithfulness
                        ),
                    )

                with c4:
                    st.metric(
                        "CORRECTNESS",
                        percentage(
                            correctness
                        ),
                    )

                st.write(
                    "**Expected Answer**"
                )

                st.info(
                    expected_answer
                )

                st.write(
                    "**Generated Answer**"
                )

                st.write(
                    generated_answer
                )

    else:

        st.warning(
            "The evaluation JSON was found, "
            "but no benchmark tests were found."
        )


st.divider()


# ============================================================
# ENGINEERING HIGHLIGHTS
# ============================================================

st.subheader(
    "System Design Highlights"
)

st.caption(
    "Core engineering decisions behind ReliableRAG."
)


e1, e2, e3 = st.columns(3)


with e1:

    st.markdown(
        "### Semantic Retrieval"
    )

    st.write(
        "Sentence Transformers convert document chunks "
        "into semantic vectors. ChromaDB performs vector "
        "similarity search to retrieve relevant context."
    )


with e2:

    st.markdown(
        "### Grounded Generation"
    )

    st.write(
        "Retrieved evidence is injected into a controlled "
        "generation prompt so the local LLM answers using "
        "document context."
    )


with e3:

    st.markdown(
        "### Evaluation-Driven AI"
    )

    st.write(
        "Retrieval quality, context relevance, faithfulness, "
        "answer correctness and latency are measured through "
        "a repeatable benchmark pipeline."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "RELIABLERAG · EVALUATION-DRIVEN "
    "RETRIEVAL-AUGMENTED GENERATION"
)

st.caption(
    "FastAPI · ChromaDB · Sentence Transformers · "
    "Ollama · Llama 3.2"
)