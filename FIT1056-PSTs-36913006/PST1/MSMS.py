# MSMS.py - The In-Memory Prototype

# --- Data Models ---
class Student:
    """A blueprint for student objects. Holds their info."""
    def __init__(self, student_id, name):
        self.id = student_id
        self.name = name
        self.enrolled_in = []

class Teacher:
    """A blueprint for teacher objects."""
    def __init__(self, teacher_id, name, speciality):
        self.id = teacher_id
        self.name = name
        self.speciality = speciality

# --- In-Memory Databases ---
student_db = []
teacher_db = []
next_student_id = 1
next_teacher_id = 1


# --- Core Helper Functions ---
def add_teacher(name, speciality):
    """Creates a Teacher object and adds it to the database."""
    global next_teacher_id
    new_teacher = Teacher(next_teacher_id, name, speciality)
    teacher_db.append(new_teacher)
    # TODO: Increment the next_teacher_id counter.
    next_teacher_id += 1
    print(f"Core: Teacher '{name}' added successfully.")

def list_students():
    """Prints all students in the database."""
    print("\n--- Student List ---")
    if not student_db:
        print("No students in the system.")
        return
    for student in student_db:
        print(f"  ID: {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")

def list_teachers():
    """Prints all teachers in the database."""
    print("\n--- Teacher List ---")
    for teacher in teacher_db:
        print(f"  ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")

def find_students(term):
    """Finds students by name."""
    print(f"\n--- Finding Students matching '{term}' ---")

    results = []

    for student in student_db:
        if term in student: results.append(student)
 
    if len(results) == 0: print("No match found.")
    else:
        for student in results:
            print(f"  ID: {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")

def find_teachers(term):
    """Finds teachers by name or speciality."""
    # TODO: Implement this function similar to find_students, but check
    # for the term in BOTH the teacher's name AND their speciality.
    results = []

    for teacher in teacher_db:
        if (term.lower() in teacher.name.lower()) or (term.lower() in teacher.speciality.lower()):
            results.append(teacher)

    if len(results) == 0: print("No match found.")
    else:
        for teacher in results:
            print(f"  ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")



# --- Front Desk Functions ---
def find_student_by_id(student_id):
    """A new helper to find one student by their exact ID."""
    for student in student_db:
        if student.id == student_id:
            return student
    return None

def front_desk_register(name, instrument):
    """High-level function to register a new student and enrol them."""
    global next_student_id
    new_student = Student(next_student_id, name)
    student_db.append(new_student)
    next_student_id += 1
    
    front_desk_enrol(new_student.id, instrument)
    print(f"Front Desk: Successfully registered '{name}' and enrolled them in '{instrument}'.")

def front_desk_enrol(student_id, instrument):
    """High-level function to enrol an existing student in a course."""
    student = find_student_by_id(student_id)
    if student:
        student.enrolled_in.append(instrument)
        print(f"Front Desk: Enrolled student {student_id} in '{instrument}'.")
    else:
        print(f"Error: Student ID {student_id} not found.")

def front_desk_lookup(term):
    """High-level function to search everything."""
    print(f"\n--- Performing lookup for '{term}' ---")
    find_students(term)
    find_teachers(term)