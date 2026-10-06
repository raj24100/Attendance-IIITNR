import streamlit as st
import time
import numpy as np

from PIL import Image

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier
)

from src.pipelines.voice_pipeline import get_voice_embedding

from src.database.db import get_all_students


def student_dashboard():
    st.header("DASHBOARD HERE")


def student_screen():

    # Apply page styling
    style_background_dashboard()
    style_base_layout()

    # --------------------------------------------------
    # If student is already logged in
    # --------------------------------------------------
    if "student_data" in st.session_state:
        student_dashboard()
        return

    # --------------------------------------------------
    # Header and Back Button
    # --------------------------------------------------
    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="large"
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to home",
            type="secondary",
            key="loginbackbtn"
        ):
            st.session_state["login_type"] = None
            st.rerun()

    # --------------------------------------------------
    # Face Login
    # --------------------------------------------------
    st.header(
        "Login using FaceID",
        text_alignment="center"
    )

    st.space()
    st.space()

    show_registration = False

    photo_source = st.camera_input(
        "Position your face in the center"
    )

    # --------------------------------------------------
    # Face Recognition
    # --------------------------------------------------
    if photo_source:

        img = np.array(
            Image.open(photo_source)
        )

        with st.spinner("AI is scanning..."):

            try:
                detected, all_ids, num_faces = predict_attendance(img)

            except Exception as e:
                st.error(
                    f"Face recognition failed: {e}"
                )
                detected = None
                num_faces = 0

            # No face
            if num_faces == 0:
                st.warning("Face not found!")

            # Multiple faces
            elif num_faces > 1:
                st.warning(
                    "Multiple faces found. Please keep only one face in the camera."
                )

            # Exactly one face
            else:

                if detected:

                    student_id = list(
                        detected.keys()
                    )[0]

                    try:
                        all_students = get_all_students()

                        student = next(
                            (
                                s for s in all_students
                                if s.get("student_id") == student_id
                            ),
                            None
                        )

                    except Exception as e:
                        st.error(
                            f"Unable to load student data: {e}"
                        )
                        student = None

                    if student:

                        st.session_state["is_logged_in"] = True
                        st.session_state["user_role"] = "student"
                        st.session_state["student_data"] = student

                        st.toast(
                            f"Welcome back {student.get('name', 'Student')}!"
                        )

                        time.sleep(1)

                        st.rerun()

                    else:
                        st.warning(
                            "Student was recognized, but student details were not found in the database."
                        )

                else:

                    st.info(
                        "Face not recognized! You might be a new student."
                    )

                    show_registration = True

    # --------------------------------------------------
    # New Student Registration
    # --------------------------------------------------
    if show_registration:

        with st.container(border=True):

            st.header("Registration New Profile")

            new_name = st.text_input(
                "Enter your name",
                placeholder="E.g. Raj Sahana"
            )

            st.subheader(
                "Optional: Voice Enrollment"
            )

            st.info(
                "Enroll your voice for voice-only attendance."
            )

            audio_data = None

            try:

                audio_data = st.audio_input(
                    "Record a short phrase like: I am present, My name is Raj."
                )

            except Exception as e:

                st.warning(
                    f"Audio recording is unavailable: {e}"
                )

            # --------------------------------------------------
            # Create Account Button
            # --------------------------------------------------
            if st.button(
                "Create Account",
                type="primary",
                key="create_student_btn"
            ):

                if not new_name.strip():

                    st.warning(
                        "Please enter your name!"
                    )

                elif photo_source is None:

                    st.warning(
                        "Please capture your face first!"
                    )

                else:

                    with st.spinner(
                        "Creating profile..."
                    ):

                        try:

                            # Get face embedding
                            img = np.array(
                                Image.open(photo_source)
                            )

                            encodings = get_face_embeddings(
                                img
                            )

                            if not encodings:

                                st.error(
                                    "Couldn't capture your facial features for registration."
                                )

                            else:

                                face_emb = encodings[0].tolist()

                                # Get voice embedding
                                voice_emb = None

                                if audio_data:

                                    try:

                                        voice_emb = get_voice_embedding(
                                            audio_data.read()
                                        )

                                    except Exception as e:

                                        st.warning(
                                            f"Voice enrollment failed: {e}"
                                        )

                                # --------------------------------------------------
                                # IMPORTANT
                                # --------------------------------------------------
                                # Your original code used create_student().
                                #
                                # That function does not currently exist in db.py.
                                #
                                # Therefore registration cannot be completed
                                # until create_student() is added to db.py.
                                # --------------------------------------------------

                                st.error(
                                    "Registration cannot be completed because "
                                    "`create_student()` is missing from "
                                    "`src/database/db.py`."
                                )

                                st.info(
                                    "Your FaceID login code is ready. "
                                    "Please add the `create_student()` function "
                                    "to db.py before using registration."
                                )

                        except Exception as e:

                            st.error(
                                f"Registration failed: {e}"
                            )

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------
    footer_dashboard()