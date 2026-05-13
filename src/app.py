import streamlit as st

from screens import ChatPage, UploadsPage, SheetPage, LoginPage
from shared.utils import init_session, init_sidebar

st.set_page_config(
    page_title="Financial Agents",
    page_icon="resources/assets/cash-coin.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "page_status" not in st.session_state:
    st.session_state.page_status = "Not Logged"

if st.session_state.page_status == "Logged":

    selected = init_sidebar()

    session = init_session()

    if selected == "Chat":
        chat_page = ChatPage(session)
        chat_page.render()

    elif selected == "Uploads":
        upload_page = UploadsPage()
        upload_page.render()

    elif selected == "Planilha":
        sheet_page = SheetPage(session)
        sheet_page.render()

    elif selected == "Dashboard":
        st.title(f"You have selected {selected}")
    
    elif selected == "Log Out":
        st.session_state.page_status = "Not Logged"
        st.rerun()

else:

    login_page = LoginPage()
    login_page.render()