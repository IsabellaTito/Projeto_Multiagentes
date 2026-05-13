import streamlit as st

from shared.utils import hello_component

class LoginPage:
    def render(self):
        _, center, _ = st.columns([2,1,2])

        center.space("xxlarge")

        with center.container(width="stretch", border=True, vertical_alignment="center", height="stretch"):
            with st.form("Log in", border=False):
                hello_component()

                role = st.text_input("Email", placeholder="Enter email")

                password = st.text_input("Password", placeholder="Enter password", type="password")

                submitted = st.container(horizontal=True, horizontal_alignment="center").form_submit_button("Log in", type='primary')
            
                if submitted:
                    if role:
                        if password:
                            if password == "1234":
                                st.session_state.page_status = "Logged"
                                st.rerun()
                            else:
                                st.error("Invalid password.")
                        else:
                            st.warning("Enter a password")
                    else:
                        st.warning("Enter a email")