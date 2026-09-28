import streamlit as st


def show_student_management_page(manager):
    """Renders student searching and registration controls."""
    st.header("Student Management")

    st.subheader("Find a Student")
    search_term = st.text_input(
        "Search by student name",
        placeholder="Enter all or part of a name"
    )

    matching_students = manager.search_students(search_term)
    student_records = []

    for student in matching_students:
        course_names = []

        for course_id in student.enrolled_course_ids:
            course = manager.find_course_by_id(course_id)

            if course is not None:
                course_names.append(course.name)

        student_records.append({
            "Student ID": student.id,
            "Name": student.name,
            "Enrolled Courses": ", ".join(course_names) or "None"
        })

    if student_records:
        st.dataframe(
            student_records,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No students matched your search.")

    st.divider()
    st.subheader("Register New Student")

    available_instruments = []

    for course in manager.courses:
        teacher = manager.find_teacher_by_id(course.teacher_id)

        if teacher is not None and course.instrument not in available_instruments:
            available_instruments.append(course.instrument)

    available_instruments.sort()
    
    if not available_instruments:
        st.warning(
            "Registration is unavailable because no courses have "
            "an assigned teacher."
        )
        return

    with st.form("registration_form", clear_on_submit=True):
        student_name = st.text_input("New Student Name")
        selected_instrument = st.selectbox(
            "First Instrument",
            available_instruments
        )

        submitted = st.form_submit_button("Register Student")

        if submitted:
            new_student = manager.register_new_student(
                student_name,
                selected_instrument
            )

            if new_student is not None:
                st.success(
                    f"Registered {new_student.name} with student ID "
                    f"{new_student.id}."
                )
            elif not student_name.strip():
                st.warning("Please enter the student's name.")
            else:
                st.error(
                    "Registration failed. The student may already exist, "
                    "or no suitable course and teacher are available."
                )