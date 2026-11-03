import streamlit as st

from src.rag_pipeline import ask_question, build_rag_pipeline


@st.cache_resource
def load_retriever():
    return build_rag_pipeline()


st.set_page_config(page_title="Document Q&A")
st.title("Ask your AWS RAG guide")
st.caption("Ask a question about the PDF. Answers include retrieved source pages.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Redisplay earlier questions and answers after Streamlit reruns the app.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sources"):
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.write(source)

question = st.chat_input("Ask a question")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the PDF and generating an answer..."):
            retriever = load_retriever()
            answer, documents = ask_question(question, retriever)

        sources = list(
            dict.fromkeys(
                f'{doc.metadata.get("source", "Unknown source")} '
                f'(page {doc.metadata.get("page", "Unknown page")})'
                for doc in documents
            )
        )

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