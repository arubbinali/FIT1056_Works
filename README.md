# FIT1056
## Music School Management System (MSMS)

This project builds a Music School Management System over five stages
(PSTs). Each stage is an upgrade on the one before it, going from a
simple in-memory script all the way to a proper, tested application with
a GUI. It's an individual task, tracked with Git the whole way through.

## Index

1. [PST1 - The In-Memory Prototype](#pst1---the-in-memory-prototype)
2. PST2 - The Upgrade (file storage, validation)
3. PST3 - The Architecture (OOP rebuild)
4. PST4 - The User Interface (GUI)
5. PST5 - The Quality Assurance (automated tests)

---

## PST1 - The In-Memory Prototype

This is the first stage. The goal here is just to get a working
console app going that proves the core logic works - registering
students, enrolling them in instruments, and looking things up. Nothing
gets saved anywhere yet, all the data lives in memory and resets every
time the program stops. Everything is built inside one file, [`MSMS.py`](https://github.com/arubbinali/FIT1056_Works/blob/main/FIT1056-PSTs-36913006/PST1/MSMS.py).

It's broken into 4 fragments:

- **Fragment 1.1** - the data models (Student, Teacher classes) and the
  in-memory lists that act as the databases.
- **Fragment 1.2** - the core helper functions that manage the data
  (adding, listing, searching).
- **Fragment 1.3** - the front desk functions, the higher-level stuff
  that actually gets used by the menu.
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
Author: Arub

Website: https://doaor.com/

Other works: https://doaor.com/d/

> This README is not complete and is under development. ([https://github.com/arubbinali/FIT1056_Works](https://github.com/arubbinali/FIT1056_Works))
