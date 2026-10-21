
import streamlit as st
from src.ui.base_layout import style_background_deshboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login


def teacher_screen():
    style_background_deshboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()

    elif (
        "teacher_login_type" not in st.session_state
        or st.session_state.teacher_login_type == "login"
    ):
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    st.header(f"Welcome, {teacher_data['name']}")


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

    return False


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
            if not teacher_username or not teacher_pass:
                st.error("Please enter username and password.")
            elif login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome Back!", icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password combination.")

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


def register_teacher(
    teacher_username,
    teacher_name,
    teacher_pass,
    teacher_pass_confirm
):
    if not all([
        teacher_username.strip(),
        teacher_name.strip(),
        teacher_pass,
        teacher_pass_confirm
    ]):
        return False, "All fields are required!"

    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."

    try:
        if check_teacher_exists(teacher_username.strip()):
            return False, "Username already taken."

        create_teacher(
            teacher_username.strip(),
            teacher_pass,
            teacher_name.strip()
        )

        return True, "Account created successfully. Please log in."

    except Exception:
        return False, "Unexpected error occurred. Please try again."


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
            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_pass,
                teacher_pass_confirm
            )

            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state["teacher_login_type"] = "login"
                st.rerun()
            else:
                st.error(message)

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
