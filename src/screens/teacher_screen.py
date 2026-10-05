import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login
)


# =========================================================
# TEACHER SCREEN
# =========================================================

def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    # If teacher is already logged in
    if "teacher_data" in st.session_state:
        teacher_dashboard()

    # Otherwise show login/register screen
    elif (
        "teacher_login_type" not in st.session_state
        or st.session_state["teacher_login_type"] == "login"
    ):
        teacher_screen_login()

    elif st.session_state["teacher_login_type"] == "register":
        teacher_screen_register()


# =========================================================
# TEACHER DASHBOARD
# =========================================================

def teacher_dashboard():

    # IMPORTANT:
    # Initialize the dashboard tab before using it
    if "current_teacher_tab" not in st.session_state:
        st.session_state["current_teacher_tab"] = "attendance_records"

    teacher_data = st.session_state["teacher_data"]

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:

        st.subheader(
            f"Welcome, {teacher_data['name']}"
        )

        if st.button(
            "LogOut",
            type="secondary",
            key="teacher_logout_btn"
        ):

            # Remove teacher information
            st.session_state.pop("teacher_data", None)

            # Reset login status
            st.session_state["is_logged_in"] = False

            # Reset dashboard tab
            st.session_state["current_teacher_tab"] = "attendance_records"

            # Go back
            st.rerun()

    st.space()

    # -----------------------------------------------------
    # DASHBOARD TABS
    # -----------------------------------------------------

    tab1, tab2, tab3 = st.columns(
        [1, 1, 1]
    )

    # -----------------------------------------------------
    # TAKE ATTENDANCE
    # -----------------------------------------------------

    with tab1:

        if st.session_state["current_teacher_tab"] == "take_attendance":
            button_type = "primary"
        else:
            button_type = "tertiary"

        if st.button(
            "Take Attendance",
            type=button_type,
            width="stretch",
            icon=":material/ar_on_you:",
            key="take_attendance_btn"
        ):

            st.session_state["current_teacher_tab"] = "take_attendance"

            st.rerun()

    # -----------------------------------------------------
    # MANAGE SUBJECTS
    # -----------------------------------------------------

    with tab2:

        if st.session_state["current_teacher_tab"] == "manage_subjects":
            button_type = "primary"
        else:
            button_type = "tertiary"

        if st.button(
            "Manage Subjects",
            type=button_type,
            width="stretch",
            icon=":material/book_ribbon:",
            key="manage_subjects_btn"
        ):

            st.session_state["current_teacher_tab"] = "manage_subjects"

            st.rerun()

    # -----------------------------------------------------
    # ATTENDANCE RECORDS
    # -----------------------------------------------------

    with tab3:

        if st.session_state["current_teacher_tab"] == "attendance_records":
            button_type = "primary"
        else:
            button_type = "tertiary"

        if st.button(
            "Attendance Records",
            type=button_type,
            width="stretch",
            icon=":material/cards_stack:",
            key="attendance_records_btn"
        ):

            st.session_state["current_teacher_tab"] = "attendance_records"

            st.rerun()

    st.divider()

    # -----------------------------------------------------
    # SHOW SELECTED TAB
    # -----------------------------------------------------

    current_tab = st.session_state["current_teacher_tab"]

    if current_tab == "take_attendance":

        teacher_tab_take_attendance()

    elif current_tab == "manage_subjects":

        teacher_tab_manage_subjects()

    elif current_tab == "attendance_records":

        teacher_tab_attendance_records()

    else:

        # Safety fallback
        st.session_state["current_teacher_tab"] = "attendance_records"

        teacher_tab_attendance_records()

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    footer_dashboard()


# =========================================================
# TAKE ATTENDANCE TAB
# =========================================================

def teacher_tab_take_attendance():

    st.header("Take AI Attendance")


# =========================================================
# MANAGE SUBJECTS TAB
# =========================================================

def teacher_tab_manage_subjects():

    st.header("Manage Subjects")


# =========================================================
# ATTENDANCE RECORDS TAB
# =========================================================

def teacher_tab_attendance_records():

    st.header("Attendance Records")


# =========================================================
# TEACHER LOGIN FUNCTION
# =========================================================

def login_teacher(username, password):

    if not username or not password:
        return False

    teacher = teacher_login(
        username,
        password
    )

    if teacher:

        st.session_state["user_role"] = "teacher"

        st.session_state["teacher_data"] = teacher

        st.session_state["is_logged_in"] = True

        # Initialize dashboard tab
        st.session_state["current_teacher_tab"] = "attendance_records"

        return True

    return False


# =========================================================
# TEACHER LOGIN SCREEN
# =========================================================

def teacher_screen_login():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    # -----------------------------------------------------
    # LEFT SIDE
    # -----------------------------------------------------

    with c1:

        header_dashboard()

    # -----------------------------------------------------
    # RIGHT SIDE
    # -----------------------------------------------------

    with c2:

        if st.button(
            "Go back to home",
            type="secondary",
            key="teacher_login_back_btn"
        ):

            st.session_state["login_type"] = None

            st.rerun()

    st.header(
        "Login using password",
        text_alignment="center"
    )

    st.space()
    st.space()

    # -----------------------------------------------------
    # USERNAME
    # -----------------------------------------------------

    teacher_username = st.text_input(
        "Enter username",
        placeholder="RajSahana",
        key="teacher_username_login"
    )

    # -----------------------------------------------------
    # PASSWORD
    # -----------------------------------------------------

    teacher_pass = st.text_input(
        "Enter Password",
        type="password",
        placeholder="Enter password",
        key="teacher_password_login"
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    # -----------------------------------------------------
    # LOGIN BUTTON
    # -----------------------------------------------------

    with btnc1:

        if st.button(
            "Login",
            icon=":material/passkey:",
            width="stretch",
            key="teacher_login_btn"
        ):

            if login_teacher(
                teacher_username,
                teacher_pass
            ):

                st.toast(
                    "Welcome back!",
                    icon="👋"
                )

                import time
                time.sleep(1)

                st.rerun()

            else:

                st.error(
                    "Invalid username and password combo"
                )

    # -----------------------------------------------------
    # REGISTER BUTTON
    # -----------------------------------------------------

    with btnc2:

        if st.button(
            "Register Instead",
            type="primary",
            icon=":material/passkey:",
            width="stretch",
            key="teacher_register_btn"
        ):

            st.session_state["teacher_login_type"] = "register"

            st.rerun()

    footer_dashboard()


# =========================================================
# REGISTER TEACHER FUNCTION
# =========================================================

def register_teacher(
    teacher_username,
    teacher_name,
    teacher_pass,
    teacher_pass_confirm
):

    # Check empty fields
    if (
        not teacher_username
        or not teacher_name
        or not teacher_pass
        or not teacher_pass_confirm
    ):

        return False, "All fields are required!"

    # Check username
    if check_teacher_exists(teacher_username):

        return False, "Username already taken"

    # Check password
    if teacher_pass != teacher_pass_confirm:

        return False, "Password doesn't match"

    try:

        create_teacher(
            teacher_username,
            teacher_pass,
            teacher_name
        )

        return True, "Successfully Created! Login Now"

    except Exception as e:

        return False, f"Unexpected Error: {e}"


# =========================================================
# TEACHER REGISTER SCREEN
# =========================================================

def teacher_screen_register():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    # -----------------------------------------------------
    # LEFT SIDE
    # -----------------------------------------------------

    with c1:

        header_dashboard()

    # -----------------------------------------------------
    # RIGHT SIDE
    # -----------------------------------------------------

    with c2:

        if st.button(
            "Go back to home",
            type="secondary",
            key="teacher_register_back_btn"
        ):

            st.session_state["teacher_login_type"] = "login"

            st.rerun()

    st.header(
        "Register your teacher profile"
    )

    st.space()
    st.space()

    # -----------------------------------------------------
    # USERNAME
    # -----------------------------------------------------

    teacher_username = st.text_input(
        "Enter username",
        placeholder="RajSahana",
        key="teacher_username_register"
    )

    # -----------------------------------------------------
    # NAME
    # -----------------------------------------------------

    teacher_name = st.text_input(
        "Enter name",
        placeholder="RajSahana",
        key="teacher_name_register"
    )

    # -----------------------------------------------------
    # PASSWORD
    # -----------------------------------------------------

    teacher_pass = st.text_input(
        "Enter Password",
        type="password",
        placeholder="Enter password",
        key="teacher_password_register"
    )

    # -----------------------------------------------------
    # CONFIRM PASSWORD
    # -----------------------------------------------------

    teacher_pass_confirm = st.text_input(
        "Confirm your password",
        type="password",
        placeholder="Enter password",
        key="teacher_password_confirm_register"
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    # -----------------------------------------------------
    # REGISTER BUTTON
    # -----------------------------------------------------

    with btnc1:

        if st.button(
            "Register now",
            icon=":material/passkey:",
            width="stretch",
            key="teacher_register_now_btn"
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

    # -----------------------------------------------------
    # LOGIN INSTEAD BUTTON
    # -----------------------------------------------------

    with btnc2:

        if st.button(
            "Login Instead",
            type="primary",
            icon=":material/passkey:",
            width="stretch",
            key="teacher_login_instead_btn"
        ):

            st.session_state["teacher_login_type"] = "login"

            st.rerun()

    footer_dashboard()