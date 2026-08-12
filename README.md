# FIT1056
## Music School Management System (MSMS)

This project builds a Music School Management System over five stages (PSTs). Each stage is an upgrade on the one before it, going from a simple in-memory script all the way to a proper, tested application with a GUI. It's an individual task, tracked with Git the whole way through.

## Index

1. [PST1 - The In-Memory Prototype](#pst1---the-in-memory-prototype)
2. [PST2 - The Upgrade (file storage, validation)](#pst2---the-upgrade)
3. PST3 - The Architecture (OOP rebuild)
4. PST4 - The User Interface (GUI)
5. PST5 - The Quality Assurance (automated tests)

---

## PST1 - The In-Memory Prototype

This is the first stage. The goal here is just to get a working console app going that proves the core logic works - registering students, enrolling them in instruments, and looking things up. Nothing gets saved anywhere yet, all the data lives in memory and resets every time the program stops. Everything is built inside one file, [`MSMS.py`](https://github.com/arubbinali/FIT1056_Works/blob/main/FIT1056-PSTs-36913006/PST1/MSMS.py).

It's broken into 4 fragments:

- **Fragment 1.1** - the data models (Student, Teacher classes) and the in-memory lists that act as the databases.
- **Fragment 1.2** - the core helper functions that manage the data (adding, listing, searching).
- **Fragment 1.3** - the front desk functions, the higher-level stuff that actually gets used by the menu.
- **Fragment 1.4** - the main menu that ties everything together.

### Functions

- `add_teacher(name, speciality)` - creates a new teacher and adds them to the teacher list.
- `list_students()` - prints every student and what they're enrolled in.
- `list_teachers()` - prints every teacher and their speciality.
- `find_students(term)` - searches students by name.
- `find_teachers(term)` - searches teachers by name or speciality.
- `find_student_by_id(student_id)` - looks up a single student by their exact ID.
- `front_desk_register(name, instrument)` - registers a new student and enrols them in one instrument at the same time.
- `front_desk_enrol(student_id, instrument)` - enrols an existing student in a new instrument.
- `front_desk_lookup(term)` - searches both students and teachers at once.
- `main()` - runs the interactive menu loop.

---

## PST2 - The Upgrade

PST2 refactors everything into a single global `app_data` dictionary and adds a proper JSON persistence layer, so students, teachers, and attendance records survive between runs. It also fills in the missing CRUD operations (update and delete) and introduces two new receptionist features: checking students in and printing a student ID card. [`MSMS.py`](https://github.com/arubbinali/FIT1056_Works/blob/main/FIT1056-PSTs-36913006/PST1/MSMS.py) is retired for this stage and everything now lives in one new file, [`pst2_main.py`](https://github.com/arubbinali/FIT1056_Works/blob/main/FIT1056-PSTs-36913006/PST2/pst2_main.py).

It's broken into 4 fragments:

- **Fragment 2.1** - the core persistence engine: `load_data()` and `save_data()`, which read and write the whole `app_data` dictionary to `msms.json`.
- **Fragment 2.2** - the full CRUD operations for teachers and students, rewritten to work against `app_data` instead of separate lists, with update and remove added for both.
- **Fragment 2.3** - the new receptionist features: checking a student into a course and printing a text-file ID badge for them.
- **Fragment 2.4** - the refactored main menu, which loads data on startup and saves immediately after any change.

### Functions

- `load_data(path)` - reads `app_data` in from the JSON file at `path`; if the file doesn't exist yet, initialises `app_data` with an empty default structure instead.
- `save_data(path)` - writes the current `app_data` dictionary out to the JSON file at `path`, formatted for readability.
- `add_teacher(name, speciality)` - creates a new teacher dictionary and adds it to `app_data['teachers']`.
- `update_teacher(teacher_id, **fields)` - finds a teacher by ID and updates any of their fields with the keyword arguments passed in.
- `remove_teacher(teacher_id)` - finds a teacher by ID and removes them from `app_data['teachers']`.
- `update_student(student_id, **fields)` - finds a student by ID and updates any of their fields with the keyword arguments passed in.
- `remove_student(student_id)` - finds a student by ID and removes them from `app_data['students']`.
- `check_in(student_id, course_id, timestamp)` - records an attendance entry in `app_data['attendance']`, defaulting to the current time if no timestamp is given.
- `print_student_card(student_id)` - looks up a student and writes their details to a text-file badge, e.g. `1_card.txt`.
- `main()` - loads the saved data on startup, runs the interactive menu, and saves after every change.

### Design choices / assumptions

- `save_data()` is called immediately after any state-changing action (check-in, update, remove) rather than only on exit, so a crash or forced quit doesn't lose progress.
- ID lookups assume `student_id` / `teacher_id` are unique integers matching the `id` key stored in each record.

---

Author: Arub

Website: https://doaor.com/

Other works: https://doaor.com/d/

> This README is not complete and is under development. ([https://github.com/arubbinali/FIT1056_Works](https://github.com/arubbinali/FIT1056_Works))