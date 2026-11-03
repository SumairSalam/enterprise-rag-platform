# Enterprise RAG Platform

A learning project that answers questions about an AWS Prescriptive Guidance PDF
using Retrieval-Augmented Generation (RAG). The current implementation runs
locally: FAISS retrieves relevant text chunks, and Ollama generates an answer
using those chunks as context.

## What the project does

1. Loads `data/aws_rag_guide.pdf`, one PDF page per document.
2. Splits pages into overlapping text chunks.
3. Embeds each chunk and indexes the vectors in a FAISS vector store.
4. Retrieves the four most relevant chunks for a question.
5. Formats the retrieved text and its source metadata as context.
6. Sends the question and context to the local Ollama model.
7. Shows the answer and source pages in a Streamlit chat interface.

The project also includes a BM25 keyword retriever that can be combined with
semantic search. The main RAG pipeline currently uses the standard FAISS
retriever, not the hybrid retriever.

## Requirements

- Python 3.10 or newer
- Ollama installed and running locally
- The `llama3.2:3b` model pulled into Ollama
- Internet access on first run to download the embedding model

## Run on Windows (PowerShell)

Run these commands from the repository root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull llama3.2:3b
python -m streamlit run app.py
```

Open the local URL printed by Streamlit in your browser. The app builds its
retriever on the first question and caches it while the Streamlit process is
running. Restarting the app rebuilds the in-memory FAISS index. The current app
uses the included PDF; document uploads and persistent indexing are not yet
implemented.

If PowerShell blocks virtual-environment activation, allow it only for the
current terminal process:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

## Run the command-line demos

```powershell
python -m src.test_retrieval
python -m src.test_hybrid_retrieval
python -m src.test_rag
```

These modules print example results; they are demos rather than automated tests
with pass/fail assertions.

## Module guide

| Module | Responsibility |
| --- | --- |
| `app.py` | Streamlit chat UI, session history, and source display |
| `src/loader.py` | Load PDF pages and their metadata |
| `src/splitter.py` | Split page documents into overlapping chunks |
| `src/embeddings.py` | Create the sentence-transformer embedding model |
| `src/vectorstore.py` | Build a FAISS index from chunks and embeddings |
| `src/retriever.py` | Configure semantic search over the FAISS index |
| `src/hybrid_retriever.py` | Combine semantic results with BM25 keyword results |
| `src/rag_pipeline.py` | Build the retriever and coordinate question answering |
| `src/context.py` | Format retrieved chunks and source metadata for the prompt |
| `src/prompts.py` | Define instructions that ground answers in retrieved context |
| `src/llm.py` | Configure the local Ollama chat model |
| `src/generation.py` | Send the question and formatted context to the model |

## Current scope and next steps

This is a local learning prototype, not an AWS deployment. A deployment-ready
version still needs document uploads, persistent storage, application
configuration, automated tests, and authentication. A possible AWS path is S3
for PDF storage, Amazon Bedrock for generation, persistent vector search such as
OpenSearch Serverless, and a container deployment on ECS Fargate with IAM
permissions, HTTPS, monitoring, and access control.