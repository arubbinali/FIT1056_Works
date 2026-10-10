import csv
import json

import pytest

from app.schedule import ScheduleManager


@pytest.fixture
def sample_data():
    """Return a small but complete set of music-school records."""
    return {
        "students": [
            {"id": 1, "name": "Alice", "enrolled_course_ids": [101]},
            {"id": 2, "name": "Bob", "enrolled_course_ids": [102]},
        ],
        "teachers": [
            {"id": 1, "name": "Evelyn", "speciality": "Piano"},
        ],
        "courses": [
            {
                "id": 101,
                "name": "Beginner Piano",
                "instrument": "Piano",
                "teacher_id": 1,
                "enrolled_student_ids": [1],
                "lessons": [
                    {
                        "lesson_id": 1,
                        "day": "Monday",
                        "start_time": "16:00",
                        "room": "Room A",
                    }
                ],
            },
            {
                "id": 102,
                "name": "Guitar",
                "instrument": "Guitar",
                "teacher_id": 99,
                "enrolled_student_ids": [2],
                "lessons": [],
            },
        ],
        "attendance": [],
        "finance": [],
    }


@pytest.fixture
def manager(tmp_path, sample_data):
    """Create a manager with an isolated JSON file for each test."""
    data_path = tmp_path / "msms.json"
    data_path.write_text(json.dumps(sample_data), encoding="utf-8")
    return ScheduleManager(data_path)


def test_loads_all_record_types(manager):
    # Arrange and Act are performed by the fixture.
    # Assert
    assert len(manager.students) == 2
    assert len(manager.teachers) == 1
    assert len(manager.courses) == 2
    assert manager.attendance_log == []
    assert manager.finance_log == []


def test_older_data_without_finance_key_remains_compatible(
    tmp_path, sample_data
):
    # Arrange
    sample_data.pop("finance")
    data_path = tmp_path / "old_pst4_data.json"
    data_path.write_text(json.dumps(sample_data), encoding="utf-8")

    # Act
    old_manager = ScheduleManager(data_path)

    # Assert
    assert old_manager.finance_log == []


def test_create_course_assigns_unique_id_and_persists(manager):
    # Act
    course = manager.create_course("Violin Basics", "Violin", 1)
    reloaded = ScheduleManager(manager.data_path)

    # Assert
    assert course.id == 103
    assert reloaded.find_course_by_id(103).name == "Violin Basics"


def test_record_payment_and_history_persist(manager):
    # Act
    result = manager.record_payment(1, 100.00, "Credit Card")
    reloaded = ScheduleManager(manager.data_path)
    history = reloaded.get_payment_history(1)

    # Assert
    assert result is True
    assert len(history) == 1
    assert history[0]["amount"] == 100.00
    assert history[0]["method"] == "Credit Card"
    assert "T" in history[0]["timestamp"]


@pytest.mark.parametrize("amount", [0, -10, "invalid", None, float("inf")])
def test_record_payment_rejects_invalid_amounts(manager, amount):
    # Act
    result = manager.record_payment(1, amount, "Cash")

    # Assert
    assert result is False
    assert manager.finance_log == []


def test_record_payment_rejects_unknown_student(manager):
    # Act
    result = manager.record_payment(999, 50, "Cash")

    # Assert
    assert result is False
    assert manager.finance_log == []


@pytest.mark.parametrize("method", ["", "   ", None])
def test_record_payment_rejects_blank_method(manager, method):
    # Act
    result = manager.record_payment(1, 50, method)

    # Assert
    assert result is False
    assert manager.finance_log == []


def test_get_payment_history_filters_by_student(manager):
    # Arrange
    manager.record_payment(1, 25, "Cash")
    manager.record_payment(2, 40, "Bank Transfer")

    # Act
    history = manager.get_payment_history(1)

    # Assert
    assert len(history) == 1
    assert history[0]["student_id"] == 1


def test_get_payment_history_no_results(manager):
    # Act
    history = manager.get_payment_history(1)

    # Assert
    assert history == []


def test_export_finance_report(manager, tmp_path):
    # Arrange
    manager.record_payment(1, 75.5, "Cash")
    report_path = tmp_path / "reports" / "finance.csv"

    # Act
    result = manager.export_report("finance", report_path)
    with report_path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    # Assert
    assert result is True
    assert len(rows) == 1
    assert rows[0]["student_id"] == "1"
    assert rows[0]["amount"] == "75.5"


def test_export_attendance_report(manager, tmp_path):
    # Arrange
    manager.check_in(1, 101)
    report_path = tmp_path / "attendance.csv"

    # Act
    result = manager.export_report("attendance", report_path)
    with report_path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    # Assert
    assert result is True
    assert rows[0]["course_id"] == "101"


def test_export_empty_report_still_writes_headers(manager, tmp_path):
    # Arrange
    report_path = tmp_path / "empty.csv"

    # Act
    result = manager.export_report("finance", report_path)

    # Assert
    assert result is True
    assert report_path.read_text(encoding="utf-8").strip() == (
        "student_id,amount,method,timestamp"
    )


def test_export_rejects_unknown_report_type(manager, tmp_path):
    # Arrange
    report_path = tmp_path / "unknown.csv"

    # Act
    result = manager.export_report("students", report_path)

    # Assert
    assert result is False
    assert not report_path.exists()


def test_check_in_requires_current_enrolment(manager):
    # Act
    valid_result = manager.check_in(1, 101)
    invalid_result = manager.check_in(1, 102)

    # Assert
    assert valid_result is True
    assert invalid_result is False
    assert len(manager.attendance_log) == 1


def test_switch_course_updates_both_sides_and_persists(manager):
    # Act
    result = manager.switch_course(1, 101, 102)
    reloaded = ScheduleManager(manager.data_path)

    # Assert
    assert result is True
    assert reloaded.find_student_by_id(1).enrolled_course_ids == [102]
    assert 1 not in reloaded.find_course_by_id(101).enrolled_student_ids
    assert 1 in reloaded.find_course_by_id(102).enrolled_student_ids


def test_cancel_lesson_hides_it_from_roster_and_persists(manager):
    # Act
    result = manager.cancel_lesson(1, "Teacher unavailable")
    reloaded = ScheduleManager(manager.data_path)

    # Assert
    assert result is True
    assert reloaded.get_daily_roster("Monday") == []
    lesson = reloaded.find_course_by_id(101).lessons[0]
    assert lesson["cancelled"] is True
    assert lesson["cancellation_reason"] == "Teacher unavailable"


def test_cancel_lesson_rejects_missing_lesson_or_reason(manager):
    # Act and Assert
    assert manager.cancel_lesson(999, "Unknown lesson") is False
    assert manager.cancel_lesson(1, "   ") is False


def test_corrupt_json_starts_with_empty_records(tmp_path):
    # Arrange
    data_path = tmp_path / "broken.json"
    data_path.write_text("{not valid json", encoding="utf-8")

    # Act
    broken_manager = ScheduleManager(data_path)

    # Assert
    assert broken_manager.students == []
    assert broken_manager.finance_log == []
