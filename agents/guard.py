from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

guard_agent = Agent(
    role="Confidence Guard",
    goal="Decide whether the answer is reliable enough to return",
    backstory=(
        "You block weak or hallucinated answers."
    ),
    llm=ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1
    ),
    verbose=True
)
