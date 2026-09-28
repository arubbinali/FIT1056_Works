import pandas as pd
import streamlit as st


def show_roster_page(manager):
    """Renders the daily roster and student check-in controls."""
    st.header("Daily Roster")

    day = st.selectbox(
        "Select a day",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]
    )

    roster = manager.get_daily_roster(day)

    if roster:
        roster_table = pd.DataFrame(roster)
        roster_table = roster_table.rename(columns={
            "start_time": "Time",
            "course_name": "Course",
            "teacher_name": "Teacher",
            "room": "Room"
        })

        st.dataframe(
            roster_table,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(f"No lessons are scheduled for {day}.")

    st.divider()
    st.subheader("Student Check-in")

    student_options = {
        f"{student.name} (ID: {student.id})": student.id
        for student in manager.students
    }

    course_options = {
        f"{course.name} (ID: {course.id})": course.id
        for course in manager.courses
    }

    if not student_options or not course_options:
        st.warning(
            "At least one student and one course are required "
            "before check-in can be used."
        )
        return

    with st.form("check_in_form", clear_on_submit=True):
        selected_student = st.selectbox(
            "Select Student",
            student_options.keys()
        )

        selected_course = st.selectbox(
            "Select Course",
            course_options.keys()
        )

        submitted = st.form_submit_button("Check-in Student")

        if submitted:
            student_id = student_options[selected_student]
            course_id = course_options[selected_course]

            success = manager.check_in(student_id, course_id)

            if success:
                st.success(
                    f"Checked in {selected_student} for "
                    f"{selected_course}."
                )
            else:
                st.error("Check-in failed. Please verify the records.")