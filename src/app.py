import streamlit as st

from screens import ChatPage, UploadsPage, SheetPage

from agents.expense_agent import ExpenseAgent
from agents.config.settings import LLM_PROVIDER

from shared.utils import init_session, init_sidebar

st.set_page_config(
    page_title="Financial Agents",
    page_icon="resources/assets/cash-coin.svg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

selected = init_sidebar()

session = init_session()

if selected == "Chat":
    chat_page = ChatPage(session)
    chat_page.render()

if selected == "Uploads":
    upload_page = UploadsPage()
    upload_page.render()

if selected == "Planilha":
    sheet_page = SheetPage(session)
    sheet_page.render()


#    st.title(f"You have selected {selected}")
#    agent = ExpenseAgent(llm_provider=LLM_PROVIDER)
#    text = st.text_input("Gasto")

#    if text:
#        response = agent.agent_call(text)
#        st.warning(response)
#        st.warning(f"{response.data} - {response.valor} - {response.descricao} - {response.categoria}")



if selected == "Dashboard":
    st.title(f"You have selected {selected}")