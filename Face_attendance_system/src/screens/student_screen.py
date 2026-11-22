
import streamlit as st
import numpy as np
import time

from PIL import Image
from src.ui.base_layout import style_background_deshboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
from src.pipelines.face_pipelines import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    # Displays the student dashboard.
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    st.subheader(f"Welcome, {student_data['name']}")

    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button("Logout", type="secondary", key="student_logout_btn"):
            st.session_state.pop("student_data", None)
            st.session_state.pop("user_role", None)
            st.session_state.pop("last_photo", None)
            st.session_state.pop("scan_result", None)
            st.session_state.pop("scan_error", None)
            st.session_state["is_logged_in"] = False
            st.rerun()

    st.space()

    c1, c2 = st.columns(2)
    with c1:
        st.header("Your Enrolled Subjects")
    with c2:
        if st.button("Enroll in Subject", type='primary', width='stretch'):
            enroll_dialog()
    st.divider()

    with st.spinner('Loading your enrolled Subjects...'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

        stats_map = {}

        for log in logs:
            sid = log['subject_id']

            if sid not in stats_map:
                stats_map[sid] = {"total": 0, "attended": 0}

            stats_map[sid]['total'] += 1
            if log.get('is_present'):
                stats_map[sid]['attended'] += 1

        cols = st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node.get('subjects')
            if not sub:
                continue  # subject was deleted

            sid = sub['subject_id']
            stats = stats_map.get(sid, {"total": 0, "attended": 0})

            def unenroll_btn(sid=sid, name=sub['name']):
                if st.button("Unenroll from this course", type='tertiary', width='stretch',
                             icon=':material/delete_forever:', key=f"unenroll_{sid}"):
                    unenroll_student_to_subject(student_id, sid)
                    st.toast(f"UnEnrolled from {name} successfully!")
                    st.rerun()

            with cols[i % 2]:
                subject_card(
                    name=sub['name'],
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=[
                        ('🗓️', 'Total', stats['total']),
                        ('☑️', 'Attended', stats['attended']),
                    ],
                    footer_callback=unenroll_btn
                )

    footer_dashboard()


def student_screen():
    style_background_deshboard()  # Applies the dashboard background.
    style_base_layout()  # Applies the base layout styling.

    if "student_data" in st.session_state:
        student_dashboard()  # Opens the dashboard for a logged-in student.
        return

    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back To Home", type="secondary", key="loginbackbtn"):
            st.session_state["login_type"] = "home"
            st.rerun()

    st.header('Login using Face Id', text_alignment='center')
    st.space()
    st.space()

    photo_source = st.camera_input("Position your face in the Center")

    if photo_source:
        photo_bytes = photo_source.getvalue()

        # Scan only when the photo changes, not on every click or keystroke
        if st.session_state.get("last_photo") != photo_bytes:
            st.session_state["last_photo"] = photo_bytes
            st.session_state.pop("scan_error", None)
            img = np.array(Image.open(photo_source).convert("RGB"))

            try:
                with st.spinner('AI is scanning...'):
                    st.session_state["scan_result"] = predict_attendance(img)
            except Exception as e:
                # Treat as an unknown face so registration is still possible
                st.session_state["scan_result"] = ({}, [], 1)
                st.session_state["scan_error"] = str(e)

        detected, all_ids, num_faces = st.session_state["scan_result"]

        if num_faces == 0:
            st.warning('Face Not Found')

        elif num_faces > 1:
            st.warning('Multiple faces found')

        elif detected:
            student_id = list(detected.keys())[0]
            student = next((s for s in get_all_students() if s['student_id'] == student_id), None)

            if student:
                st.session_state.is_logged_in = True
                st.session_state.user_role = 'student'
                st.session_state.student_data = student

                st.toast(f"Welcome Back {student['name']}")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Face recognized but profile not found. Please contact your teacher.")

        else:
            st.info('Face not recognized! You might be a new student.')
            if st.session_state.get("scan_error"):
                st.caption(f"Scan note: {st.session_state['scan_error']}")

            with st.container(border=True):
                st.header('Register new Profile')
                new_name = st.text_input("Enter your name", placeholder='E.g. Alice').strip()

                st.subheader('Optional: Voice Enrollment')
                st.info('Enroll your voice for voice-based attendance.')
                audio_data = st.audio_input('Record a short phrase like I am Present, My name is Bob.')

                if st.button('Create Account', type='primary'):
                    if not new_name:
                        st.warning('Please enter your name.')
                    else:
                        try:
                            with st.spinner('Creating Profile...'):
                                img = np.array(Image.open(photo_source).convert("RGB"))
                                encodings = get_face_embeddings(img)

                                if not encodings:
                                    st.error("Couldn't read your face. Retake the photo in good light.")
                                    st.stop()

                                voice_emb = None
                                if audio_data:
                                    voice_emb = get_voice_embedding(audio_data.read())

                                response_data = create_student(
                                    new_name,
                                    face_embedding=encodings[0].tolist(),
                                    voice_embedding=voice_emb
                                )

                                if not response_data:
                                    st.error('Database did not save the profile (check Supabase insert / RLS policy).')
                                    st.stop()

                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]

                                st.toast(f'Profile Created! Hi {new_name}')
                                time.sleep(1)
                                st.rerun()
                        except Exception as e:
                            st.exception(e)  # shows the real error on the page

    footer_dashboard()









