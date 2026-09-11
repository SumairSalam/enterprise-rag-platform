from src.llm import get_llm
from src.prompts import RAG_PROMPT
from src.context import format_context


def generate_answer(question, documents):
    llm = get_llm()

    context = format_context(documents)

    chain = RAG_PROMPT | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return response.content