from langchain_core.prompts import ChatPromptTemplate


RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful assistant for answering questions from documents.

Use only the provided context to answer the question.

If the answer is not present in the context, say:
"I don't have enough information in the provided document to answer this question."

Do not make up information.
""",
        ),
        (
            "human",
            """
Context:
{context}

Question:
{question}
""",
        ),
    ]
)