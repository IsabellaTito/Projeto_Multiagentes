import streamlit as st

hello_component = st.components.v2.component(
    name="hello_app",
    html="<center><h2>Financial Agents 🤖</center></h2>",
    css="h2 { color: var(--st-primary-color); }",
)