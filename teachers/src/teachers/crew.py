from crewai import Agent, Crew, Process, Task, LLM
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

    @agent
    def tutor(self) -> Agent:
        agent_config = self.agents_config["tutor"]
        stream_handler = getattr(self, 'stream_handler', None)
        print(f"DEBUG: Creating tutor agent. Stream handler present: {stream_handler is not None}") # DEBUG LOG
        callbacks = [stream_handler] if stream_handler else []
        
        return Agent(
            config=agent_config, 
            tools=[retriever_toolfour,retriever_tooltwot,retriever_tooltwo,retriever_toolthree],
            callbacks=callbacks
        )

    @task
    def quick_answer_task(self) -> Task:
        return Task(config=self.tasks_config["quick_answer_task"])

    @crew
    def simple_crew(self, stream_handler=None) -> Crew:
        # Manually create the agent to ensure callbacks are attached correctly
        agent_config = self.agents_config["tutor"]
        
        # Create LLM with callback if handler exists
        llm = None
        if stream_handler:
            # We must use the same model as defined in agents.yaml
            llm = LLM(
                model="gemini/gemini-2.5-flash",
                callbacks=[stream_handler]
            )
            print(f"DEBUG: Created LLM with callback: {stream_handler}")
        
        tutor_agent = Agent(
            role=agent_config['role'], # Helper to ensure role matches
            goal=agent_config['goal'],
            backstory=agent_config['backstory'],
            tools=[retriever_toolfour, retriever_tooltwot, retriever_tooltwo, retriever_toolthree],
            llm=llm if llm else "gemini/gemini-2.5-flash", # Use created LLM or default string
            callbacks=[stream_handler] if stream_handler else [], # Explicitly attach to Agent too
            verbose=True
        )

        # Get task and explicitly assign agent to override any defaults
        task = self.quick_answer_task()
        task.agent = tutor_agent

        return Crew(
            agents=[tutor_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
