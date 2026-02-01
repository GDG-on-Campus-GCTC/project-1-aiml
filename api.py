from fastapi import FastAPI
from crew import run_crew

app = FastAPI()

@app.post("/qa")
def qa(payload: dict):
    question = payload.get("question")

    result = run_crew(question)

    if "NO_CONFIDENT_ANSWER" in str(result):
        return {
            "answer": "No confident answer available.",
            "confidence": "low"
        }

    return {
        "answer": str(result),
        "confidence": "high"
    }
