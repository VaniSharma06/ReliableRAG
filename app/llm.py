import ollama


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are ReliableRAG, an AI assistant that answers questions from
provided documents.

Use ONLY the context below to answer the question.

If the answer cannot be found in the context, say:
"I cannot determine the answer from the provided documents."

Context:
{context}

Question:
{question}

Give a clear and concise answer.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]