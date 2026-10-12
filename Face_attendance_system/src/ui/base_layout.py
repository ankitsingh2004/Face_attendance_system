import streamlit as st


def style_baackground_home():
    st.markdown("""
    <style>
    .stApp {
        background: #5865F2 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def style_baackground_deshboard():
    st.markdown("""
    <style>
    .stApp {
        background: #E0E3FF !important;
    }
    </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

    /* Hide Streamlit top menu and header */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Main container spacing */
    .block-container {
        padding-top: 1.5rem !important;
    }

    /* Heading styles */
    h1, h2 {
        font-family: 'Climate Crisis', sans-serif !important;
        font-size: 3.5rem !important;
        line-height: 1.1 !important;
        margin-bottom: 0rem !important;
    }

    /* General text */
    h3, h4, p, label {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Primary buttons */
    button[kind="primary"] {
        border-radius: 1.5rem !important;
        background: #5865F2 !important;
        color: white !important;
        padding: 10px 20px !important;
        border: none !important;
        transition: transform 0.25s ease-in-out !important;
    }

    /* Secondary buttons */
    button[kind="secondary"] {
        border-radius: 1.5rem !important;
        background: #EB459E !important;
        color: white !important;
        padding: 10px 20px !important;
        border: none !important;
        transition: transform 0.25s ease-in-out !important;
    }

    /* Hover effect */
    button:hover {
        transform: scale(1.05);
    }

    </style>
    """, unsafe_allow_html=True)