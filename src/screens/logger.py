import streamlit as st
import tailer

class LogsPage:
    def __init__(self,session_id:int):
        self._arquivo_log = "historico_agente.log" 

    def render(self):
        st.title("Monitor de Logs dos Agentes")

        log_placeholder = st.empty()

        # Botão para atualizar a visualização manualmente
        if st.button("Atualizar Logs"):
            # Tente usar encoding='utf-8' com errors='replace' ou 'ignore'
            with open(self._arquivo_log, 'r', encoding='utf-8', errors='replace') as f:
                ultimas_linhas = tailer.tail(f, 50)
                conteudo = "\n".join(ultimas_linhas)
                log_placeholder.code(conteudo)
