import time

import streamlit as st

from shared.repository.session import ChatRepository
from shared.storage import get_db


class ChatPage():
    def __init__(self):
        db = get_db()
        self.chat_repository = ChatRepository(db)

        session_id = self.chat_repository.get_session_by_id(1)

        if session_id is None:
            session_id = self.chat_repository.create_session()
        
        if "session_id" not in st.session_state:
            st.session_state.session_id = session_id

        if "messages" not in st.session_state:
            st.session_state.messages = self.chat_repository.get_messages_as_dict(st.session_state.session_id)

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
            # adiciona user
            message = {"role": "user", "content": prompt}

            st.session_state.messages.append(message)

            self.chat_repository.create_message(
                session_id=st.session_state.session_id, 
                role=message["role"],
                content=message["content"])

            with chat_container:
                with st.chat_message("user"):
                    st.write(prompt)

            # placeholder da resposta
            with chat_container:
                with st.chat_message("assistant"):
                    placeholder = st.empty()

                    full_response = ""

                    # streaming fake
                    size = len(prompt.split())
                    for i, word in enumerate(prompt.split()):
                        full_response += word + " "
                        placeholder.markdown(full_response)

                        if i % (size/3) == 0:
                            self.auto_scroll()  #scroll
                        time.sleep(0.05)

            # salva resposta final
            message = {"role": "assistant", "content": full_response}
            st.session_state.messages.append(message)
            self.chat_repository.create_message(
                session_id=st.session_state.session_id, 
                role=message["role"],
                content=message["content"])

