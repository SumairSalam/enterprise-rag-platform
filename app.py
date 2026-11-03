import hashlib
import tempfile
from pathlib import Path

import streamlit as st

from src.rag_pipeline import ask_question, build_rag_pipeline


DEFAULT_PDF_PATH = Path("data") / "aws_rag_guide.pdf"


@st.cache_resource(show_spinner=False)
def load_retriever(pdf_bytes: bytes | None, filename: str | None):
    if pdf_bytes is None:
        return build_rag_pipeline()

    if filename is None:
        raise ValueError("A filename is required for an uploaded PDF.")

    safe_filename = Path(filename).name

    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = Path(temp_dir) / safe_filename
        pdf_path.write_bytes(pdf_bytes)

        return build_rag_pipeline(pdf_path)


def get_sources(documents):
    sources = []
    seen = set()

    for document in documents:
        source_path = document.metadata.get("source", "Unknown source")
        source = Path(source_path).name
        page = document.metadata.get("page", "Unknown page")
        source_label = f"{source} (page {page})"

        if source_label not in seen:
            seen.add(source_label)
            sources.append(source_label)

    return sources


st.set_page_config(page_title="Document Q&A")
st.title("Ask a question about a PDF")
st.caption("Answers are based on the selected PDF and include source pages.")

uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_pdf is None:
    pdf_bytes = None
    filename = None
    document_key = "default"
    st.info(f"Using the bundled document: {DEFAULT_PDF_PATH.name}")
else:
    pdf_bytes = uploaded_pdf.getvalue()
    filename = uploaded_pdf.name
    document_key = hashlib.sha256(pdf_bytes).hexdigest()
    st.success(f"Selected: {filename}")

if st.session_state.get("document_key") != document_key:
    st.session_state.document_key = document_key
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sources"):
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.write(source)

question = st.chat_input("Ask a question about the selected PDF")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the PDF and generating an answer..."):
            retriever = load_retriever(pdf_bytes, filename)
            answer, documents = ask_question(question, retriever)

        sources = get_sources(documents)
        st.markdown(answer)

        if sources:
            with st.expander("Sources"):
                for source in sources:
                    st.write(source)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )