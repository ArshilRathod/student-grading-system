import tkinter as tk
from tkinter import messagebox
import sqlite3
import main  # this is your main grading system functions

def login_action():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        login_window.destroy()
        main.run_program()  # Open your menu after successful login
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Tkinter window setup
login_window = tk.Tk()
login_window.title("Login - Student Grading System")
login_window.geometry("300x200")

tk.Label(login_window, text="Username").pack(pady=5)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

tk.Label(login_window, text="Password").pack(pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

tk.Button(login_window, text="Login", command=login_action).pack(pady=10)

login_window.mainloop()