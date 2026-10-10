import csv
import datetime
import json
import logging
import math
from pathlib import Path

from app.student import StudentUser
from app.teacher import Course, TeacherUser

DEFAULT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "msms.json"
LOGGER = logging.getLogger(__name__)


class ScheduleManager:
    """Controls the music school's records and business operations."""

    def __init__(self, data_path=None):
        self.data_path = Path(data_path) if data_path else DEFAULT_DATA_PATH
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self.finance_log = []
        self._load_data()

    def _load_data(self):
        """Load saved JSON records and recreate the model objects."""
        try:
            with self.data_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            LOGGER.warning(
                "Data file %s was not found; starting with empty records.",
                self.data_path,
            )
            return
        except (json.JSONDecodeError, OSError) as error:
            LOGGER.error("Could not load %s: %s", self.data_path, error)
            return

        for student_data in data.get("students", []):
            student = StudentUser(student_data["id"], student_data["name"])
            student.enrolled_course_ids = student_data.get(
                "enrolled_course_ids", []
            )
            self.students.append(student)

        for teacher_data in data.get("teachers", []):
            teacher = TeacherUser(
                teacher_data["id"],
                teacher_data["name"],
                teacher_data["speciality"],
            )
            self.teachers.append(teacher)

        for course_data in data.get("courses", []):
            course = Course(
                course_data["id"],
                course_data["name"],
                course_data["instrument"],
                course_data["teacher_id"],
            )
            course.enrolled_student_ids = course_data.get(
                "enrolled_student_ids", []
            )
            course.lessons = course_data.get("lessons", [])
            self.courses.append(course)

        self.attendance_log = data.get("attendance", [])
        # Loading with a default keeps older PST4 data files compatible.
        self.finance_log = data.get("finance", [])

    def _save_data(self):
        """Convert the objects to dictionaries and save all records to JSON."""
        data_to_save = {
            "students": [student.__dict__ for student in self.students],
            "teachers": [teacher.__dict__ for teacher in self.teachers],
            "courses": [course.__dict__ for course in self.courses],
            "attendance": self.attendance_log,
            "finance": self.finance_log,
        }

        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with self.data_path.open("w", encoding="utf-8") as file:
            json.dump(data_to_save, file, indent=4)

    def find_student_by_id(self, student_id):
        """Return the student with the given ID, or None if not found."""
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def find_teacher_by_id(self, teacher_id):
        """Return the teacher with the given ID, or None if not found."""
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None

    def find_course_by_id(self, course_id):
        """Return the course with the given ID, or None if not found."""
        for course in self.courses:
            if course.id == course_id:
                return course
        return None

    def create_course(self, name, instrument, teacher_id):
        """Create, save, and return a course with a new unique ID."""
        if not isinstance(name, str) or not isinstance(instrument, str):
            return None

        clean_name = name.strip()
        clean_instrument = instrument.strip()

        if not clean_name or not clean_instrument:
            return None

        course_id = max((course.id for course in self.courses), default=100) + 1
        course = Course(course_id, clean_name, clean_instrument, teacher_id)
        self.courses.append(course)
        self._save_data()
        LOGGER.info("Course %s created with ID %s.", clean_name, course_id)
        return course

    def check_in(self, student_id, course_id):
        """Record attendance when both IDs exist and the student is enrolled."""
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if student is None or course is None:
            return False

        if course_id not in student.enrolled_course_ids:
            return False

        check_in_record = {
            "student_id": student_id,
            "course_id": course_id,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        self.attendance_log.append(check_in_record)
        self._save_data()
        LOGGER.info(
            "Student ID %s checked into course ID %s.", student_id, course_id
        )
        return True

    def get_daily_roster(self, day):
        """Return active lessons scheduled on a given day, ordered by time."""
        if not isinstance(day, str):
            return []

        clean_day = day.strip().lower()
        roster = []

        for course in self.courses:
            teacher = self.find_teacher_by_id(course.teacher_id)
            teacher_name = teacher.name if teacher else "Unassigned"

            for lesson in course.lessons:
                is_cancelled = lesson.get("cancelled", False)
                is_requested_day = lesson.get("day", "").lower() == clean_day

                if is_requested_day and not is_cancelled:
                    roster.append(
                        {
                            "start_time": lesson.get("start_time", "Unknown"),
                            "course_name": course.name,
                            "teacher_name": teacher_name,
                            "room": lesson.get("room", "Unassigned"),
                        }
                    )

        return sorted(roster, key=lambda lesson: lesson["start_time"])

    def switch_course(self, student_id, from_course_id, to_course_id):
        """Move a student from one valid enrolment to another course."""
        student = self.find_student_by_id(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if student is None or from_course is None or to_course is None:
            return False

        has_source_enrolment = (
            from_course_id in student.enrolled_course_ids
            and student_id in from_course.enrolled_student_ids
        )
        has_target_enrolment = (
            to_course_id in student.enrolled_course_ids
            or student_id in to_course.enrolled_student_ids
        )

        if not has_source_enrolment or has_target_enrolment:
            return False

        student.enrolled_course_ids.remove(from_course_id)
        student.enrolled_course_ids.append(to_course_id)
        from_course.enrolled_student_ids.remove(student_id)
        to_course.enrolled_student_ids.append(student_id)

        self._save_data()
        LOGGER.info(
            "Student ID %s switched from course %s to course %s.",
            student_id,
            from_course_id,
            to_course_id,
        )
        return True

    def search_students(self, term):
        """Return students whose names or IDs contain the search term."""
        search_term = str(term).strip().lower()

        if not search_term:
            return self.students.copy()

        return [
            student
            for student in self.students
            if search_term in student.name.lower()
            or search_term == str(student.id)
        ]

    def register_new_student(self, name, instrument):
        """Register a unique student in the first matching staffed course."""
        if not isinstance(name, str) or not isinstance(instrument, str):
            return None

        clean_name = name.strip()
        clean_instrument = instrument.strip().lower()

        if not clean_name or not clean_instrument:
            return None

        if any(
            student.name.lower() == clean_name.lower()
            for student in self.students
        ):
            return None

        selected_course = None
        for course in self.courses:
            teacher = self.find_teacher_by_id(course.teacher_id)
            if course.instrument.lower() == clean_instrument and teacher:
                selected_course = course
                break

        if selected_course is None:
            return None

        student_id = max(
            (student.id for student in self.students), default=0
        ) + 1
        student = StudentUser(student_id, clean_name)
        student.enrolled_course_ids.append(selected_course.id)
        self.students.append(student)
        selected_course.enrolled_student_ids.append(student_id)

        self._save_data()
        LOGGER.info("Student %s registered with ID %s.", clean_name, student_id)
        return student

    def record_payment(self, student_id, amount, method):
        """Validate and save a payment for an existing student."""
        student = self.find_student_by_id(student_id)
        clean_method = "" if method is None else str(method).strip()

        try:
            clean_amount = float(amount)
        except (TypeError, ValueError):
            return False

        if (
            student is None
            or isinstance(amount, bool)
            or not math.isfinite(clean_amount)
            or clean_amount <= 0
            or not clean_method
        ):
            return False

        payment_record = {
            "student_id": student_id,
            "amount": round(clean_amount, 2),
            "method": clean_method,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        self.finance_log.append(payment_record)
        self._save_data()
        LOGGER.info(
            "Payment of %.2f recorded for student ID %s.",
            clean_amount,
            student_id,
        )
        return True

    def get_payment_history(self, student_id):
        """Return all payment records belonging to one student."""
        return [
            payment
            for payment in self.finance_log
            if payment.get("student_id") == student_id
        ]

    def export_report(self, kind, out_path):
        """Export the finance or attendance log to a CSV file."""
        report_kind = str(kind).strip().lower()

        if report_kind == "finance":
            records = self.finance_log
            headers = ["student_id", "amount", "method", "timestamp"]
        elif report_kind == "attendance":
            records = self.attendance_log
            headers = ["student_id", "course_id", "timestamp"]
        else:
            return False

        if out_path is None:
            return False

        output_path = Path(out_path)
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file, fieldnames=headers, extrasaction="ignore"
                )
                writer.writeheader()
                writer.writerows(records)
        except OSError as error:
            LOGGER.error("Could not export %s report: %s", report_kind, error)
            return False

        LOGGER.info("%s report exported to %s.", report_kind, output_path)
        return True

    def cancel_lesson(self, lesson_id, reason):
        """Mark a lesson as cancelled while retaining its audit details."""
        clean_reason = "" if reason is None else str(reason).strip()
        if not clean_reason:
            return False

        for course in self.courses:
            for lesson in course.lessons:
                if lesson.get("lesson_id") == lesson_id:
                    if lesson.get("cancelled", False):
                        return False

                    lesson["cancelled"] = True
                    lesson["cancellation_reason"] = clean_reason
                    lesson["cancelled_at"] = (
                        datetime.datetime.now().isoformat()
                    )
                    self._save_data()
                    LOGGER.warning(
                        "Lesson ID %s was cancelled. Reason: %s",
                        lesson_id,
                        clean_reason,
                    )
                    return True

        return False
