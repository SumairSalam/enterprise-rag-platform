def format_context(documents):
    formatted_chunks = []

    for i, doc in enumerate(documents, start=1):
        source = doc.metadata.get("source", "Unknown source")
        page = doc.metadata.get("page", "Unknown page")

        chunk = f"""
[Document {i}]
Source: {source}
Page: {page}

{doc.page_content}
"""

        formatted_chunks.append(chunk.strip())

    return "\n\n".join(formatted_chunks)