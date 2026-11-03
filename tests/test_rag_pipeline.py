from pathlib import Path

from src import rag_pipeline


def test_build_pipeline_uses_supplied_pdf(monkeypatch):
    pdf_path = Path("sample.pdf")
    documents = ["loaded document"]
    chunks = ["split chunk"]
    vector_store = object()
    retriever = object()
    calls = []

    def fake_load_pdf(path):
        calls.append(("load_pdf", path))
        return documents

    def fake_split_documents(received_documents):
        calls.append(("split_documents", received_documents))
        return chunks

    def fake_create_vector_store(received_chunks):
        calls.append(("create_vector_store", received_chunks))
        return vector_store

    def fake_create_retriever(received_store):
        calls.append(("create_retriever", received_store))
        return retriever

    monkeypatch.setattr(rag_pipeline, "load_pdf", fake_load_pdf)
    monkeypatch.setattr(rag_pipeline, "split_documents", fake_split_documents)
    monkeypatch.setattr(
        rag_pipeline, "create_vector_store", fake_create_vector_store
    )
    monkeypatch.setattr(
        rag_pipeline, "create_retriever", fake_create_retriever
    )

    result = rag_pipeline.build_rag_pipeline(pdf_path)

    assert result is retriever
    assert calls == [
        ("load_pdf", str(pdf_path)),
        ("split_documents", documents),
        ("create_vector_store", chunks),
        ("create_retriever", vector_store),
    ]


def test_ask_question_returns_answer_and_sources(monkeypatch):
    question = "What does this document say?"
    documents = ["matching passage"]
    generated = []

    class FakeRetriever:
        def invoke(self, received_question):
            assert received_question == question
            return documents

    def fake_generate_answer(question, documents):
        generated.append((question, documents))
        return "The answer"

    monkeypatch.setattr(
        rag_pipeline, "generate_answer", fake_generate_answer
    )

    answer, sources = rag_pipeline.ask_question(question, FakeRetriever())

    assert generated == [(question, documents)]
    assert answer == "The answer"
    assert sources == documents
