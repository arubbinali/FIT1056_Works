from app.schedule import ScheduleManager


def front_desk_daily_roster(manager, day):
    """Displays all lessons scheduled for a given day."""
    roster = manager.get_daily_roster(day)

    print(f"\n--- Daily Roster for {day.title()} ---")

    if not roster:
        print("No lessons scheduled.")
        return

    print(f"{'Time':<8} {'Course':<32} {'Teacher':<24} {'Room'}")
    print("-" * 78)

    for lesson in roster:
        print(
            f"{lesson['start_time']:<8} "
            f"{lesson['course_name']:<32} "
            f"{lesson['teacher_name']:<24} "
            f"{lesson['room']}"
        )


def front_desk_show_records(manager):
    """Displays students, their courses, and all available courses."""
    print("\n--- Students ---")

    for student in manager.students:
        course_names = []

        for course_id in student.enrolled_course_ids:
            course = manager.find_course_by_id(course_id)

            if course:
                course_names.append(course.name)

        print(
            f"ID: {student.id} | {student.name} | "
            f"Courses: {', '.join(course_names)}"
        )

    print("\n--- Available Courses ---")

    for course in manager.courses:
        print(f"ID: {course.id} | {course.name} | {course.instrument}")


def switch_course(manager, student_id, from_course_id, to_course_id):
    """Requests a course switch through the ScheduleManager."""
    return manager.switch_course(student_id, from_course_id, to_course_id)


def read_number(prompt):
    """Reads a whole-number ID without crashing on invalid input."""
    try:
        return int(input(prompt))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def main():
    """Runs the MSMS console application."""
    manager = ScheduleManager()

    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("1. View Daily Roster")
        print("2. Check In Student")
        print("3. Switch Student Course")
        print("4. View Students and Courses")
        print("q. Quit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            day = input("Enter day (e.g., Monday): ").strip()
            front_desk_daily_roster(manager, day)

        elif choice == "2":
            student_id = read_number("Enter student ID: ")
            course_id = read_number("Enter course ID: ")

            if student_id is not None and course_id is not None:
                manager.check_in(student_id, course_id)

        elif choice == "3":
            student_id = read_number("Enter student ID: ")
            from_course_id = read_number("Enter current course ID: ")
            to_course_id = read_number("Enter new course ID: ")

            if None not in (student_id, from_course_id, to_course_id):
                switch_course(
                    manager,
                    student_id,
                    from_course_id,
                    to_course_id
                )

        elif choice == "4":
            front_desk_show_records(manager)

        elif choice.lower() == "q":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()