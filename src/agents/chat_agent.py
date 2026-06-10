from datetime import date

import streamlit as st
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.prompts import load_prompt

from agents.config import get_llm_gemini, get_llm_openrouter, AgentLogger
from agents.config.settings import GEMINI_MODEL, OPENROUTER_MODEL
from agents.expense_agent import ExpenseAgent
from shared.enums import LLM_Providers
from shared.repository import ExpenseRepository
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
        
        self._local_observer = AgentLogger()
        prompt = load_prompt("resources/prompts/chat_agent.yaml")

        @tool
        def get_expenses(description: str | None = None, expense_date: date | None = None):
            """
            Consulta despesas previamente registradas pelo usuário.

            Utilize esta ferramenta quando o usuário fizer perguntas sobre
            gastos já cadastrados, como consultas, buscas ou verificações.

            IMPORTANTE:
            - Pelo menos um dos filtros (description ou date) deve ser informado.
            - Nunca chame esta ferramenta sem fornecer ao menos um filtro.
            - Quando não houver informação suficiente para definir um filtro,
            solicite mais detalhes ao usuário.

            Exemplos de uso:
            - "Quanto gastei com gasolina?"
            - "Mostre minhas despesas de ontem."
            - "Eu já registrei mercado este mês?"
            - "Quais foram meus gastos na terça-feira?"
            - "Procure despesas relacionadas a Uber."

            Filtros disponíveis:
            - description:
            Texto utilizado para localizar despesas cuja descrição
            contenha o termo informado.

            - date:
            Data exata da despesa no formato YYYY-MM-DD.

            Observações:
            - Os filtros são opcionais individualmente, mas pelo menos um deles
            deve ser informado.
            - Quando mais de um filtro for informado, eles serão combinados.
            - A consulta é limitada à sessão atual do usuário.

            Returns:
                Lista de despesas encontradas contendo:
                - data
                - descricao
                - categoria
                - valor
            """
            result= self.expense_repository.get_expenses(
                session_id=self.session_id,
                descricao=description,
                data=expense_date,
            )

            return result

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
            tools=[call_expense_agent, ChatAgent.get_today_date, get_expenses],
        )

    @staticmethod
    @tool
    def get_today_date() -> str:
        """Retorna a data atual do sistema."""
        now = date.today()
        return now.strftime("%Y-%m-%d")

    def agent_call(self, messages: list) -> str:
        result = self.agent.invoke(
            {
                "messages": messages
            },
            config={
                "callbacks": [self._local_observer]
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
