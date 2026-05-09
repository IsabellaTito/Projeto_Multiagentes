import time

import streamlit as st

from agents.chat_agent import ChatAgent
from agents.config.settings import LLM_PROVIDER
from shared.repository.session import ChatRepository
from shared.storage import get_db


class ChatPage():
    def __init__(self):
        db = get_db()
        self.chat_repository = ChatRepository(db)

        session_id = self.chat_repository.get_session_by_id(1)

        if session_id is None:
            chat_session = self.chat_repository.create_session()
            session_id = chat_session.id
        
        if "session_id" not in st.session_state:
            st.session_state.session_id = session_id

        if "messages" not in st.session_state:
            st.session_state.messages = self.chat_repository.get_messages_as_dict(st.session_state.session_id)

        self.agent = ChatAgent(llm_provider=LLM_PROVIDER, session_id=session_id)

    # função JS de scroll
    @staticmethod
    def auto_scroll():
        st.markdown(
            """
            <script>
            const doc = window.parent.document;
            const main = doc.querySelector('section.main');
            if (main) {
                main.scrollTop = main.scrollHeight;
            }
            </script>
            """,
            unsafe_allow_html=True
        )

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

                # placeholder da resposta
                with chat_container:
                    with st.chat_message("assistant"):
                        placeholder = st.empty()

                        full_response = ""

                        # streaming fake
                        size = len(agent_reponse.split())
                        scroll_step = max(1, size // 3)

                        for i, word in enumerate(agent_reponse.split()):
                            full_response += word + " "
                            placeholder.markdown(full_response)

                            if i % scroll_step == 0:
                                self.auto_scroll()  #scroll
                            time.sleep(0.05)

                # salva resposta final
                message = {"role": "assistant", "content": full_response}
                st.session_state.messages.append(message)

                self.chat_repository.create_message(
                    session_id=st.session_state.session_id, 
                    role=user_message["role"],
                    content=user_message["content"])

                self.chat_repository.create_message(
                    session_id=st.session_state.session_id, 
                    role=message["role"],
                    content=message["content"])
                
            except Exception as e:
                st.error(f"Erro inesperado: {e}")

