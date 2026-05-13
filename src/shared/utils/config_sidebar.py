import streamlit as st
from streamlit_extras.avatar import *
from streamlit_option_menu import option_menu

def init_sidebar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Financial Agents",
            options=["Chat", "Uploads", "Planilha", "Dashboard", "Log Out"],
            icons=["chat-right-text-fill", "file-earmark-arrow-up-fill", "table", "clipboard-data-fill", "door-open-fill"],
            menu_icon="cash-coin",
            default_index=0,
            # orientation="horizontal",
            key="selected",
        )

    with st.sidebar:
        avatar(
            "https://github.com/IsabellaTito.png",
            label="Isabella Tito",
            caption="Creator",
        )

    with st.sidebar:
        avatar(
            "https://github.com/Matheus256.png",
            label="Matheus Nascimento",
            caption="Creator",
        )
    
    return selected

