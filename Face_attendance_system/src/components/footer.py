import streamlit as st

def footer_home():
    st.markdown("""
        <div style="margin-top:2rem; display:flex; gap:6px;
                    justify-content:center; align-items:center;">
            <p>Created with ❤️ by Ankit Singh</p>
        </div>
        <div style="text-align:center; font-size:12px; color:gray;">
            © 2026 Ankit Singh. All rights reserved.
        </div>
    """, unsafe_allow_html=True)