from langchain_openai import OpenAIEmbeddings


def get_embedding_model():
    embedings = OpenAIEmbeddings(
        model="text-embedding-3-small",
    )
    return embedings()