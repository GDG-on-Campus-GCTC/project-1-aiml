import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from crewai.tools import tool

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


FAISS_DIR = os.path.join(BASE_DIR, "finalfirstret")

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

@tool("retriever_tooltwo")
def retriever_tooltwo(query: str) -> str:
    """
    all first yerar subject like BEE or Basic Electrical Engineering , pps 1 and pps 2 or Programming for problem solving 1 and 2 
    mvc , bem  , applied physics ap , semiconductor devieces sd , engineering chemistry ec , engineering mathematics em  you should only call this tool `retriever_tooltwo` to retrieve notes and then answer the question based on the retrieved content only mainly only when mentioned 1 st year.

    """
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found."

    return "\n\n".join(
        f"[Source: {d.metadata.get('source', 'unknown')} | Page: {d.metadata.get('page', 'NA')}]\n{d.page_content}"
        for d in docs
    )

