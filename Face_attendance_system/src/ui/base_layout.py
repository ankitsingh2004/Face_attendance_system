# import streamlit as st


# def style_background_home():
#     st.markdown("""
#     <style>
#     .stApp {
#         background: #5865F2 !important;
#     }

#     div[data-testid="stColumn"] {
#         background: #E0E3FF !important;
#         padding: 1rem !important;
#         border-radius: 1rem !important;
#     }
#     </style>
#     """, unsafe_allow_html=True)


# def style_background_deshboard():
#     st.markdown("""
#     <style>
#     .stApp {
#         background: #E0E3FF !important;
#     }
#     </style>
#     """, unsafe_allow_html=True)


# def style_base_layout():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&display=swap');
#     @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

#     /* Hide Streamlit menu and header */
#     #MainMenu, footer, header {
#         visibility: hidden;
#     }

#     /* Main container spacing */
#     .block-container {
#         padding-top: 1.5rem !important;
#     }

#     /* Heading styles */
#     h1, h2 {
#         font-family: 'Climate Crisis', sans-serif !important;
#         font-size: 2rem !important;
#         line-height: 1 !important;
#     }

#     /* General text */
#     h3, h4, p, label {
#         font-family: 'Outfit', sans-serif !important;
#     }

#     /* Primary buttons */
#     button[kind="primary"] {
#         border-radius: 1.5rem !important;
#         background: #5865F2 !important;
#         color: white !important;
#         padding: 10px 20px !important;
#         border: none !important;
#     }

#     /* Secondary buttons */
#     button[kind="secondary"] {
#         border-radius: 1.5rem !important;
#         background: #EB459E !important;
#         color: white !important;
#         padding: 10px 20px !important;
#         border: none !important;
#     }

#     /* Button hover effect */
#     button:hover {
#         transform: scale(1.02);
#     }
#     </style>
#     """, unsafe_allow_html=True)



import streamlit as st


def style_background_home():
    st.markdown("""
    <style>
    .stApp {
        background: #5865F2 !important;
    }

    div[data-testid="stColumn"] {
        background: #E0E3FF !important;
        padding: 1rem !important;
        border-radius: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)


def style_background_deshboard():
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

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1.5rem !important;
    }

    h1, h2 {
        font-family: 'Climate Crisis', sans-serif !important;
        line-height: 1.15 !important;
    }

    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }

    h3, h4, p, label, button {
        font-family: 'Outfit', sans-serif !important;
    }

    button[kind="primary"] {
        background: #5865F2 !important;
        color: white !important;
        border: none !important;
        border-radius: 1.5rem !important;
        padding: 10px 20px !important;
    }

    button[kind="secondary"] {
        background: #EB2997 !important;
        color: white !important;
        border: none !important;
        border-radius: 1.5rem !important;
        padding: 10px 20px !important;
    }

    button[kind="tertiary"] {
        background: black !important;
        color: white !important;
        border: none !important;
        border-radius: 1.5rem !important;
        padding: 10px 20px !important;
    }

    button:hover {
        filter: brightness(1.1);
        transform: scale(1.02);
        transition: all 0.2s ease;
    }
    </style>
    """, unsafe_allow_html=True)