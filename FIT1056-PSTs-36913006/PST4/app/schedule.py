import datetime
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

    def find_student_by_id(self, student_id):
        """Finds one student using their exact ID."""
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def find_course_by_id(self, course_id):
        """Finds one course using its exact ID."""
        for course in self.courses:
            if course.id == course_id:
                return course
        return None

    def check_in(self, student_id, course_id):
        """Records a student's attendance for a valid course."""
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False

        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {
            "student_id": student_id,
            "course_id": course_id,
            "timestamp": timestamp
        }

        self.attendance_log.append(check_in_record)
        self._save_data()
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

    def find_teacher_by_id(self, teacher_id):
        """Finds one teacher using their exact ID."""
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None

    def get_daily_roster(self, day):
        """Returns all lessons scheduled on a given day."""
        roster = []

        for course in self.courses:
            teacher = self.find_teacher_by_id(course.teacher_id)

            for lesson in course.lessons:
                if lesson["day"].lower() == day.lower():
                    roster.append({
                        "start_time": lesson["start_time"],
                        "course_name": course.name,
                        "teacher_name": teacher.name,
                        "room": lesson["room"]
                    })

        return sorted(roster, key=lambda lesson: lesson["start_time"])

    def switch_course(self, student_id, from_course_id, to_course_id):
        """Moves a student from one valid course to another."""
        student = self.find_student_by_id(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if not student or not from_course or not to_course:
            print("Error: Course switch failed. Invalid Student or Course ID.")
            return False

        if from_course_id not in student.enrolled_course_ids:
            print(f"Error: {student.name} is not enrolled in {from_course.name}.")
            return False

        if to_course_id in student.enrolled_course_ids:
            print(f"Error: {student.name} is already enrolled in {to_course.name}.")
            return False

        student.enrolled_course_ids.remove(from_course_id)
        student.enrolled_course_ids.append(to_course_id)

        from_course.enrolled_student_ids.remove(student_id)
        to_course.enrolled_student_ids.append(student_id)

        self._save_data()
        print(f"Success: {student.name} switched from {from_course.name} to {to_course.name}.")
        return True