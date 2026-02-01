from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

research_agent = Agent(
    role="Academic Researcher",
    goal="Research and derive an accurate academic answer",
    backstory=(
        "You are an expert GCTC instructor. "
        "You reason step-by-step and never guess."
    ),
    llm=ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1
    ),
    verbose=True
)
