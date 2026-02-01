from crewai import Crew, Task
from agents.researcher import research_agent
from agents.validator import validation_agent
from agents.formatter import formatting_agent
from agents.guard import guard_agent


def run_crew(question: str):

    research_task = Task(
        description=f"""
        Research and draft a clear academic answer for the question:
        "{question}"

        Do not guess. Use correct academic reasoning.
        """,
        expected_output="""
        A detailed draft answer explaining the concept clearly and correctly.
        """,
        agent=research_agent
    )

    validation_task = Task(
        description="""
        Validate the research answer for correctness, completeness,
        and logical soundness. Identify any errors or missing points.
        """,
        expected_output="""
        A validated and corrected version of the answer,
        or a statement that the answer is weak or incorrect.
        """,
        agent=validation_agent
    )

    guard_task = Task(
        description="""
        Decide whether the validated answer is reliable enough
        to be shown to students.

        If the answer is weak, incomplete, or speculative,
        respond ONLY with the exact string:
        NO_CONFIDENT_ANSWER
        """,
        expected_output="""
        Either NO_CONFIDENT_ANSWER
        or a confirmation that the answer is acceptable.
        """,
        agent=guard_agent
    )

    formatting_task = Task(
        description="""
        Format the final approved answer into a concise,
        student-friendly, exam-ready explanation.
        """,
        expected_output="""
        A clean, well-structured final answer suitable for students.
        """,
        agent=formatting_agent
    )

    crew = Crew(
        agents=[
            research_agent,
            validation_agent,
            guard_agent,
            formatting_agent
        ],
        tasks=[
            research_task,
            validation_task,
            guard_task,
            formatting_task
        ],
        verbose=True
    )

    return crew.kickoff()
