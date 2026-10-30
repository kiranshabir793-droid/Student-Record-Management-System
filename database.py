import sqlite3


# Database se connection banane ka function
def connect_db():
    connection = sqlite3.connect("students.db")
    return connection


# Students ki table banane ka function


def create_table():
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                email TEXT,
                gpa REAL DEFAULT 0.0,
                roll_number TEXT,
                grade TEXT DEFAULT 'F'
            )
        """)

        # Check existing columns
        cursor.execute("PRAGMA table_info(students)")
        columns = [column[1] for column in cursor.fetchall()]

        # Add missing columns without deleting existing records
        if "gpa" not in columns:
            cursor.execute(
                "ALTER TABLE students ADD COLUMN gpa REAL DEFAULT 0.0"
            )

        if "roll_number" not in columns:
            cursor.execute(
                "ALTER TABLE students ADD COLUMN roll_number TEXT"
            )

        if "grade" not in columns:
            cursor.execute(
                "ALTER TABLE students ADD COLUMN grade TEXT DEFAULT 'F'"
            )

        # Unique index for non-empty roll numbers
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            unique_student_roll_number
            ON students(roll_number)
            WHERE roll_number IS NOT NULL
              AND roll_number != ''
        """)

        connection.commit()
        print("Database updated successfully!")

    except sqlite3.Error as error:
        connection.rollback()
        print("Database Error:", error)

    finally:
        connection.close()




# Function ko run karna
if __name__ == "__main__":
    create_table()
    print("Database and table created successfully!")