import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from crewai.tools import tool

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAISS_DIR = os.path.join(BASE_DIR, "first_year_retrival1-2")


if not os.path.exists(FAISS_DIR):
    raise FileNotFoundError(f"FAISS directory not found: {FAISS_DIR}")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vectorstore = FAISS.load_local(
    FAISS_DIR,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 15}
)


@tool("retriever_tool")
def retriever_toolonetwo(query: str) -> str:
    """
    Retrieve relevant chunks from FAISS vector database
    """

    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found."

    return "\n\n".join(
        f"[Source: {d.metadata.get('source', 'unknown')} | Page: {d.metadata.get('page', 'NA')}]\n{d.page_content}"
        for d in docs
    )
