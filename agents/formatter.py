from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

formatting_agent = Agent(
    role="Answer Formatter",
    goal="Format a concise, exam-ready answer",
    backstory=(
        "You convert verified content into clear student-friendly answers."
    ),
    llm=ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1
    ),
    verbose=True
)
