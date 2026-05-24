import streamlit as st

def apply_style():

    st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }

    h1, h2, h3 {
        color: #00C2A8;
    }

    .stMetric {
        background-color: #111827;
        border-radius: 10px;
        padding: 10px;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }
    </style>
    """, unsafe_allow_html=True)