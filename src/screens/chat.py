import time

import streamlit as st

from agents.chat_agent import ChatAgent
from agents.config.settings import LLM_PROVIDER
from shared.repository import MessageRepository
from shared.storage import get_db


class ChatPage():
    def __init__(self,session_id:int):
        
        db = get_db()
        self.message_repository = MessageRepository(db)
        
        if "session_id" not in st.session_state:
            st.session_state.session_id = session_id

        if "messages" not in st.session_state:
            st.session_state.messages = self.message_repository.get_messages_as_dict(st.session_state.session_id)
        
        if not st.session_state.messages:
            apresentacao ="""
                    Olá, sou seu assistente financeiro pessoal! 💰

                    Te ajudarei a organizar melhor seus gastos.
                    
                    Vamos começar os registros?  
                    Basta me contar os gastos que organizarei tudo para você.
                                    
                """
            
            st.session_state.messages.append({"role": "assistant", "content": apresentacao})


        self.agent = ChatAgent(llm_provider=LLM_PROVIDER, session_id=session_id)

    @staticmethod
    def stream_message(message: str, delay: float = 0.05):
        for word in message.split():
            yield word + " "
            time.sleep(delay)

    def render(self):
        chat_container = st.container(height="stretch", border=False, width="stretch")

        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        # input
        if prompt := st.chat_input("Digite algo"):
            try:
                # adiciona user
                user_message = {"role": "user", "content": prompt}
                st.session_state.messages.append(user_message)

                with chat_container:
                    with st.chat_message("user"):
                        st.write(prompt)

                with st.spinner(text="Pensando..."):
                    agent_reponse = self.agent.agent_call(st.session_state.messages[-10:])

                # stream da resposta
                with chat_container:
                    with st.chat_message("assistant"):
                        st.write_stream(self.stream_message(agent_reponse))

                # salva resposta final
                message = {"role": "assistant", "content": agent_reponse}
                st.session_state.messages.append(message)

                self.message_repository.create_message(
                    session_id=st.session_state.session_id, 
                    role=user_message["role"],
                    content=user_message["content"])

                self.message_repository.create_message(
                    session_id=st.session_state.session_id, 
                    role=message["role"],
                    content=message["content"])
                
            except Exception as e:
                st.error(f"Erro inesperado: {e}")

