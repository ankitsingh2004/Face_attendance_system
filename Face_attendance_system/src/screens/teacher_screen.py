import streamlit as st
from src.ui.base_layout import style_background_deshboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard


def teacher_screen():
    style_background_deshboard()
    style_base_layout()

    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back To Home", type="secondary", key="loginbackbtn"):
            st.session_state["login_type"] = "home"
            st.rerun()

    st.header("Login using password", text_alignment="center")
    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="Rawatji",
        key="teacher_login_username"
    )

    teacher_pass = st.text_input(
        "Enter Password",
        type="password",
        placeholder="Enter password",
        key="teacher_login_password"
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button(
            "Login",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch",
            key="teacher_login_btn"
        ):
            if teacher_username and teacher_pass:
                st.info("Login authentication is not implemented yet.")
            else:
                st.warning("Please enter your username and password.")

    with btnc2:
        if st.button(
            "Register Instead",
            type="primary",
            icon=":material/person_add:",
            width="stretch",
            key="teacher_register_btn"
        ):
            st.session_state["teacher_login_type"] = "register"
            st.rerun()

    footer_dashboard()


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back To Home",
            type="secondary",
            key="registerbackbtn"
        ):
            st.session_state["login_type"] = "home"
            st.rerun()

    st.header("Register your teacher profile", text_alignment="center")
    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="Rawatji",
        key="teacher_register_username"
    )

    teacher_name = st.text_input(
        "Enter Name",
        placeholder="Rawat",
        key="teacher_register_name"
    )

    teacher_pass = st.text_input(
        "Enter Password",
        type="password",
        placeholder="Create a password",
        key="teacher_register_password"
    )

    teacher_pass_confirm = st.text_input(
        "Confirm your password",
        type="password",
        placeholder="Confirm your password",
        key="teacher_register_password_confirm"
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button(
            "Register",
            type="primary",
            icon=":material/person_add:",
            width="stretch",
            key="teacher_register_submit"
        ):
            if teacher_username and teacher_name and teacher_pass and teacher_pass_confirm:
                st.info("Teacher registration logic is not implemented yet.")
            else:
                st.warning("Please fill in all fields.")

    with btnc2:
        if st.button(
            "Login Instead",
            icon=":material/passkey:",
            width="stretch",
            key="teacher_login_instead"
        ):
            st.session_state["teacher_login_type"] = "login"
            st.rerun()

    footer_dashboard()