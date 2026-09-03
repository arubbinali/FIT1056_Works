# FIT1056 - Music School Management System

This individual project develops a Music School Management System (MSMS) across five Problem-Solving Tasks (PSTs). Each stage improves the architecture and functionality of the previous one.

## Project stages

- **PST1 - In-Memory Prototype:** A console application for registering, enrolling, listing, and searching students and teachers.
- **PST2 - Persistence Upgrade:** Adds JSON storage, CRUD operations, attendance records, and student ID-card printing.
- **PST3 - Object-Oriented Architecture:** Rebuilds the system using dedicated model classes, a controller, persistent data, and a separate console view.
- **PST4 - User Interface:** Will replace the console interface with a GUI.
- **PST5 - Quality Assurance:** Will add automated tests and further error handling.

## PST3 structure

```text
FIT1056-PSTs-36913006/
└── PST3/
    ├── app/
    │   ├── user.py
    │   ├── student.py
    │   ├── teacher.py
    │   └── schedule.py
    ├── data/
    │   └── msms.json
    └── main.py
````

## PST3 features

* Uses `User`, `StudentUser`, `TeacherUser`, and `Course` classes to represent the system's core entities.
* Uses `ScheduleManager` as the controller for loading, saving, searching, attendance, daily rosters, and course switches.
* Loads JSON dictionaries into Python objects on startup and saves objects back to JSON after changes.
* Displays daily lesson rosters with the lesson time, course, teacher, and room.
* Displays students and available courses so the receptionist can find valid IDs.
* Records a student check-in with an ISO-format timestamp.
* Validates IDs and prevents invalid or duplicate course switches.

## Running PST3

Python 3 is the only requirement.

```bash
cd FIT1056-PSTs-36913006/PST3
python main.py
```

Use the menu to view a daily roster, check in a student, or switch a student between courses. Enter `q` to quit.

## Testing

PST3 was tested using the supplied sample data.

* Viewing Monday's roster returns Beginner Piano at 16:00 in Room A.
* A valid check-in is saved and remains after the JSON data is reloaded.
* An invalid student or course ID returns `False` without crashing the program.
* Switching Alice from course `103` to course `102` updates both the student's and courses' enrolment lists.

## Design choices

The project separates responsibilities into three layers:

* **Model:** `User`, `StudentUser`, `TeacherUser`, and `Course` store the system data.
* **Controller:** `ScheduleManager` contains business logic and persistence.
* **View:** `main.py` handles user interaction and delegates work to one `ScheduleManager` instance.

