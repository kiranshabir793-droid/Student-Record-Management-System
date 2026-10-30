import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess
import sys

# Main Dashboard Window
root = tk.Tk()
root.title("Student Record Management System")
root.geometry("1000x650")
root.configure(bg="#F3F6FA")

# Colors
NAVY = "#172554"
BLUE = "#2563EB"
WHITE = "#FFFFFF"
BG = "#F3F6FA"
TEXT = "#1E293B"


# Theme Mode
dark_mode = False

def toggle_dark_mode():
    global dark_mode

    dark_mode = not dark_mode


    if dark_mode:
        root.configure(bg="#1E293B")
        content.configure(bg="#1E293B")
        theme_btn.config(text="☀️ Light Mode")
    else:
        root.configure(bg=BG)
        content.configure(bg=BG)
        theme_btn.config(text="🌙 Dark Mode")

    
theme_btn = tk.Button(
    root,
    text="🌙 Dark Mode",
    command=toggle_dark_mode,
    bg=WHITE,
    fg=NAVY,
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2"
)



# Total Students Count
def get_total_students():
    try:
        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        total = cursor.fetchone()[0]
        connection.close()
        return total

    except sqlite3.Error:
        return 0


# Open Registration Window
def open_registration():
    try:
        subprocess.Popen([sys.executable, "main.py"])
    except Exception as error:
        messagebox.showerror("Error", str(error))


# View Students
def view_students():
    window = tk.Toplevel(root)
    window.title("All Students")
    window.geometry("1200x500")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="ALL STUDENTS",
        font=("Arial", 18, "bold"),
        bg=BG,
        fg=NAVY
    ).pack(pady=15)

    
    columns = ("ID", "Name", "Age", "Gender", "Email", "GPA", "Roll Number", "Grade")

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    
    
    for column in columns:
        table.heading(column, text=column)

    table.column("ID", width=50, anchor="center")
    table.column("Name", width=150, anchor="center")
    table.column("Age", width=60, anchor="center")
    table.column("Gender", width=100, anchor="center")
    table.column("Email", width=250, anchor="center")
    table.column("GPA", width=80, anchor="center")
    table.column("Roll Number", width=140, anchor="center")
    table.column("Grade", width=100, anchor="center")

    table.pack(fill="both", expand=True, padx=20, pady=15)



    try:
        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()

        cursor.execute(
    "SELECT id, name, age, gender, email, gpa, roll_number, grade FROM students"
)
        for record in cursor.fetchall():
            table.insert("", "end", values=record)

        connection.close()

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))


# Search Student
def search_student_window():
    window = tk.Toplevel(root)
    window.title("Search Student")
    window.geometry("450x300")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="SEARCH STUDENT",
        font=("Arial", 18, "bold"),
        bg=BG,
        fg=NAVY
    ).pack(pady=(25, 15))

    tk.Label(
        window,
        text="Enter Student ID:",
        font=("Arial", 12),
        bg=BG,
        fg=TEXT
    ).pack(pady=5)

    student_id_entry = tk.Entry(
        window,
        font=("Arial", 11),
        width=20,
        bg="#E8EEF7",
        fg=TEXT,
        relief="solid",
        bd=1
    )
    student_id_entry.pack(pady=5)

    def search_record():
        student_id = student_id_entry.get().strip()

        if not student_id:
            messagebox.showwarning(
                "Warning", "Please enter Student ID."
            )
            return

        if not student_id.isdigit():
            messagebox.showwarning(
                "Warning", "Student ID must be a number."
            )
            return

        try:
            connection = sqlite3.connect("students.db")
            cursor = connection.cursor()

            
            cursor.execute(
            """
            SELECT id, name, age, gender, email, gpa, roll_number, grade
            FROM students
            WHERE id = ?
            """,
            (int(student_id),)
)


            
                         

            record = cursor.fetchone()
            connection.close()

            if record:
                messagebox.showinfo(
                    "Student Found",
                    f"Student ID: {record[0]}\n"
                    f"Name: {record[1]}\n"
                    f"Age: {record[2]}\n"
                    f"Gender: {record[3]}\n"
                    f"Email: {record[4]}"
                    f"GPA: {record[5]}\n"
                    f"Roll Number: {record[6]}\n"
                    f"Grade: {record[7]}"
                )
            else:
                messagebox.showwarning(
                    "Not Found", "Student ID not found."
                )

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    tk.Button(
        window,
        text="Search Student",
        command=search_record,
        font=("Arial", 11, "bold"),
        bg=BLUE,
        fg=WHITE,
        relief="flat",
        padx=15,
        pady=8
    ).pack(pady=20)


# Update Student
def update_student_window():
    window = tk.Toplevel(root)
    window.title("Update Student")
    window.geometry("450x650")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="UPDATE STUDENT",
        font=("Arial", 18, "bold"),
        bg=BG,
        fg=NAVY
    ).pack(pady=12)

    tk.Label(
        window,
        text="Student ID:",
        bg=BG,
        fg=TEXT
    ).pack()

    id_entry = tk.Entry(
        window,
        width=20,
        font=("Arial", 11),
        bg="#E8EEF7",
        relief="solid",
        bd=1
    )
    id_entry.pack(pady=5)

    fields = {}

    for label_text in ["Name", "Age", "Gender", "Email", "GPA", "Roll Number", "Grade"]:

        tk.Label(
            window,
            text=label_text + ":",
            font=("Arial", 10, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=(4, 1))

        entry = tk.Entry(
            window,
            width=25,
            font=("Arial", 10),
            bg="#E8EEF7",
            relief="solid",
            bd=1
        )
        entry.pack(pady=3)

        fields[label_text] = entry

    # Load Student Details
    def load_student():
        student_id = id_entry.get().strip()

        if not student_id.isdigit():
            messagebox.showwarning(
                "Warning", "Enter a valid Student ID."
            )
            return

        connection = sqlite3.connect("students.db")

        try:
            cursor = connection.cursor()

            
            cursor.execute(
            """
            SELECT name, age, gender, email, gpa, roll_number, grade
            FROM students
            WHERE id = ?
            """,
           (int(student_id),)
)



            record = cursor.fetchone()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))
            return

        finally:
            connection.close()

        if not record:
            messagebox.showwarning(
                "Not Found", "Student ID not found."
            )
            return

        for entry, value in zip(fields.values(), record):
            entry.delete(0, tk.END)
            entry.insert(
                0, "" if value is None else str(value)
            )

    # Save Updated Details
    def save_changes():
        student_id = id_entry.get().strip()

        if not student_id.isdigit():
            messagebox.showwarning(
                "Warning", "Enter a valid Student ID."
            )
            return

        values = [
            fields[name].get().strip()
            for name in fields
        ]

        if not all(values):
            messagebox.showwarning(
                "Warning", "Please fill in all fields."
            )
            return

        if not values[1].isdigit() or int(values[1]) <= 0:
            messagebox.showwarning(
                "Warning", "Enter a valid age."
            )
            return

        try:
            gpa = float(values[4])

            if not 0.0 <= gpa <= 4.0:
                messagebox.showwarning(
                    "Warning", "GPA must be between 0.0 and 4.0."
                )
                return

        except ValueError:
            messagebox.showwarning(
                "Warning", "Enter a valid GPA, for example 3.5."
            )
            return

        connection = sqlite3.connect("students.db")

        try:
            cursor = connection.cursor()

            
            cursor.execute(
    """
    UPDATE students
    SET name = ?, age = ?, gender = ?,
        email = ?, gpa = ?, roll_number = ?, grade = ?
    WHERE id = ?
    """,
    (
        values[0],
        int(values[1]),
        values[2],
        values[3],
        gpa,
        values[5],
        values[6],
        int(student_id)
    )
)



            connection.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning(
                    "Not Found", "Student ID not found."
                )
            else:
                messagebox.showinfo(
                    "Success", "Student updated successfully!"
                )

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

        finally:
            connection.close()

    tk.Button(
        window,
        text="Load Student",
        command=load_student,
        bg=BLUE,
        fg=WHITE,
        relief="flat",
        padx=12,
        pady=6
    ).pack(pady=7)

    tk.Button(
        window,
        text="Save Changes",
        command=save_changes,
        bg=NAVY,
        fg=WHITE,
        relief="flat",
        padx=12,
        pady=6
    ).pack(pady=5)


# Delete Student
def delete_student_window():
    window = tk.Toplevel(root)
    window.title("Delete Student")
    window.geometry("450x300")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="DELETE STUDENT",
        font=("Arial", 18, "bold"),
        bg=BG,
        fg=NAVY
    ).pack(pady=(25, 15))

    tk.Label(
        window,
        text="Enter Student ID:",
        font=("Arial", 11, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=5)

    id_entry = tk.Entry(
        window,
        width=20,
        font=("Arial", 11),
        bg="#E8EEF7",
        relief="solid",
        bd=1
    )
    id_entry.pack(pady=5)

    def delete_record():
        student_id = id_entry.get().strip()

        if not student_id.isdigit():
            messagebox.showwarning(
                "Warning", "Please enter a valid Student ID."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete Student ID {student_id}?"
        )

        if not confirm:
            return

        connection = sqlite3.connect("students.db")

        try:
            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM students WHERE id = ?",
                (int(student_id),)
            )

            connection.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning(
                    "Not Found", "Student ID not found."
                )
            else:
                messagebox.showinfo(
                    "Success", "Student deleted successfully!"
                )
                id_entry.delete(0, tk.END)

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

        finally:
            connection.close()

    tk.Button(
        window,
        text="Delete Student",
        command=delete_record,
        font=("Arial", 11, "bold"),
        bg="#DC2626",
        fg=WHITE,
        relief="flat",
        padx=15,
        pady=8
    ).pack(pady=20)


# Future Features
def coming_soon(feature):
    messagebox.showinfo(
        feature,
        feature + " window will be added in the next step."
    )


# Sidebar
sidebar = tk.Frame(root, bg=NAVY, width=230)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="STUDENT\nMANAGEMENT",
    font=("Arial", 17, "bold"),
    bg=NAVY,
    fg=WHITE,
    justify="left"
).pack(pady=(35, 45), padx=20, anchor="w")


def sidebar_button(text, command):
    tk.Button(
        sidebar,
        text=text,
        command=command,
        font=("Arial", 11, "bold"),
        bg=NAVY,
        fg=WHITE,
        activebackground=BLUE,
        activeforeground=WHITE,
        relief="flat",
        anchor="w",
        padx=25,
        pady=12,
        cursor="hand2"
    ).pack(fill="x", padx=8, pady=3)


sidebar_button("🏠  Dashboard", lambda: None)
sidebar_button("➕  Registration", open_registration)
sidebar_button("📋  View Students", view_students)
sidebar_button("🔍  Search Student", search_student_window)
sidebar_button("✏️  Update Student", update_student_window)
sidebar_button("🗑️  Delete Student", delete_student_window)


# Main Content
content = tk.Frame(root, bg=BG)
content.pack(side="left", fill="both", expand=True)
theme_btn.place(relx=0.97, rely=0.03, anchor="ne")
theme_btn.lift()



tk.Label(
    content,
    text="Dashboard",
    font=("Arial", 26, "bold"),
    bg=BG,
    fg=NAVY
).pack(anchor="w", padx=35, pady=(35, 5))

tk.Label(
    content,
    text="Welcome to Student Record Management System",
    font=("Arial", 12),
    bg=BG,
    fg=TEXT
).pack(anchor="w", padx=35, pady=(0, 25))


# Total Students Card
card = tk.Frame(
    content,
    bg=WHITE,
    highlightthickness=1,
    highlightbackground="#DCE3ED"
)
card.pack(fill="x", padx=35, pady=10)

tk.Label(
    card,
    text="TOTAL REGISTERED STUDENTS",
    font=("Arial", 12, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", padx=25, pady=(22, 5))

total_label = tk.Label(
card,
text=str(get_total_students()),
font=("Arial", 34, "bold"),
bg=WHITE,
fg=BLUE
)
total_label.pack(anchor="w", padx=25, pady=(0, 22))

def refresh_total_students():
     total_label.config(text=str(get_total_students()))
     root.after(2000, refresh_total_students)

refresh_total_students()


# Quick Actions
tk.Label(
    content,
    text="Quick Actions",
    font=("Arial", 17, "bold"),
    bg=BG,
    fg=NAVY
).pack(anchor="w", padx=35, pady=(25, 10))


def action_button(text, command):
    tk.Button(
        content,
        text=text,
        command=command,
        font=("Arial", 12, "bold"),
        bg=BLUE,
        fg=WHITE,
        activebackground=NAVY,
        activeforeground=WHITE,
        relief="flat",
        padx=15,
        pady=12,
        cursor="hand2"
    ).pack(fill="x", padx=35, pady=6)


action_button("Register New Student", open_registration)
action_button("View All Students", view_students)


tk.Label(
    content,
    text="Student Record Management System | Python + Tkinter + SQLite",
    font=("Arial", 9),
    bg=BG,
    fg="#64748B"
).pack(side="bottom", pady=18)


root.mainloop()