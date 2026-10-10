# FIT1056 - Music School Management System

This individual project develops a Music School Management System (MSMS)
across five Problem-Solving Tasks. Each stage improves the architecture,
functionality, and reliability of the previous stage.

## Project stages

- **PST1 - In-Memory Prototype:** Console-based student and teacher
  management using in-memory data.
- **PST2 - Persistence Upgrade:** Added JSON storage, CRUD operations,
  attendance records, and student ID-card generation.
- **PST3 - Object-Oriented Architecture:** Rebuilt the system using model
  classes, a controller, persistent data, and a separate console view.
- **PST4 - Graphical User Interface:** Replaced the console view with a
  Streamlit interface for students, courses, attendance, and daily rosters.
- **PST5 - Quality and Finance Gate:** Added payment tracking, CSV reports,
  logging, backups, lesson cancellation, input validation, and automated tests.

## PST5 features

- Records validated payments for existing students and saves them to JSON.
- Shows each student's payment history and total amount paid.
- Exports finance and attendance reports as CSV files.
- Provides finance and report-download controls in the Streamlit interface.
- Creates a timestamped data backup when a Streamlit session starts.
- Logs important operations and errors to `logs/msms.log`.
- Cancels lessons without deleting their audit details.
- Preserves compatibility with PST4 JSON files that do not contain finance data.
- Handles missing or malformed data files without crashing during startup.
- Includes automated tests for successful operations, invalid input,
  persistence, reporting, backups, logging, and important edge cases.

## PST5 structure

```text
FIT1056-PSTs-36913006/
└── PST5/
    ├── app/
    │   ├── __init__.py
    │   ├── admin_utils.py
    │   ├── schedule.py
    │   ├── student.py
    │   ├── teacher.py
    │   └── user.py
    ├── data/
    │   └── msms.json
    ├── gui/
    │   ├── __init__.py
    │   ├── course_pages.py
    │   ├── finance_pages.py
    │   ├── main_dashboard.py
    │   ├── roster_pages.py
    │   └── student_pages.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test_admin_utils.py
    │   └── test_schedule_manager.py
    ├── main.py
    ├── pytest.ini
    └── requirements.txt
```

The `logs/` and `data/backups/` directories are created automatically at
runtime and should not be committed.

## Requirements and installation

- Python 3.10 or newer
- Streamlit
- pandas
- pytest

From inside the `PST5` directory, install the declared packages:

```powershell
py -m pip install -r requirements.txt
```

## Running the application

From the repository root:

```powershell
Set-Location .\FIT1056-PSTs-36913006\PST5
py -m streamlit run main.py
```

Streamlit displays a local URL and normally opens it in the default browser.
Use the sidebar to open the overview, student, roster, course, and finance
pages.

## Running the automated tests

Run the following command from inside `PST5`:

```powershell
py -m pytest
```

Pytest automatically discovers the files in `tests/`. A successful run ends
with all tests marked as passed. The tests use temporary files, so they do not
change `data/msms.json`.

Python syntax can also be checked from inside `PST5`:

```powershell
py -m compileall -q .
```

## Main PST5 operations

### Payment recording

`ScheduleManager.record_payment(student_id, amount, method)` confirms that the
student exists, the amount is a finite positive number, and the payment method
is not blank. A successful payment receives an ISO-format timestamp, is added
to `finance_log`, is saved immediately, and produces a log entry.

### Payment history

`ScheduleManager.get_payment_history(student_id)` filters the finance log and
returns only that student's transactions. The finance page displays these
records and calculates the student's total paid amount.

### CSV reports

`ScheduleManager.export_report(kind, out_path)` supports `finance` and
`attendance`. It writes the correct CSV header even when a report has no rows,
creates missing output directories, and rejects unknown report types.

### Logging and backups

`init_logger()` configures timestamped file logging. `backup_data()` copies the
JSON file to `data/backups/` with a unique timestamped filename. The launcher
creates one backup at the beginning of each Streamlit browser session.

### Lesson cancellation

`ScheduleManager.cancel_lesson(lesson_id, reason)` records the reason and
cancellation timestamp instead of deleting the lesson. Cancelled lessons are
excluded from the active daily roster while their audit data remains saved.

## Testing completed

The automated suite covers:

- loading all object and log data;
- compatibility with older PST4 data;
- unique course creation and persistence;
- valid payment recording and reloading;
- rejected unknown students, blank methods, and invalid amounts;
- student-specific and empty payment histories;
- finance, attendance, empty, and invalid CSV exports;
- enrolment-aware student check-in;
- consistent course switching on both sides of the relationship;
- lesson cancellation and roster filtering;
- safe handling of malformed JSON;
- successful backups, missing backup sources, and file logging.

The Streamlit launcher and every navigation page were also smoke-tested using
Streamlit's application testing interface.

## Design choices and assumptions

- `User`, `StudentUser`, `TeacherUser`, and `Course` are the data models.
- `ScheduleManager` is the controller for persistence and business logic.
- Files in `gui/` are the Streamlit view layer.
- JSON remains the single source of truth so the system stays compatible with
  earlier PST stages.
- State-changing methods save immediately to reduce data loss.
- Student check-in requires enrolment in the selected course.
- Payment amounts are stored as numbers rounded to two decimal places.
- Cancellation is non-destructive so administrators retain an audit trail.
- One `ScheduleManager` is stored in Streamlit session state during a session.

## AI acknowledgement

OpenAI Codex was used to assist with code development, debugging, testing
strategy, and documentation. All generated work was reviewed and tested by the
author.

## Author

**Muhammad Arub bin Ali**

Student ID: **36913006**
