from langchain.agents import create_agent
from langchain_core.prompts import load_prompt

from agents.config import get_llm_gemini
from shared.enums import LLM_Providers

class ChatAgent:
    def __init__(self, llm_provider: LLM_Providers, temperatura:float = 0, model:str = "gemini-2.5-flash"):
        if llm_provider == LLM_Providers.GEMINI:
            self.llm = get_llm_gemini(model,temperatura)
        
        prompt = load_prompt("resources/prompts/chat_agent.yaml")

        self.agent = create_agent(
            model = self.llm,
            system_prompt=prompt.format()
        )

    def agent_call(self, input: list) -> str:
        result = self.agent.invoke(
            {
                "messages": input
            }
        )
        return result["messages"][-1].content
    



    

