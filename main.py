import sqlite3
import report   # make sure report.py is in same folder
from login import login_user

def show_menu():
    print("\n====== STUDENT GRADING SYSTEM ======")
    print("1. Add New Student")
    print("2. Add New Subject")
    print("3. Add Grades")
    print("4. View Student Report")
    print("5. Delete Student")
    print("6. Exit")

def add_student():
    name = input("Enter student name: ").strip()
    roll_no = input("Enter roll number: ").strip().upper()
    student_class = input("Enter class (e.g. 10A): ").strip()

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO students (name, roll_no, class) VALUES (?, ?, ?)",
                       (name, roll_no, student_class))
        conn.commit()
        print("✅ Student added successfully.")
    except sqlite3.IntegrityError:
        print("⚠️ Roll number already exists. Try again.")
    finally:
        conn.close()

def add_subject():
    subject_name = input("Enter subject name: ").strip()
    subject_code = input("Enter subject code (e.g. MATH, ENG): ").strip().upper()

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO subjects (name, code) VALUES (?, ?)", 
                       (subject_name, subject_code))
        conn.commit()
        print("✅ Subject added successfully.")
    except sqlite3.IntegrityError:
        print("⚠️ Subject code already exists.")
    finally:
        conn.close()

def add_grades():
    roll_no = input("Enter student roll number: ").strip().upper()
    subject_code = input("Enter subject code: ").strip().upper()
    
    try:
        marks = int(input("Enter marks: ").strip())
    except ValueError:
        print("❌ Please enter a valid number for marks.")
        return

    exam_type = input("Enter exam type (e.g. midterm, final): ").strip().lower()

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM students WHERE roll_no = ?", (roll_no,))
    student = cursor.fetchone()

    if student is None:
        print("❌ Student not found.")
        conn.close()
        return

    student_id = student[0]

    cursor.execute("SELECT id FROM subjects WHERE code = ?", (subject_code,))
    subject = cursor.fetchone()

    if subject is None:
        print("❌ Subject not found.")
        conn.close()
        return

    subject_id = subject[0]

    cursor.execute("""
        INSERT INTO grades (student_id, subject_id, marks, exam_type)
        VALUES (?, ?, ?, ?)
    """, (student_id, subject_id, marks, exam_type))

    conn.commit()
    conn.close()
    print("✅ Grade added successfully.")

def delete_student():
    roll_no = input("Enter roll number of the student to delete: ").strip().upper()

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM students WHERE roll_no = ?", (roll_no,))
    student = cursor.fetchone()

    if student is None:
        print("❌ Student not found.")
        conn.close()
        return

    student_id = student[0]

    confirm = input(f"⚠️ Are you sure you want to delete student '{roll_no}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("❌ Delete cancelled.")
        conn.close()
        return

    cursor.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    print(f"🗑️ Student '{roll_no}' and related grades deleted.")

def run_program():
    while True:
        show_menu()
        choice = input("Enter your choice (1–6): ").strip()

        if choice == '1':
            add_student()
        elif choice == '2':
            add_subject()
        elif choice == '3':
            add_grades()
        elif choice == '4':
            roll_no = input("Enter roll number to view report: ").strip().upper()
            report.generate_report(roll_no)
        elif choice == '5':
            delete_student()
        elif choice == '6':
            print("👋 Exiting. Thank you!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    role = login_user()
    if role:
        run_program()
    else:
        print("❌ Login failed. Exiting.")
