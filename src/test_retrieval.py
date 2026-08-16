# from src.loader import load_pdf
# from src.splitter import split_documents
# from src.vectorstore import create_vector_store
# from src.retriever import create_retriever


# documents = load_pdf("data\aws_rag_guide.pdf")
from pathlib import Path

from src.loader import load_pdf
from src.splitter import split_documents
from src.vectorstore import create_vector_store
from src.retriever import create_retriever


documents = load_pdf(str(Path("data") / "aws_rag_guide.pdf"))

chunks = split_documents(documents)

vector_store = create_vector_store(chunks)

retriever = create_retriever(vector_store)


query = "What are the main challenges discussed?"


results = retriever.invoke(query)


for i, document in enumerate(results):

    print(f"\n--- RESULT {i + 1} ---")

    print(document.page_content)

    print("\nMetadata:")

    print(document.metadata)