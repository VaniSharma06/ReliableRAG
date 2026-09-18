from typing import List, Dict


def calculate_retrieval_score(
    retrieved_chunks: List[str],
    expected_keywords: List[str]
) -> float:

    if not expected_keywords:
        return 0.0

    combined_text = " ".join(retrieved_chunks).lower()

    matches = sum(
        1
        for keyword in expected_keywords
        if keyword.lower() in combined_text
    )

    return round(matches / len(expected_keywords), 2)


def calculate_context_relevance(
    question: str,
    retrieved_chunks: List[str]
) -> float:

    if not retrieved_chunks:
        return 0.0

    question_words = {
        word.lower().strip(".,?!")
        for word in question.split()
        if len(word) > 3
    }

    context = " ".join(retrieved_chunks).lower()

    if not question_words:
        return 0.0

    matches = sum(
        1 for word in question_words
        if word in context
    )

    return round(
        min(matches / len(question_words), 1.0),
        2
    )


def calculate_faithfulness(
    answer: str,
    retrieved_chunks: List[str]
) -> float:

    if not answer.strip() or not retrieved_chunks:
        return 0.0

    context = " ".join(retrieved_chunks).lower()

    answer_words = {
        word.lower().strip(".,?!")
        for word in answer.split()
        if len(word) > 4
    }

    if not answer_words:
        return 0.0

    supported_words = sum(
        1 for word in answer_words
        if word in context
    )

    return round(
        min(supported_words / len(answer_words), 1.0),
        2
    )


def calculate_answer_correctness(
    answer: str,
    expected_keywords: List[str]
) -> float:

    if not answer.strip() or not expected_keywords:
        return 0.0

    answer_lower = answer.lower()

    matches = sum(
        1
        for keyword in expected_keywords
        if keyword.lower() in answer_lower
    )

    return round(
        matches / len(expected_keywords),
        2
    )


def evaluate_response(
    question: str,
    answer: str,
    retrieved_chunks: List[str],
    expected_keywords: List[str]
) -> Dict:

    retrieval_score = calculate_retrieval_score(
        retrieved_chunks,
        expected_keywords
    )

    context_relevance = calculate_context_relevance(
        question,
        retrieved_chunks
    )

    faithfulness = calculate_faithfulness(
        answer,
        retrieved_chunks
    )

    answer_correctness = calculate_answer_correctness(
        answer,
        expected_keywords
    )

    return {
        "retrieval_score": retrieval_score,
        "context_relevance": context_relevance,
        "faithfulness": faithfulness,
        "answer_correctness": answer_correctness,
        "answer_generated": bool(answer.strip()),
        "source_count": len(retrieved_chunks)
    }