import time

import streamlit as st


class ChatPage():

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
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

        chat_container = st.container(height="stretch", border=False, width=1200)

        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        # input
        if prompt := st.chat_input("Digite algo"):
            # adiciona user
            st.session_state.messages.append({"role": "user", "content": prompt})

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
                            self.auto_scroll()  # 👈 scroll a cada atualização
                        time.sleep(0.05)

            # salva resposta final
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

            