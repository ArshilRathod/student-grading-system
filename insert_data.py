import sqlite3

# Connect to the database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# --------------------------
# 1. Insert Students
# --------------------------
students = [
    ("Arshil", "R001", "10A"),
    ("Ravi", "R002", "10A"),
    ("Sana", "R003", "10B")
]

for name, roll_no, student_class in students:
    try:
        cursor.execute("INSERT INTO students (name, roll_no, class) VALUES (?, ?, ?)",
                       (name, roll_no, student_class))
    except sqlite3.IntegrityError:
        print(f"⚠️ Student with roll number {roll_no} already exists.")

print("✅ Students inserted.")

# --------------------------
# 2. Insert Subjects
# --------------------------
subjects = [
    ("Math", "MATH"),
    ("Science", "SCI"),
    ("English", "ENG")
]

for subject_name, subject_code in subjects:
    try:
        cursor.execute("INSERT INTO subjects (name, code) VALUES (?, ?)",
                       (subject_name, subject_code))
    except sqlite3.IntegrityError:
        print(f"⚠️ Subject with code {subject_code} already exists.")

print("✅ Subjects inserted.")

# --------------------------
# 3. Insert Grades
# --------------------------

# First, fetch student and subject IDs
cursor.execute("SELECT id, roll_no FROM students")
student_map = {roll_no: student_id for student_id, roll_no in cursor.fetchall()}

cursor.execute("SELECT id, code FROM subjects")
subject_map = {code: subject_id for subject_id, code in cursor.fetchall()}

# Now insert grades using those IDs
grades = [
    # (roll_no, subject_code, marks, exam_type)
    ("R001", "MATH", 88, "midterm"),
    ("R001", "SCI", 91, "midterm"),
    ("R001", "ENG", 85, "midterm"),
    
    ("R002", "MATH", 74, "midterm"),
    ("R002", "SCI", 79, "midterm"),
    ("R002", "ENG", 68, "midterm"),
    
    ("R003", "MATH", 95, "midterm"),
    ("R003", "SCI", 89, "midterm"),
    ("R003", "ENG", 93, "midterm")
]

for roll_no, subject_code, marks, exam_type in grades:
    student_id = student_map.get(roll_no)
    subject_id = subject_map.get(subject_code)
    if student_id and subject_id:
        cursor.execute("""
            INSERT INTO grades (student_id, subject_id, marks, exam_type)
            VALUES (?, ?, ?, ?)
        """, (student_id, subject_id, marks, exam_type))

print("✅ Grades inserted.")

# Commit and close
conn.commit()
conn.close()
print("🎉 All data inserted successfully.")
