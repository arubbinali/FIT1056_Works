import json
import datetime

DATA_FILE = "msms.json"
app_data = {}

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    global app_data
    try:
        with open(path, 'r') as f:
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")

# --- Full CRUD for Core Data ---
def add_teacher(name, speciality):
    teacher_id = app_data['next_teacher_id']
    new_teacher = {"id": teacher_id, "name": name, "speciality": speciality}
    app_data['teachers'].append(new_teacher)
    app_data['next_teacher_id'] += 1
    print(f"Core: Teacher '{name}' added.")

def update_teacher(teacher_id, **fields):
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")

def remove_teacher(teacher_id):
    original_len = len(app_data['teachers'])
    app_data['teachers'] = [t for t in app_data['teachers'] if t['id'] != teacher_id]
    if len(app_data['teachers']) < original_len:
        print(f"Teacher {teacher_id} removed.")
    else:
        print(f"Error: Teacher with ID {teacher_id} not found.")

def update_student(student_id, **fields):
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            print(f"Student {student_id} updated.")
            return
    print(f"Error: Student with ID {student_id} not found.")

def remove_student(student_id):
    original_len = len(app_data['students'])
    app_data['students'] = [s for s in app_data['students'] if s['id'] != student_id]
    if len(app_data['students']) < original_len:
        print(f"Student {student_id} removed.")
    else:
        print(f"Error: Student with ID {student_id} not found.")

# --- New Receptionist Features ---
def check_in(student_id, course_id, timestamp=None):
    if timestamp is None:
        timestamp = datetime.datetime.now().isoformat()

    check_in_record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
    }
    app_data['attendance'].append(check_in_record)
    print(f"Receptionist: Student {student_id} checked into {course_id}.")

def print_student_card(student_id):
    student_to_print = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student_to_print = s
            break

    if student_to_print:
        filename = f"{student_id}_card.txt"
        with open(filename, 'w') as f:
            f.write("========================\n")
            f.write(f"  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student_to_print['id']}\n")
            f.write(f"Name: {student_to_print['name']}\n")
            f.write(f"Enrolled In: {', '.join(student_to_print.get('enrolled_in', []))}\n")
        print(f"Printed student card to {filename}.")
    else:
        print(f"Error: Could not print card, student {student_id} not found.")