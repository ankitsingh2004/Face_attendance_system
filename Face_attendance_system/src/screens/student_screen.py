# import streamlit as st

# from src.ui.base_layout import style_background_deshboard, style_base_layout
# from src.components.header import header_dashboard
# from src.components.footer import footer_dashboard
# from src.database.db import check_teacher_exists, create_teacher, teacher_login

# import numpy as np
# from src.pipelines.face_pipelines import predict_attendance, get_face_embeddings ,train_classifier
# from PIL import Image

# from src.database.db import get_all_students ,create_student
# from src.pipelines.voice_pipeline import get_voice_embedding
# import time 



# def student_dashboard():
#      st.header('DASHBOARD HERE')



# def student_screen():

#    style_background_deshboard()
#    style_base_layout()


#    if "student_data" in st.session_state:
#         student_dashboard()




   
#    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
   
#    with c1:
#            header_dashboard()
#    with c2:
#            if st.button("Go back To Home", type="secondary", key="loginbackbtn"):
#                st.session_state["login_type"] = "home"
#                st.rerun()
   
#    st.header('Login using Face Id',text_alignment='center')
#    st.space()
#    st.space()

#    show_registration = False
#    photo_source = st.camera_input("Position your face in the Center")
#    if photo_source:
#         img = np.array(Image.open(photo_source))

#         with st.spinner('AI is scanning...'):
#               detected, all_ids, num_faces =  predict_attendance(img)


#               if num_faces ==0:
#                     st.warning('Face Not Found')
#               elif num_faces >1:
#                st.warning('Multile face found ')
#               else :
#                    if detected:
#                         student_id = list(detected.keys())[0]
#                         all_students = get_all_students()
#                         student = next((s for s in all_students if s['student_id'] ==student_id),None)

#                         if student:
#                              st.session_state.is_logged_in =True
#                              st.session_state.user_role ='student'
#                              st.session_state_data = student

#                              st.toast(f'Welcome Back{student['name']} ')
#                              time.sleep(1)

#                              st.rerun()

#                    else:
#                         # continue
#                         st.info('Face not recognized! You Might be a new student ')
#                         show_registration = True


#         if show_registration:
#                    with st.container(border =True):

#                     st.header('Register new Profile')
#                     new_name = st.text_input("Enter your name",placeholder='E.g. Alice')
#                     st.subheader('Optional : Voice Enrollment')
#                     st.info('Enroll your voice only attendance ')

#                    audio_data = None

#                    try:
#                         audio_data = st.audio_input('Record a short Phrase like I am Present,My name is Bob.')
#                    except Exception:
#                         st.error('Audio Data failed!')


#                    if st.button('Create Account',type='primary'):
#                         if new_name:
#                              with st.spinner('Creating Profile...'):
#                                   img = np.array(Image.open(photo_source))
#                                   encodings = get_face_embeddings(img)
#                                   if encodings:
#                                        face_emb = encodings[0].tolist()

#                                        voice_emb = None 

#                                        if audio_data:
#                                             voice_emb = get_voice_embedding(audio_data.read())

#                                             response_data = create_student(new_name,face_embeddings=face_emb,voice_embedding=voice_emb)

#                                             if response_data:
#                                                  train_classifier()
#                                                  st.session_state.is_logged_in =True
#                                                  st.session_state.user_role ='student'
#                                                  st.session_state_data = response_data[0]
                                                 
#                                                  st.toast(f'Profile Created! Hi {new_name} ')
#                                                  time.sleep(1)
#                                                  st.rerun()

#                                   else :
#                                         st.error('couldnt capture your facial features for Registration')
#                         else :
#                              st.warning('Please enter your name ')






#    footer_dashboard()
   














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
            st.session_state["is_logged_in"] = False
            st.session_state["current_teacher_tab"] = "take_attendance"
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
            sub = sub_node['subjects']
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
        header_dashboard()  # Displays the application header.

    with c2:
        if st.button("Go back To Home", type="secondary", key="loginbackbtn"):
            st.session_state["login_type"] = "home"  # Sets the screen to home.
            st.rerun()  # Refreshes the application.

    st.header('Login using Face Id', text_alignment='center')  # Displays the face login heading.
    st.space()
    st.space()

    show_registration = False
    photo_source = st.camera_input("Position your face in the Center")  # Captures the student's photo.

    if photo_source:
        img = np.array(Image.open(photo_source))  # Converts the photo into a NumPy array.

        with st.spinner('AI is scanning...'):
            detected, all_ids, num_faces = predict_attendance(img)  # Detects faces and checks attendance.

            if num_faces == 0:
                st.warning('Face Not Found')  # Shows a warning if no face is detected.

            elif num_faces > 1:
                st.warning('Multiple faces found')  # Requires only one face in the camera.

            else:
                if detected:
                    student_id = list(detected.keys())[0]  # Gets the recognized student's ID.
                    all_students = get_all_students()  # Fetches registered students from the database.
                    student = next((s for s in all_students if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True  # Marks the student as logged in.
                        st.session_state.user_role = 'student'  # Sets the user role.
                        st.session_state.student_data = student  # Stores the student's information.

                        st.toast(f"Welcome Back {student['name']}")  # Displays the welcome message.
                        time.sleep(1)
                        st.rerun()  # Opens the student dashboard.

                else:
                    st.info('Face not recognized! You might be a new student.')  # Offers registration.
                    show_registration = True

        if show_registration:
            with st.container(border=True):
                st.header('Register new Profile')  # Displays the registration form.
                new_name = st.text_input("Enter your name", placeholder='E.g. Alice')  # Gets the student's name.
                st.subheader('Optional: Voice Enrollment')
                st.info('Enroll your voice for voice-based attendance.')  # Explains optional voice enrollment.
                audio_data = st.audio_input('Record a short phrase like I am Present, My name is Bob.')  # Records voice.

                if st.button('Create Account', type='primary'):
                    if new_name:
                        with st.spinner('Creating Profile...'):
                            img = np.array(Image.open(photo_source))  # Reads the captured photo.
                            encodings = get_face_embeddings(img)  # Extracts facial features.

                            if encodings:
                                face_emb = encodings[0].tolist()  # Converts face features into a list.
                                voice_emb = None  # Keeps voice enrollment optional.

                                if audio_data:
                                    voice_emb = get_voice_embedding(audio_data.read())  # Extracts voice features.

                                response_data = create_student(
                                    new_name,
                                    face_embedding=face_emb,
                                    voice_embedding=voice_emb
                                )  # Saves student details and embeddings to Supabase.

                                if response_data:
                                    train_classifier()  # Trains the face recognition model.
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = 'student'
                                    st.session_state.student_data = response_data[0]  # Stores the new student's data.

                                    st.toast(f'Profile Created! Hi {new_name}')  # Confirms successful registration.
                                    time.sleep(1)
                                    st.rerun()  # Refreshes the app after registration.
                                else:
                                    st.error('Failed to create student profile.')  # Reports a database failure.
                            else:
                                st.error("Couldn't capture your facial features for registration.")  # Reports face extraction failure.
                    else:
                        st.warning('Please enter your name.')  # Requires a student name.

    footer_dashboard()  # Displays the page footer.
   