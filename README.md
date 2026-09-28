# FIT1056 - Music School Management System

This individual project develops a Music School Management System (MSMS) across five Problem-Solving Tasks (PSTs). Each stage improves the architecture and functionality of the previous stage.

## Project stages

- **PST1 - In-Memory Prototype:** Console-based student and teacher management using in-memory data.
- **PST2 - Persistence Upgrade:** Added JSON storage, CRUD operations, attendance records, and student ID-card generation.
- **PST3 - Object-Oriented Architecture:** Rebuilt the system using model classes, a controller, persistent data, and a separate console view.
- **PST4 - Graphical User Interface:** Replaced the console view with a Streamlit interface for managing students, courses, attendance, and daily rosters.
- **PST5 - Quality Assurance:** Will add automated testing and further error handling.

## PST4 features

- Streamlit dashboard with navigation and session-state management.
- Overview page showing totals for students, teachers, courses, and attendance records.
- Case-insensitive student search by full or partial name.
- Student registration using a name and instrument.
- Automatic student ID generation.
- Validation for blank names, duplicate students, invalid instruments, and unavailable courses.
- Daily lesson roster filtered by weekday.
- Roster information showing lesson time, course, teacher, and room.
- Student check-in using valid student and course IDs.
- Attendance records saved with ISO-format timestamps.
- Course switching with validation for invalid IDs, existing enrolments, and duplicate target courses.
- Persistent JSON storage so changes remain after restarting the application.
- Safe handling of courses without an assigned teacher.

## PST4 structure

```text
FIT1056-PSTs-36913006/
└── PST4/
    ├── app/
    │   ├── __init__.py
    │   ├── user.py
    │   ├── student.py
    │   ├── teacher.py
    │   └── schedule.py
    ├── data/
    │   └── msms.json
    ├── gui/
    │   ├── __init__.py
    │   ├── main_dashboard.py
    │   ├── student_pages.py
    │   ├── roster_pages.py
    │   └── course_pages.py
    ├── main.py
    └── requirements.txt
```

## Requirements

- Python 3
- Streamlit 1.64.0
- pandas 2.3.3

Install the required packages from inside the PST4 folder:

```bash
py -m pip install -r requirements.txt
```

## Running PST4

Navigate to the PST4 folder:

```bash
cd FIT1056-PSTs-36913006/PST4
```

Start the Streamlit application:

```bash
py -m streamlit run main.py
```

Streamlit will display a local address in the terminal and normally open the application automatically in the default web browser.

## Using the application

### Overview

The overview page displays the total numbers of students, teachers, courses, and attendance records currently loaded from the JSON data file.

### Student search

Open the student search page and enter all or part of a student's name. The search is case-insensitive and displays matching students and their enrolled courses.

### Student registration

Enter the student's name and select an instrument. The system finds an available course for that instrument, creates a unique student ID, enrols the student, and saves the updated data.

### Daily roster

Select a weekday to view all lessons scheduled for that day. Each roster entry includes the start time, course name, teacher, and room.

### Student check-in

Select a student and course from the displayed options. A successful check-in adds an attendance record containing the student ID, course ID, and current timestamp.

### Course management

The course-management page displays the available courses and allows a student to switch from one enrolled course to another valid course.

## Testing

PST4 was tested using copies of the supplied sample JSON data so the original data remained unchanged.

The following scenarios were tested:

- The supplied students, teachers, courses, lessons, and attendance records load correctly.
- Student searches work with full names, partial names, and different letter cases.
- A valid student registration updates both the student and course enrolment records.
- Registered students remain available after the JSON file is reloaded.
- Blank names, duplicate names, and invalid instruments are rejected.
- Monday's roster displays Beginner Piano at 16:00 in Room A.
- Days without lessons display an empty-roster message.
- A course with a missing teacher displays `Unassigned` instead of crashing.
- A valid check-in is saved and remains after the JSON file is reloaded.
- Invalid student and course IDs are rejected without crashing.
- Valid course switches update the student and both course enrolment lists.
- Invalid and duplicate course switches are rejected.
- The saved JSON remains valid after changes.

Python files can also be checked for syntax errors from the repository root using:

```bash
py -m compileall -q FIT1056-PSTs-36913006/PST4
```

## Design choices and assumptions

PST4 separates the program into three main layers:

- **Model:** `User`, `StudentUser`, `TeacherUser`, and `Course` represent the system's main entities.
- **Controller:** `ScheduleManager` handles data loading, saving, searching, registration, attendance, rosters, and course switching.
- **View:** The files inside `gui` contain the Streamlit pages and user-interface components.

One `ScheduleManager` instance is stored in Streamlit session state so the application does not reload the controller unnecessarily during normal page interactions.

Student registration enrols a student in the first available course matching the selected instrument. Only courses with assigned teachers are offered for registration.

The JSON file is saved immediately after operations that change the data, reducing the risk of losing changes if the program closes unexpectedly.

## AI acknowledgement

OpenAI Codex was used to assist with code development, debugging, testing strategy, and documentation. All generated work was reviewed, tested, and understood by the author.

## Author

**Muhammad Arub bin Ali**  
Student ID: **36913006**