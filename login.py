import sqlite3
import getpass


def signup_user():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    username = input("Enter new username: ").strip()
    password = input("Enter new password: ").strip()
    role = input("Enter role (admin/teacher): ").strip().lower()

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, password, role))
        conn.commit()
        print("✅ User registered successfully.")
    except sqlite3.IntegrityError:
        print("⚠️ Username already exists.")
    finally:
        conn.close()

def login_user():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()   # 🔒 Hides password while typing

    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"✅ Login successful. Welcome, {username} ({user[0]})")
        return user[0]  # return role
    else:
        print("❌ Invalid username or password.")
        return None
