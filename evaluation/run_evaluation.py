import json
import time
from pathlib import Path

from evaluation.dataset import EVALUATION_DATASET
from app.vector_store import VectorStore
from app.llm import generate_answer
from evaluation.evaluator import evaluate_response


BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "evaluation" / "results"
RESULTS_DIR.mkdir(exist_ok=True)

RESULTS_FILE = RESULTS_DIR / "evaluation_results.json"


def run_evaluation():

    vector_store = VectorStore()
    results = []

    print("\n==============================")
    print("ReliableRAG Evaluation")
    print("==============================\n")

    for index, item in enumerate(EVALUATION_DATASET, start=1):

        question = item["question"]

        print(f"Running test {index}/{len(EVALUATION_DATASET)}")
        print(f"Question: {question}")

        start_time = time.perf_counter()

        retrieved = vector_store.search(
            question,
            top_k=3
        )

        documents = retrieved["documents"][0]
        context = "\n\n".join(documents)

        answer = generate_answer(
            question,
            context
        )

        latency = time.perf_counter() - start_time

        evaluation = evaluate_response(
            question=question,
            answer=answer,
            retrieved_chunks=documents,
            expected_keywords=item["expected_keywords"]
        )

        evaluation["latency_seconds"] = round(latency, 3)

        results.append({
            "question": question,
            "expected_answer": item["expected_answer"],
            "generated_answer": answer,
            "evaluation": evaluation
        })

        print(f"Retrieval Score: {evaluation['retrieval_score']}")
        print(f"Context Relevance: {evaluation['context_relevance']}")
        print(f"Faithfulness: {evaluation['faithfulness']}")
        print(f"Answer Correctness: {evaluation['answer_correctness']}")
        print(f"Latency: {evaluation['latency_seconds']} sec")
        print("-" * 50)

    # Calculate aggregate metrics
    count = len(results)

    if count > 0:
        avg_retrieval = sum(
            r["evaluation"]["retrieval_score"]
            for r in results
        ) / count

        avg_relevance = sum(
            r["evaluation"]["context_relevance"]
            for r in results
        ) / count

        avg_faithfulness = sum(
            r["evaluation"]["faithfulness"]
            for r in results
        ) / count

        avg_correctness = sum(
            r["evaluation"]["answer_correctness"]
            for r in results
        ) / count

        avg_latency = sum(
            r["evaluation"]["latency_seconds"]
            for r in results
        ) / count

    else:
        avg_retrieval = 0
        avg_relevance = 0
        avg_faithfulness = 0
        avg_correctness = 0
        avg_latency = 0

    summary = {
        "total_questions": count,
        "average_retrieval_score": round(avg_retrieval, 3),
        "average_context_relevance": round(avg_relevance, 3),
        "average_faithfulness": round(avg_faithfulness, 3),
        "average_answer_correctness": round(avg_correctness, 3),
        "average_latency_seconds": round(avg_latency, 3)
    }

    output = {
        "summary": summary,
        "tests": results
    }

    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)

    print("\n==============================")
    print("Evaluation Complete")
    print("==============================")

    print("\nAggregate Results:")
    print(json.dumps(summary, indent=4))

    print(f"\nResults saved to:")
    print(RESULTS_FILE)


if __name__ == "__main__":
    run_evaluation()