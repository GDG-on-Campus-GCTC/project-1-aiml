from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage, SystemMessage
from teachers.similar import retriever_tooltwo
from teachers.tooler import retriever_tooltwot
from teachers.toolers import retriever_toolthree
from teachers.fourth import retriever_toolfour
import yaml
import os

class QueueCallbackHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.queue.put(token)

    def on_llm_end(self, response, **kwargs) -> None:
        pass

    def on_llm_error(self, error, **kwargs) -> None:
        self.queue.put(f"\n❌ Error: {error}\n")
        self.queue.put(None)

def run_lite_mode(inputs, queue):
    """
    Runs the Tutor logic using direct LLM invocation with tool results.
    This bypasses the complex agent framework to avoid compatibility issues.
    """
    try:
        config_path = "src/teachers/config/agents.yaml"
        if not os.path.exists(config_path):
            config_path = "teachers/src/teachers/config/agents.yaml"
        
        try:
            with open(config_path, "r") as f:
                agents_config = yaml.safe_load(f)
            tutor_config = agents_config.get("tutor", {})
            role = tutor_config.get("role", "Tutor")
            goal = tutor_config.get("goal", "Help the student.")
            backstory = tutor_config.get("backstory", "You are a helpful tutor.")
        except Exception as e:
            print(f"Config load warning: {e}")
            role = "Tutor"
            goal = "Help student"
            backstory = "Helpful AI"

        steps_handler = QueueCallbackHandler(queue)
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            streaming=True,
            callbacks=[steps_handler]
        )

        query = inputs.get('topic', '')
        year = inputs.get('current_year', '2026')
        
        context_parts = []
        tools = [
            ("Year 4 Retriever", retriever_toolfour),
            ("Year 2 Retriever", retriever_tooltwot),
            ("General Retriever 1", retriever_tooltwo),
            ("General Retriever 2", retriever_toolthree)
        ]
        
        for tool_name, tool in tools:
            try:
                result = tool.run(query)
                if result and len(str(result).strip()) > 50:
                    context_parts.append(f"From {tool_name}:\n{result}\n")
            except Exception as e:
                pass
                continue
        
        if context_parts:
            context = "\n---\n".join(context_parts)
        else:
            context = "No specific documents found. Use your general knowledge."
        
        system_prompt = f"""You are a {role}.
Goal: {goal}
Backstory: {backstory}

Current Year Context: {year}

RETRIEVED INFORMATION:
{context}

Instructions:
1. Use the retrieved information above as your PRIMARY source
2. If the retrieved info is incomplete, supplement with your knowledge
3. Be concise and accurate
4. Format your answer clearly"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Question: {query}")
        ]
        
        llm.invoke(messages)
        
        # Signal completion
        queue.put(None)
        
    except Exception as e:
        print(f"Error in lite mode: {e}")
        queue.put(f"\n❌ Error: {e}\n")
        queue.put(None)
