import sqlite3
import matplotlib.pyplot as plt
import csv
from fpdf import FPDF
import os

def generate_report(roll_no):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Get student info
    cursor.execute("SELECT id, name, class FROM students WHERE roll_no = ?", (roll_no,))
    student = cursor.fetchone()

    if student is None:
        print(" Student not found.")
        conn.close()
        return

    student_id, name, student_class = student

    # Get grades and subjects
    cursor.execute("""
        SELECT subjects.name, grades.marks, grades.exam_type
        FROM grades
        JOIN subjects ON grades.subject_id = subjects.id
        WHERE grades.student_id = ?
    """, (student_id,))
    results = cursor.fetchall()
    conn.close()

    if not results:
        print(" No grades found for this student.")
        return

    # Console output
    print("\n====== STUDENT REPORT ======")
    print(f"Name    : {name}")
    print(f"Roll No : {roll_no}")
    print(f"Class   : {student_class}")
    print("-" * 40)
    print(f"{'Subject':<15} {'Exam Type':<10} {'Marks'}")
    print("-" * 40)

    subjects = []
    marks = []
    csv_data = []

    for subject_name, mark, exam_type in results:
        display_label = f"{subject_name} ({exam_type})"
        print(f"{subject_name:<15} {exam_type:<10} {mark}")
        subjects.append(display_label)
        marks.append(mark)
        csv_data.append([subject_name, exam_type, mark])

    # ======  CUSTOMIZED CHART GENERATION ======
    plt.style.use('ggplot')  # or try 'bmh', 'classic', etc.
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(subjects, marks, color='royalblue', edgecolor='black')

    ax.set_title(f"{name}'s Grade Report", fontsize=16, fontweight='bold')
    ax.set_xlabel("Subjects & Exams", fontsize=12)
    ax.set_ylabel("Marks", fontsize=12)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    ax.set_ylim(0, max(marks) + 10)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval + 1, f'{yval}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    chart_filename = f"{roll_no}_chart.png"
    plt.savefig(chart_filename, dpi=300)
    plt.close()
    print(f"Chart saved as {chart_filename}")

    # ====== 📁 EXPORT TO CSV ======
    csv_filename = f"student_report_{roll_no}.csv"
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Subject", "Exam Type", "Marks"])
        writer.writerows(csv_data)
    print(f" CSV saved as {csv_filename}")

    # ======  EXPORT TO PDF ======
    pdf_filename = f"student_report_{roll_no}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt=" Student Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {name} | Roll No: {roll_no} | Class: {student_class}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", size=11)
    pdf.cell(60, 8, "Subject", border=1)
    pdf.cell(40, 8, "Exam Type", border=1)
    pdf.cell(30, 8, "Marks", border=1)
    pdf.ln()

    for row in csv_data:
        pdf.cell(60, 8, row[0], border=1)
        pdf.cell(40, 8, row[1], border=1)
        pdf.cell(30, 8, str(row[2]), border=1)
        pdf.ln()

    if os.path.exists(chart_filename):
        pdf.image(chart_filename, x=10, y=pdf.get_y() + 10, w=180)

    pdf.output(pdf_filename)
    print(f" PDF saved as {pdf_filename}")
