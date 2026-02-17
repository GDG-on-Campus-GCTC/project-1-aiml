from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.agents import AgentAction, AgentFinish
from queue import Queue
from typing import Any, Dict, List, Union

class CustomTokenHandler(BaseCallbackHandler):
    def __init__(self, queue: Queue):
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        # print(f"Token: {token}", end="", flush=True) # Minimize spam
        self.queue.put(token)

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        self.queue.put(f"\n\nAgent Action: {action.tool}\n")
        self.queue.put(f"Input: {action.tool_input}\n")
        self.queue.put(f"Log: {action.log}\n")

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> Any:
        self.queue.put(f"\nTool Start: {serialized.get('name')}\n")
        self.queue.put(f"Input: {input_str}\n")

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        self.queue.put(f"\nTool Output: {output}\n")

    def on_llm_end(self, response, **kwargs) -> None:
        pass # Do not signal end here, as we might have multiple LLM calls

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        pass 
        
    def on_llm_error(self, error, **kwargs) -> None:
        self.queue.put(f"Error: {error}\n")
        self.queue.put(None)
