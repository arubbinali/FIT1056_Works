import streamlit as st

from app.schedule import ScheduleManager
from gui.course_pages import show_course_management_page
from gui.roster_pages import show_roster_page
from gui.student_pages import show_student_management_page


def show_overview(manager):
    """Displays a summary of the music school records."""
    st.title("Music School Management System")
    st.write(
        "Use the navigation menu to manage students, courses, "
        "daily lessons, and attendance."
    )

    students_column, teachers_column, courses_column, attendance_column = (
        st.columns(4)
    )

    students_column.metric("Students", len(manager.students))
    teachers_column.metric("Teachers", len(manager.teachers))
    courses_column.metric("Courses", len(manager.courses))
    attendance_column.metric(
        "Attendance Records",
        len(manager.attendance_log)
    )


def launch():
    """Sets up the Streamlit application and page navigation."""
    st.set_page_config(
        layout="wide",
        page_title="Music School Management System"
    )

    if "manager" not in st.session_state:
        st.session_state.manager = ScheduleManager()

    manager = st.session_state.manager

    st.sidebar.title("MSMS Navigation")
    page = st.sidebar.radio(
        "Go to",
        [
            "Overview",
            "Student Management",
            "Daily Roster",
            "Course Management"
        ]
    )

    if page == "Overview":
        show_overview(manager)
    elif page == "Student Management":
        show_student_management_page(manager)
    elif page == "Daily Roster":
        show_roster_page(manager)
    elif page == "Course Management":
        show_course_management_page(manager)