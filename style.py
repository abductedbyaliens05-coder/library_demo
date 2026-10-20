import streamlit as st

def apply_style(title):
    st.set_page_config(page_title='Library Management System', layout='wide')
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    h1 {font-weight: 500; letter-spacing: 0.5px;
        border-bottom: 1px solid #B08D57; padding-bottom: 0.4rem;}
    h2, h3 {font-weight: 500;}
    </style>
    """, unsafe_allow_html=True)
    st.title(title)
