from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from teachers.similar import retriever_tooltwo
from teachers.tooler import retriever_tooltwot
from teachers.toolers import retriever_toolthree
from teachers.fourth import retriever_toolfour
from crewai.memory import ShortTermMemory, LongTermMemory, EntityMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.storage.rag_storage import RAGStorage


@CrewBase
class Teachers():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def internal(self) -> Agent:
        return Agent(config=self.agents_config["internal"], tools=[retriever_toolfour,retriever_tooltwot,retriever_tooltwo,retriever_toolthree])

    @agent
    def external(self) -> Agent:
        return Agent(config=self.agents_config["external"], tools=[retriever_toolfour,retriever_tooltwot,retriever_tooltwo,retriever_toolthree])

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])

    @task
    def reporting_task(self) -> Task:
        return Task(config=self.tasks_config["reporting_task"])

    @crew
    def crewcall(self) -> Crew:
        
        manager=Agent(
            config=self.agents_config['manager'],
            delegation=True
        )

        short_term_memory = ShortTermMemory(
            storage=RAGStorage(
                embedder_config={
                    
                    "provider": "sentence-transformer",
                    "config": {
                        "model_name": "all-MiniLM-L6-v2"
                    }
                },
                type="short_term",
                path="./memory/short_term/"
            )
        )

        entity_memory = EntityMemory(
            storage=RAGStorage(
                embedder_config={
                    "provider": "sentence-transformer",
                    "config": {
                        "model_name": "all-MiniLM-L6-v2"
                    }
                },
                type="short_term",
                path="./memory/entity/"
            )
        )

        long_term_memory = LongTermMemory(
            storage=LTMSQLiteStorage(
                db_path="./memory/long_term_memory.db"
            )
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=manager,
            short_term_memory=short_term_memory,
            entity_memory=entity_memory,
            long_term_memory=long_term_memory,
            verbose=True
        )
