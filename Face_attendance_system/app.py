import streamlit as st

def main():
    st.header("This is Title")
    name = st.text_input('Enter Your Name')

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Hi', type='primary', key='btn1', width='stretch'):
            print('hi', name)

    with col2:
        if st.button('Bye', type='secondary', key='btn2', width='stretch'):  # Easy for Identification
            print('bye', name)


st.markdown("""
    <style>
    button {
        background: orange !important;
    }
    </style>

    <div>
        <img src="https://i.ibb.co/YTYGn5qV/logo.png"/>
        <h1>Snap Class</h1>
    </div>
""", unsafe_allow_html=True)

main()