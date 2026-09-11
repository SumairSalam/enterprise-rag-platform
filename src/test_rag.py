from src.rag_pipeline import build_rag_pipeline, ask_question


def main():
    retriever = build_rag_pipeline()

    question = "How is RAG implemented using AWS services?"

    answer, documents = ask_question(
        question=question,
        retriever=retriever
    )

    print("\nQUESTION:")
    print(question)

    print("\nANSWER:")
    print(answer)

    print("\nSOURCES:")
    for doc in documents:
        print(
            doc.metadata.get("source"),
            "- Page",
            doc.metadata.get("page")
        )


if __name__ == "__main__":
    main()