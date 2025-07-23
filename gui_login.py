import tkinter as tk
from tkinter import messagebox
import sqlite3
import main  # to call run_program()

def check_credentials(username, password):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def login_action():
    uname = entry_username.get().strip()
    pword = entry_password.get().strip()
    result = check_credentials(uname, pword)

    if result:
        messagebox.showinfo("Login Successful", f"Welcome, {uname} ({result[0]})")
        window.destroy()
        main.run_program()  # Runs your grading system
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Tkinter GUI
window = tk.Tk()
window.title("Student Grading System - Login")
window.geometry("350x200")

tk.Label(window, text="Username:").pack(pady=5)
entry_username = tk.Entry(window)
entry_username.pack(pady=5)

tk.Label(window, text="Password:").pack(pady=5)
entry_password = tk.Entry(window, show="*")
entry_password.pack(pady=5)

tk.Button(window, text="Login", command=login_action).pack(pady=20)

window.mainloop()
            