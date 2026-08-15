# from langchain_community.document_loaders import PyPDFLoader
# from src.splitter import split_documents

# def load_pdf(file_path: str):
#     loader = PyPDFLoader(file_path)
#     documents = loader.load()
#     return documents


# if __name__ == "__main__":

#     docs = load_pdf("C:\Users\sumai\Desktop\projects\ENTERPRISE_RAG_PLATTFORM\data\aws_rag_guide.pdf")

#     print(f"Pages loaded: {len(docs)}")

#     print("\nFirst page:")
#     print(docs[0].page_content[:1000])

#     print("\nMetadata:")
#     print(docs[0].metadata)
    




from langchain_community.document_loaders import PyPDFLoader
from src.splitter import split_documents


def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents


if __name__ == "__main__":

    docs = load_pdf("C:\\Users\\sumai\\Desktop\\projects\\ENTERPRISE_RAG_PLATTFORM\\data\\aws_rag_guide.pdf")

    chunks = split_documents(docs)

    print("Pages:", len(docs))

    print("Chunks:", len(chunks))

    print("\nFirst chunk:")
    print(chunks[0].page_content)
