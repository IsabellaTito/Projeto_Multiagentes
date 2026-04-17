import streamlit as st

class UploadsPage():
    def render(self):
        st.title(f"You have selected {st.session_state["selected"]}")
        st.file_uploader(
            label="Envie os arquivos" 
        )