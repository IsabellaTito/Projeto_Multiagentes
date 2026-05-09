from datetime import date

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.prompts import load_prompt

from agents.config import get_llm_gemini, get_llm_openrouter
from agents.config.settings import GEMINI_MODEL, OPENROUTER_MODEL
from shared.enums import LLM_Providers
from shared.schemas import ExpenseSchema


class ExpenseAgent:
    def __init__(self, llm_provider: LLM_Providers, temperatura:float = 0):
        if llm_provider == LLM_Providers.GEMINI:
            self.llm = get_llm_gemini(model=GEMINI_MODEL, temperature=temperatura)
        elif llm_provider == LLM_Providers.OPENROUTER:
            self.llm = get_llm_openrouter(model=OPENROUTER_MODEL, temperature=temperatura)
        
        prompt = load_prompt("resources/prompts/expense_agent.yaml")

        self.agent = create_agent(
            model = self.llm,
            tools=[self.get_atual_date],
            system_prompt=prompt.format(),
            #response_format=ExpenseSchema,
        )

        self.extractor = self.llm.with_structured_output(ExpenseSchema)

    def agent_call(self, text: str) -> ExpenseSchema:

        result = self.agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ]
        })

        final_text = self._extract_text(result["messages"][-1])

        final_text = (
            final_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        structured = self.extractor.invoke(final_text)

        return structured
    
    @staticmethod
    @tool
    def get_atual_date() -> str:
        """Retorna a data atual do sistema."""
        now = date.today()
        return now.strftime("%Y-%m-%d")
    
    @staticmethod
    def _extract_text(message) -> str:

        content = message.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):

            texts = []

            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        texts.append(
                            block.get("text", "")
                        )
            return "\n".join(texts)

        return str(content)
