import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from crewai.tools import tool

# --------------------------------------------------
# Absolute path (IMPORTANT)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_FILE = os.path.join(BASE_DIR, "output1 (2).txt")

@tool("retriever_tool1")
def callers(query: str) -> str:
    """
    Retrieve relevant text chunks from a document using FAISS
    """

    if not os.path.exists(TEXT_FILE):
        return f"File not found: {TEXT_FILE}"

    # Load document
    loader = TextLoader(TEXT_FILE, encoding="utf-8")
    documents = loader.load()

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # FAISS (in-memory only)
    vector_store = FAISS.from_documents(chunks, embeddings)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 6}
    )

    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found in the documents."

    return "\n\n".join(doc.page_content for doc in docs)