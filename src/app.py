import streamlit as st
from streamlit_extras.avatar import *
from streamlit_option_menu import option_menu

from screens.chat import ChatPage
from screens.uploads import UploadsPage

st.set_page_config(layout="centered")

with st.sidebar:
    selected = option_menu(
        menu_title="Assistente",  # required
        options=["Chat", "Uploads", "Planilha", "Dashboard"],  # required
        icons=["chat-right-text-fill", "file-earmark-arrow-up-fill", "table", "clipboard-data-fill"],  # optional
        menu_icon=None, #"cast",  # optional
        default_index=0,  # optional
        #orientation="horizontal",
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