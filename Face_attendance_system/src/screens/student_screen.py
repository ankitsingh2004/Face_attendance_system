import streamlit as st

from src.ui.base_layout import style_background_deshboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login

import numpy as np

from PIL import Image

def student_screen():

   style_background_deshboard()
   style_base_layout()
   
   c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
   
   with c1:
           header_dashboard()
   with c2:
           if st.button("Go back To Home", type="secondary", key="loginbackbtn"):
               st.session_state["login_type"] = "home"
               st.rerun()
   
   st.header('Login using Face Id',text_alignment='center')
   st.space()
   st.space()
   photo_source = st.camera_input("Position your face in the Center")
   if photo_source:
         np.array(Image.open(photo_source))

   footer_dashboard()
   
   