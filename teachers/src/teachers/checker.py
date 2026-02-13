from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).parent

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore1 = FAISS.load_local(
    BASE_DIR / "first_year_retrival",
    embeddings,
    allow_dangerous_deserialization=True
)

vectorstore2 = FAISS.load_local(
    BASE_DIR / "first_year_retrival1-2",
    embeddings,
    allow_dangerous_deserialization=True
)

vectorstore1.merge_from(vectorstore2)

def query(q):
    retriever = vectorstore1.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 15}
    )

    docs = retriever.invoke(q)

    if not docs:
        return "No relevant information found."

    return "\n\n".join(
        f"[Source: {d.metadata.get('source', 'unknown')} | Page: {d.metadata.get('page', 'NA')}]\n{d.page_content}"
        for d in docs
    )
print(query("chemistry"))
