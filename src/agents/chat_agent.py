from langchain.agents import create_agent

from agents.config import get_llm_gemini
from shared.enums import LLM_Providers

class ChatAgent:
    def __init__(self, llm_provider: LLM_Providers, temperatura:float = 0, model:str = "gemini-2.5-flash"):
        if llm_provider == LLM_Providers.GEMINI:
            self.llm = get_llm_gemini(model)
        self.agent = create_agent(
            model = self.llm,
            system_prompt=("""
                    Você é um assistente financeiro doméstico gentil, direto e organizado. Sua função é ajudar o usuário a registrar gastos do dia a dia.
                    Ao responder:

                    - Comece com uma mensagem simples e amigável                   
                    - Em seguida, apresente apenas as informações importantes do gasto.
                    - Não inclua explicações longas ou comentários desnecessários.
                    - Organize os dados de forma clara.     
                """.strip()
            )
        )

    def agent_call(self, input: list) -> str:
        result = self.agent.invoke(
            {
                "messages": input
            }
        )
        return result["messages"][-1].content
    



    

