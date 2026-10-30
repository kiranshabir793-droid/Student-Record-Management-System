
from database import connect_db


def add_student(name, age, gender, email, gpa, roll_number="", grade="F"):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM students WHERE name = ? AND email = ?",
            (name, email)
        )

        if cursor.fetchone():
            return False

        if roll_number:
            cursor.execute(
                "SELECT id FROM students WHERE roll_number = ?",
                (roll_number,)
            )

            if cursor.fetchone():
                return False

        cursor.execute(
            """
            INSERT INTO students
            (name, age, gender, email, gpa, roll_number, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (name, age, gender, email, gpa, roll_number, grade)
        )

        connection.commit()
        return True

    finally:
        connection.close()


def search_student(student_id):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )
        return cursor.fetchone()

    finally:
        connection.close()


def update_student(student_id, name, age, gender, email, gpa, roll_number, grade):
    connection = connect_db()
    cursor = connection.cursor()

    try:

    
        if roll_number:
            cursor.execute(
                "SELECT id FROM students WHERE roll_number = ? AND id != ?",
                (roll_number, student_id)
            )

            if cursor.fetchone():
                return False


        cursor.execute(
            """
            UPDATE students
            SET name = ?,
                age = ?,
                gender = ?,
                email = ?,
                gpa = ?,
                roll_number = ?,
                grade = ?
            WHERE id = ?
            """,
            (name, age, gender, email, gpa, roll_number, grade, student_id)
        )

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()


def view_students():
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM students")
        return cursor.fetchall()

    finally:
        connection.close()

