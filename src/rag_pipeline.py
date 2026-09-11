from pathlib import Path

from src.loader import load_pdf
from src.splitter import split_documents
from src.vectorstore import create_vector_store
from src.retriever import create_retriever
from src.generation import generate_answer


PDF_PATH = Path("data") / "aws_rag_guide.pdf"


def build_rag_pipeline():
    # Load the PDF
    documents = load_pdf(str(PDF_PATH))

    # Split PDF into chunks
    chunks = split_documents(documents)

    # Create vector store
    vector_store = create_vector_store(chunks)

    # Create retriever
    retriever = create_retriever(vector_store)

    return retriever


def ask_question(question, retriever):
    # Retrieve relevant chunks
    documents = retriever.invoke(question)

    # Send retrieved chunks to the local LLM
    answer = generate_answer(
        question=question,
        documents=documents
    )

    return answer, documents