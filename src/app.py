import streamlit as st
from streamlit_extras.avatar import *
from streamlit_option_menu import option_menu

from screens.chat import ChatPage
from screens.uploads import UploadsPage

st.set_page_config(
    page_title="Financial Agents",
    page_icon="resources/assets/cash-coin.svg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

with st.sidebar:
    selected = option_menu(
        menu_title="Financial Agents",
        options=["Chat", "Uploads", "Planilha", "Dashboard"],
        icons=["chat-right-text-fill", "file-earmark-arrow-up-fill", "table", "clipboard-data-fill"],
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


if selected == "Chat":
    chat_page = ChatPage()
    chat_page.render()

if selected == "Uploads":
    upload_page = UploadsPage()
    upload_page.render()

if selected == "Planilha":
    st.title(f"You have selected {selected}")

if selected == "Dashboard":
    st.title(f"You have selected {selected}")