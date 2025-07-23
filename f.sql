CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT UNIQUE,
    class TEXT
);
INSERT INTO students (name, roll_no, class)
VALUES ('Arshil', 'R001', '10A');
SELECT * FROM students;
