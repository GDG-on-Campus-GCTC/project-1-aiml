from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

validation_agent = Agent(
    role="Answer Validator",
    goal="Verify correctness and identify gaps or mistakes",
    backstory=(
        "You review answers like a strict GCTC examiner."
    ),
    llm=ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1
    ),
    verbose=True
)
