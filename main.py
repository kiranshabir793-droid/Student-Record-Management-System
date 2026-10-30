
import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db
from student import add_student, view_students, search_student, update_student

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Student Record Management System")
root.geometry("850x650")
root.configure(bg="#f0f4f8")
root.resizable(False, False)

# ================= COLORS =================
BLUE = "#1f3c88"
LIGHT_BLUE = "#eaf2ff"
BG = "#f0f4f8"
GREEN = "#198754"
RED = "#dc3545"

# ================= HEADER =================
header = tk.Frame(root, bg=BLUE, height=70)
header.pack(fill="x")
header.pack_propagate(False)

heading = tk.Label(
    header,
    text="STUDENT RECORD MANAGEMENT SYSTEM",
    font=("Arial", 18, "bold"),
    bg=BLUE,
    fg="white"
)
heading.pack(expand=True)

# ================= STUDENT FORM =================
form = tk.LabelFrame(
    root,
    text=" Student Registration ",
    font=("Arial", 11, "bold"),
    bg="white",
    fg=BLUE,
    padx=15,
    pady=8
)
form.pack(padx=30, pady=10, fill="x")

# Student Name
tk.Label(
    form,
    text="Student Name:",
    bg="white",
    fg=BLUE,
    font=("Arial", 10, "bold")
).grid(row=0, column=0, padx=10, pady=6, sticky="w")


name_entry = tk.Entry(
    form,
    width=30,
    font=("Arial", 10),
    bg=LIGHT_BLUE,
    relief="solid",
    bd=1
)


name_entry.grid(row=0, column=1, padx=10, pady=6, sticky="w")

# Age
tk.Label(
    form,
    text="Age:",
    bg="white",
    fg=BLUE,
    font=("Arial", 10, "bold")
).grid(row=1, column=0, padx=10, pady=6, sticky="w")


age_entry = tk.Entry(
    form,
    width=30,
    font=("Arial", 10),
    bg=LIGHT_BLUE,
    relief="solid",
    bd=1
)

age_entry.grid(row=1, column=1, padx=10, pady=6, sticky="w")

# Gender
tk.Label(
    form,
    text="Gender:",
    bg="white",
    fg=BLUE,
    font=("Arial", 10, "bold")
).grid(row=2, column=0, padx=10, pady=6, sticky="w")

gender_box = ttk.Combobox(
    form,
    values=["Male", "Female", "Other"],
    width=28,
    state="readonly",
    font=("Arial", 10)
)
gender_box.grid(row=2, column=1, padx=10, pady=6, sticky="w")
gender_box.set("Select Gender")

# Email
tk.Label(
    form,
    text="Email:",
    bg="white",
    fg=BLUE,
    font=("Arial", 10, "bold")
).grid(row=3, column=0, padx=10, pady=6, sticky="w")


email_entry = tk.Entry(
    form,
    width=30,
    font=("Arial", 10),
    bg=LIGHT_BLUE,
    relief="solid",
    bd=1
)


email_entry.grid(row=3, column=1, padx=10, pady=6, sticky="w")



# GPA
tk.Label(
    form,
    text="GPA:",
    bg="white",
    fg=BLUE,
    font=("Arial", 10, "bold")
).grid(row=4, column=0, padx=10, pady=6, sticky="w")

gpa_entry = tk.Entry(
    form,
    width=30,
    font=("Arial", 10),
    bg=LIGHT_BLUE,
    relief="solid",
    bd=1
)

gpa_entry.grid(row=4, column=1, padx=10, pady=6, sticky="w")




tk.Label(
    form,
    text="Roll Number:",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=BLUE
).grid(
    row=5,
    column=0,
    padx=10,
    pady=6,
    sticky="w"
)



# Roll Number Entry
roll_number_entry = tk.Entry(
    form,
    width=30,
    font=("Arial", 10),
    bg=LIGHT_BLUE,
    relief="solid",
    bd=1
)

roll_number_entry.grid(
    row=5,
    column=1,
    padx=10,
    pady=6,
    sticky="w"
)



# Grade Label
tk.Label(
    form,
    text="Grade:",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=BLUE
).grid(
    row=6,
    column=0,
    padx=10,
    pady=6,
    sticky="w"
)



# Grade Dropdown
grade_box = ttk.Combobox(
    form,
    values=["A+", "A", "B", "C", "D", "F"],
    width=27,
    font=("Arial", 10),
    state="readonly"
)

grade_box.grid(
    row=6,
    column=1,
    padx=10,
    pady=6,
    sticky="w"
)

grade_box.set("Select Grade")






# ================= SEARCH SECTION =================
search_frame = tk.Frame(root, bg=BG)
search_frame.pack(pady=5)

tk.Label(
    search_frame,
    text="Search by ID or Name:",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=BLUE
).grid(row=0, column=0, padx=8)


search_entry = tk.Entry(
    search_frame,
    width=15,
    font=("Arial", 10),
    relief="solid",
    bd=1
)


search_entry.grid(row=0, column=1, padx=8)

# ================= FUNCTIONS =================
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_box.set("Select Gender")
    email_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)


def show_students():
    for row in student_table.get_children():
        student_table.delete(row)

    for student in view_students():
        student_table.insert("", tk.END, values=student)




def save_student():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_box.get()
    email = email_entry.get().strip()
    gpa_text = gpa_entry.get().strip()
    roll_number = roll_number_entry.get().strip()
    grade = grade_box.get()

    # Check required fields
    if (
        not name
        or not age
        or gender == "Select Gender"
        or not email
        or not gpa_text
        or not roll_number
        or grade == "Select Grade"
    ):
        messagebox.showerror(
            "Error",
            "Please fill in all fields!"
        )
        return

    # Age validation
    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror(
            "Invalid Age",
            "Please enter a valid age!"
        )
        return

    # GPA validation
    try:
        gpa = float(gpa_text)

        if not 0.0 <= gpa <= 4.0:
            messagebox.showerror(
                "Invalid GPA",
                "GPA must be between 0.0 and 4.0!"
            )
            return

    except ValueError:
        messagebox.showerror(
            "Invalid GPA",
            "Please enter a valid GPA, e.g. 3.5"
        )
        return

    # Email validation
    if (
        "@" not in email
        or "." not in email.split("@")[-1]
        or " " in email
    ):
        messagebox.showerror(
            "Invalid Email",
            "Please enter a valid email address!"
        )
        return

    # Save student
    try:
        result = add_student(
            name,
            int(age),
            gender,
            email,
            gpa,
            roll_number,
            grade
        )

        if result is False:
            messagebox.showwarning(
                "Duplicate Record",
                "This student or roll number already exists!"
            )
            return

        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

        clear_fields()
        show_students()

    except Exception as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )


        
def update_student_record():
    student_id = search_entry.get().strip()

    if not student_id.isdigit():
        messagebox.showerror(
            "Error",
            "Please enter a valid Student ID in the Search box!"
        )
        return

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_box.get()
    email = email_entry.get().strip()
    gpa_text = gpa_entry.get().strip()
    roll_number = roll_number_entry.get().strip()
    grade = grade_box.get()

    if (
        not name or not age or gender == "Select Gender"
        or not email or not gpa_text or not roll_number
        or grade == "Select Grade"
    ):
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror("Invalid Age", "Enter a valid age!")
        return

    if (
        "@" not in email
        or "." not in email.split("@")[-1]
        or " " in email
    ):
        messagebox.showerror("Invalid Email", "Enter a valid email!")
        return

    try:
        gpa = float(gpa_text)

        if not 0.0 <= gpa <= 4.0:
            messagebox.showerror(
                "Invalid GPA", "GPA must be between 0.0 and 4.0!"
            )
            return

        student = search_student(int(student_id))

        if not student:
            messagebox.showerror(
                "Not Found", "Student ID not found!"
            )
            return

        result = update_student(
            int(student_id),
            name,
            int(age),
            gender,
            email,
            gpa,
            roll_number,
            grade
        )

        if result:
            messagebox.showinfo(
                "Success", "Student record updated successfully!"
            )
            show_students()
        else:
            messagebox.showwarning(
                "No Changes", "No record was updated."
            )

    except ValueError:
        messagebox.showerror("Invalid GPA", "Enter a valid GPA, e.g. 3.5")
    except Exception as error:
        messagebox.showerror("Update Error", str(error))


        
def search_student_record():
    search_value = search_entry.get().strip()

    if not search_value:
        messagebox.showerror("Error", "Please enter Student ID or Name!")
        return

    try:
        student = None

        # Search by Student ID if input is a number
        if search_value.isdigit():
            student = search_student(int(search_value))

        else:
            # Search by Student Name
            connection = connect_db()
            cursor = connection.cursor()

            try:
                cursor.execute(
                    "SELECT * FROM students WHERE name LIKE ?",
                    (f"%{search_value}%",)
                )
                student = cursor.fetchall()
            finally:
                connection.close()

        # Clear old table records
        for row in student_table.get_children():
            student_table.delete(row)

        # Display search results
        if student:
            if isinstance(student, list):
                for record in student:
                    student_table.insert("", tk.END, values=record)
            else:
                student_table.insert("", tk.END, values=student)
        else:
            messagebox.showinfo("Search", "Student not found!")

    except Exception as error:
        messagebox.showerror("Error", str(error))



# ================= BUTTONS =================
button_frame = tk.Frame(root, bg=BG)
button_frame.pack(pady=8)

tk.Button(
    button_frame,
    text="Add Student",
    bg=GREEN,
    fg="white",
    font=("Arial", 10, "bold"),
    width=15,
    cursor="hand2",
    command=save_student
).grid(row=0, column=0, padx=6)

tk.Button(
    button_frame,
    text="View Students",
    bg=BLUE,
    fg="white",
    font=("Arial", 10, "bold"),
    width=15,
    cursor="hand2",
    command=show_students
).grid(row=0, column=1, padx=6)

tk.Button(
    button_frame,
    text="Clear",
    bg=RED,
    fg="white",
    font=("Arial", 10, "bold"),
    width=15,
    cursor="hand2",
    command=clear_fields
).grid(row=0, column=2, padx=6)


tk.Button(
    button_frame,
    text="Update Student",
    bg="#e69500",
    fg="white",
    font=("Arial", 10, "bold"),
    width=15,
    cursor="hand2",
    command=update_student_record
).grid(row=0, column=3, padx=6)



tk.Button(
    search_frame,
    text="Search",
    bg=BLUE,
    fg="white",
    font=("Arial", 10, "bold"),
    cursor="hand2",
    command=search_student_record
).grid(row=0, column=2, padx=8)

# ================= STUDENTS TABLE =================
table_frame = tk.Frame(root, bg="white")
table_frame.pack(padx=30, pady=10, fill="both", expand=True)

columns = (
    "ID",
    "Name",
    "Age",
    "Gender",
    "Email",
    "GPA",
    "Roll Number",
    "Grade"
)

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=7
)

student_table.pack(fill="both", expand=True)

column_widths = {
"ID": 45,
"Name": 100,
"Age": 55,
"Gender": 75,
"Email": 140,
"GPA": 55,
"Roll Number": 100,
"Grade": 60
}

for column in columns:
    student_table.heading(column, text=column)
    student_table.column(column, width=column_widths[column], anchor="center")


# ================= LOAD RECORDS =================

show_students()

# ================= RUN APPLICATION =================
print(view_students())
root.mainloop()
