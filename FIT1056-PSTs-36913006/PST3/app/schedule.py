import json

from app.student import StudentUser
from app.teacher import TeacherUser, Course


class ScheduleManager:
    """The main controller for all business logic and data handling."""

    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self._load_data()

    def _load_data(self):
        """Loads JSON data and recreates the model objects."""
        try:
            with open(self.data_path, "r") as file:
                data = json.load(file)

            for student_data in data.get("students", []):
                student = StudentUser(
                    student_data["id"],
                    student_data["name"]
                )
                student.enrolled_course_ids = student_data.get(
                    "enrolled_course_ids",
                    []
                )
                self.students.append(student)

            for teacher_data in data.get("teachers", []):
                teacher = TeacherUser(
                    teacher_data["id"],
                    teacher_data["name"],
                    teacher_data["speciality"]
                )
                self.teachers.append(teacher)

            for course_data in data.get("courses", []):
                course = Course(
                    course_data["id"],
                    course_data["name"],
                    course_data["instrument"],
                    course_data["teacher_id"]
                )
                course.enrolled_student_ids = course_data.get(
                    "enrolled_student_ids",
                    []
                )
                course.lessons = course_data.get("lessons", [])
                self.courses.append(course)

            self.attendance_log = data.get("attendance", [])

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")

    def _save_data(self):
        """Converts objects to dictionaries and saves them to JSON."""
        data_to_save = {
            "students": [student.__dict__ for student in self.students],
            "teachers": [teacher.__dict__ for teacher in self.teachers],
            "courses": [course.__dict__ for course in self.courses],
            "attendance": self.attendance_log
        }

        with open(self.data_path, "w") as file:
            json.dump(data_to_save, file, indent=4)