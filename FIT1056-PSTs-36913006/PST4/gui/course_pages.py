import streamlit as st


def show_course_management_page(manager):
    """Displays courses and allows a student to switch courses."""
    st.header("Course Management")

    course_records = []

    for course in manager.courses:
        teacher = manager.find_teacher_by_id(course.teacher_id)

        if teacher is None:
            teacher_name = "Unassigned"
        else:
            teacher_name = teacher.name

        course_records.append({
            "Course ID": course.id,
            "Course": course.name,
            "Instrument": course.instrument,
            "Teacher": teacher_name,
            "Enrolled Students": len(course.enrolled_student_ids)
        })

    if course_records:
        st.dataframe(
            course_records,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No courses are currently available.")

    st.divider()
    st.subheader("Switch Student Course")

    student_options = {
        f"{student.name} (ID: {student.id})": student.id
        for student in manager.students
    }

    if not student_options:
        st.warning("No students are available.")
        return

    selected_student_label = st.selectbox(
        "Select Student",
        student_options.keys()
    )

    student = manager.find_student_by_id(
        student_options[selected_student_label]
    )

    current_courses = []

    for course_id in student.enrolled_course_ids:
        course = manager.find_course_by_id(course_id)

        if course is not None:
            current_courses.append(course)

    available_courses = [
        course
        for course in manager.courses
        if course.id not in student.enrolled_course_ids
    ]

    if not current_courses:
        st.warning("This student is not enrolled in any courses.")
        return

    if not available_courses:
        st.info("This student is already enrolled in every course.")
        return

    current_course_options = {
        f"{course.name} (ID: {course.id})": course.id
        for course in current_courses
    }

    new_course_options = {
        f"{course.name} (ID: {course.id})": course.id
        for course in available_courses
    }

    with st.form("course_switch_form"):
        current_course_label = st.selectbox(
            "Current Course",
            current_course_options.keys()
        )

        new_course_label = st.selectbox(
            "New Course",
            new_course_options.keys()
        )

        submitted = st.form_submit_button("Switch Course")

        if submitted:
            success = manager.switch_course(
                student.id,
                current_course_options[current_course_label],
                new_course_options[new_course_label]
            )

            if success:
                st.success(
                    f"Switched {student.name} from "
                    f"{current_course_label} to {new_course_label}."
                )
            else:
                st.error("Course switch failed. Please verify the records.")