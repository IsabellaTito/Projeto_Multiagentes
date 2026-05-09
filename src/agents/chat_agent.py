import streamlit as st

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.prompts import load_prompt

from agents.config import get_llm_gemini, get_llm_openrouter
from agents.config.settings import GEMINI_MODEL, OPENROUTER_MODEL
from agents.expense_agent import ExpenseAgent
from shared.enums import LLM_Providers
from shared.repository.expense import ExpenseRepository
from shared.storage import get_db

class ChatAgent:
    def __init__(self, llm_provider: LLM_Providers = LLM_Providers.GEMINI, temperatura:float = 0, session_id: int = None):
        if llm_provider == LLM_Providers.GEMINI:
            self.llm = get_llm_gemini(model=GEMINI_MODEL,temperature=temperatura)
        elif llm_provider == LLM_Providers.OPENROUTER:
            self.llm = get_llm_openrouter(model=OPENROUTER_MODEL, temperature=temperatura)

        self.session_id = session_id

        self.sub_agent = ExpenseAgent(llm_provider=llm_provider)
        db = get_db()
        self.expense_repository = ExpenseRepository(db)
        
        prompt = load_prompt("resources/prompts/chat_agent.yaml")

        @tool
        def call_expense_agent(expense: str) -> str:
            """
            Processa uma despesa informada em linguagem natural.

            Esta tool envia a descrição da despesa para um
            subagente responsável por interpretar, categorizar
            e estruturar os dados do gasto.

            Após o processamento, a despesa é salva
            no banco de dados.

            Args:
                expense:
                    Texto contendo informações do gasto.

            Returns:
                Mensagem indicando sucesso ou falha.
            """

            try:
                response = self.sub_agent.agent_call(expense)

                self.expense_repository.create_expense(
                    session_id=self.session_id,
                    data=response.data,
                    descricao=response.descricao,
                    categoria=response.categoria,
                    valor=response.valor,
                )

                return f"""
                Gasto registrado com sucesso.

                Data: {response.data}
                Descrição: {response.descricao}
                Categoria: {response.categoria}
                Valor: R$ {response.valor}
                """

            except Exception as e:
                print(e)

                return (
                    "Erro inesperado ao salvar a despesa "
                    f"no banco: {e}"
                )
        
        self.agent = create_agent(
            model=self.llm,
            system_prompt=prompt.format(),
            tools=[call_expense_agent],
        )

    def agent_call(self, messages: list) -> str:
        result = self.agent.invoke(
            {
                "messages": messages
            }
        )

        content = result["messages"][-1].content

        # Gemini/OpenAI podem retornar conteúdos diferente de string
        if isinstance(content, list):
            texts = []

            for item in content:
                if isinstance(item, dict):
                    text = item.get("text")

                    if text:
                        texts.append(text)

                elif isinstance(item, str):
                    texts.append(item)

            return "\n".join(texts)

        return str(content)
