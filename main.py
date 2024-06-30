import tkinter as tk
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
import mysql.connector
from datetime import datetime

# Main window
super = tk.Tk()
super.title("Employee Main Window")
super.resizable(False, False)
super.geometry("1000x330")

def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin21",
            database="employee_management"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", f"Error: {err}")
        return None

# Employee Login page start
def but_emp_log():
    def logged_emp():
        username = entry_employee_id.get()
        password = entry_employee_password.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Required fields cannot be left empty")
            return
        
        conn = connect_to_db()
        if conn is None:
            return

        cursor = conn.cursor()
        query = 'SELECT * FROM employees WHERE emp_id = %s AND emp_password = %s'
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            user_data = f"Employee ID: {user[0]}\nEmployee Name: {user[1]}\nEmployee Email: {user[5]}\nContact Number: {user[6]}"
            messagebox.showinfo("Login Successful", f"Login Successful\n\nUser Data:\n{user_data}")
        else:
            messagebox.showerror("Login", "Invalid Username or Password")

    master = tk.Toplevel(super)
    master.title("Employee Login")
    master.resizable(False, False)
    master.geometry("500x220")

    emplogo = Image.open(r"/Users/anshsharma/Desktop/develop/python/EMS/employee.png")
    emplogo = emplogo.resize((150, 150))
    emplogo = ImageTk.PhotoImage(emplogo)
    label1 = tk.Label(master, image=emplogo)
    label1.image = emplogo  # Keep a reference to avoid garbage collection
    label1.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

    tk.Label(master, text="Employee ID", font=("Helvetica", 15, "bold")).grid(row=0, column=1, padx=5, pady=5)
    entry_employee_id = tk.Entry(master, borderwidth=3, bg="black", fg="lavender")
    entry_employee_id.grid(row=0, column=2, padx=2, pady=5)

    tk.Label(master, text="Password", font=("Helvetica", 15, "bold")).grid(row=1, column=1, padx=5, pady=5)
    entry_employee_password = tk.Entry(master, borderwidth=3, bg="black", fg="lavender", show='*')
    entry_employee_password.grid(row=1, column=2, padx=5, pady=5)

    log_button = tk.Button(master, text="Login", command=logged_emp, font=("Helvetica", 15, "bold"))
    log_button.grid(row=2, column=0, columnspan=3)

    master.mainloop()
# End here (Employee login page)

# Employee Attendance box
def but_Emp_Attend():
    def add_record(employee_id, name, check_in_time, check_out_time):
        conn = connect_to_db()
        if conn is None:
            return
        try:
            cursor = conn.cursor()
            date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('''INSERT INTO attendance (emp_id, employee_name, date, check_in_time, check_out_time)
                            VALUES (%s, %s, %s, %s, %s)''',
                        (employee_id, name, date, check_in_time, check_out_time))
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Insert Error", f"Error: {err}")
        finally:
            conn.close()

    def check_in():
        employee_id = entry_employee_id.get()
        name = entry_name.get()
        if not employee_id or not name:
            messagebox.showwarning("Input Error", "Please enter Employee ID and Name")
            return

        check_in_time = datetime.now().strftime('%H:%M:%S')
        add_record(employee_id, name, check_in_time, None)
        messagebox.showinfo("Check-In", f"{name} checked in at {check_in_time}")

    def check_out():
        employee_id = entry_employee_id.get()
        name = entry_name.get()
        if not employee_id or not name:
            messagebox.showwarning("Input Error", "Please enter Employee ID and Name")
            return

        check_out_time = datetime.now().strftime('%H:%M:%S')
        conn = connect_to_db()
        if conn is None:
            return
        try:
            cursor = conn.cursor()
            date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('''UPDATE attendance
                            SET check_out_time = %s
                            WHERE emp_id = %s AND date = %s AND check_out_time IS NULL''',
                        (check_out_time, employee_id, date))
            if cursor.rowcount == 0:
                messagebox.showwarning("Check-Out Error", "No check-in record found for today.")
            else:
                conn.commit()
                messagebox.showinfo("Check-Out", f"{name} checked out at {check_out_time}")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Update Error", f"Error: {err}")
        finally:
            conn.close()

    root = tk.Toplevel(super)
    root.resizable(False, False)
    root.title("Attendance and Time Tracking")

    tk.Label(root, text="Employee ID:", fg="lavender", font=("Helvetica", 15, "bold")).grid(row=0, column=0, padx=10, pady=10)
    entry_employee_id = tk.Entry(root, borderwidth=3, bg="black", fg="lavender")
    entry_employee_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Name:", fg="lavender", font=("Helvetica", 15, "bold")).grid(row=1, column=0, padx=10, pady=10)
    entry_name = tk.Entry(root, borderwidth=3, bg="black", fg="lavender")
    entry_name.grid(row=1, column=1, padx=10, pady=10) 

    btn_check_in = tk.Button(root, text="Check In", command=check_in, font=("Helvetica", 15, "bold"))
    btn_check_in.grid(row=2, column=0, padx=10, pady=10)

    btn_check_out = tk.Button(root, text="Check Out", command=check_out, font=("Helvetica", 15, "bold"))
    btn_check_out.grid(row=2, column=1, padx=10, pady=10)

    root.mainloop()
# end here (Attendance box)

# Add new employee start from here
def New_emp():
    def add_employee():
        emp_id = entry_employee_id.get()
        emp_full_name = entry_full_name.get()
        emp_gender = value_inside.get()
        emp_position = position_inside.get()
        emp_department = entry_emp_department.get()
        emp_email = entry_emp_email.get()
        contact_no = entry_contact_no.get()
        emp_password = entry_password.get()
        emp_address = entry_emp_address.get()

        if not emp_full_name or not emp_address or not contact_no or not emp_id:
            messagebox.showerror("Input Error", "All fields should be filled")
            return

        conn = connect_to_db()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO employees (emp_id, emp_name, emp_gender, emp_position,
                            emp_dep, emp_email, emp_contact, emp_password, emp_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                            (emp_id, emp_full_name, emp_gender, emp_position, emp_department, emp_email, contact_no, emp_password, emp_address))
            conn.commit()
            messagebox.showinfo("Success", f"Employee {emp_full_name} added successfully")
            clear_entries()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            conn.close()

    def clear_entries():
        entry_employee_id.delete(0, tk.END)
        entry_full_name.delete(0, tk.END)
        value_inside.set("Option")
        position_inside.set("Select")
        entry_emp_department.delete(0, tk.END)
        entry_emp_email.delete(0, tk.END)
        entry_contact_no.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_emp_address.delete(0, tk.END)

    root = tk.Toplevel(super)
    root.title("Employee Database Management")
    root.resizable(False, False)

    tk.Label(root, text="Employee ID:", fg="lavender").grid(row=0, column=0, padx=2, pady=5, sticky="w")
    entry_employee_id = tk.Entry(root, borderwidth=3, bg="black", fg="lavender")
    entry_employee_id.grid(row=0, column=1, padx=2, pady=5, sticky="ew")

    tk.Label(root, text="Full Name:", fg="lavender").grid(row=1, column=0, padx=2, pady=5, sticky="w")
    entry_full_name = tk.Entry(root, borderwidth=3)
    entry_full_name.grid(row=1, column=1, padx=2, pady=5, sticky="ew")

    tk.Label(root, text="Gender", fg="lavender").grid(row=2, column=0, padx=2, pady=5, sticky="w")
    option_gender = ["Male", "Female", "Other"]
    value_inside = tk.StringVar(root)
    value_inside.set("Option")
    question_menu = tk.OptionMenu(root, value_inside, *option_gender)
    question_menu.grid(row=2, column=1, padx=2, pady=5)

    tk.Label(root, text="Position:", fg="lavender").grid(row=3, column=0, padx=2, pady=5, sticky="w")
    option_position = ["Salesman", "Testing Engineer", "Senior Developer", "Junior Developer", "Database Architect"]
    position_inside = tk.StringVar(root)
    position_inside.set("Select")
    position_menu = tk.OptionMenu(root, position_inside, *option_position)
    position_menu.grid(row=3, column=1, padx=2, pady=5)

    tk.Label(root, text="Department:", fg="lavender").grid(row=4, column=0, padx=2, pady=5, sticky="w")
    entry_emp_department = tk.Entry(root, borderwidth=3)
    entry_emp_department.grid(row=4, column=1, padx=2, pady=10, sticky="ew")

    tk.Label(root, text="Email:", fg="lavender").grid(row=5, column=0, padx=2, pady=5, sticky="w")
    entry_emp_email = tk.Entry(root, borderwidth=3)
    entry_emp_email.grid(row=5, column=1, padx=2, pady=5, sticky="ew")

    tk.Label(root, text="Contact Number:", fg="lavender").grid(row=6, column=0, padx=2, pady=5, sticky="w")
    entry_contact_no = tk.Entry(root, borderwidth=3)
    entry_contact_no.grid(row=6, column=1, padx=2, pady=5, sticky="ew")

    tk.Label(root, text="Password:", fg="lavender").grid(row=7, column=0, padx=2, pady=5, sticky="w")
    entry_password = tk.Entry(root, borderwidth=3, show='*')
    entry_password.grid(row=7, column=1, padx=2, pady=5, sticky="ew")

    tk.Label(root, text="Employee Address:", fg="lavender").grid(row=8, column=0, padx=2, pady=5, sticky="w")
    entry_emp_address = tk.Entry(root, borderwidth=3)
    entry_emp_address.grid(row=8, column=1, padx=2, pady=5, sticky="ew")

    button1 = tk.Button(root, text="Add Employee", command=add_employee, fg="green")
    button1.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

    root.mainloop()
# Add New employee end here

# View employee box start from here
def View_emp():
    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT emp_id, emp_name, emp_position, emp_dep FROM employees")
    records = cursor.fetchall()
    conn.close()

    for i in tree.get_children():
        tree.delete(i)

    for row in records:
        tree.insert("", "end", values=row)
# End of view employee

Emp_login = tk.Button(super, text="New Employee", command=New_emp, font=("Helvetica", 15, "bold"), height=4, width=17)
Emp_login.grid(row=0, column=0)

Emp_create = tk.Button(super, text="View All Employee", command=View_emp, font=("Helvetica", 15, "bold"), height=4, width=17)
Emp_create.grid(row=1, column=0)

Emp_view = tk.Button(super, text="Employee Login", command=but_emp_log, font=("Helvetica", 15, "bold"), height=4, width=17)
Emp_view.grid(row=2, column=0)

Emp_attend = tk.Button(super, text="Attendance Here", command=but_Emp_Attend, font=("Helvetica", 15, "bold"), height=4, width=17)
Emp_attend.grid(row=3, column=0)

tree = ttk.Treeview(super, columns=("Employee ID", "Name", "Position", "Department"), show='headings', height=16)
tree.heading("Employee ID", text="Employee ID")
tree.heading("Name", text="Name")
tree.heading("Position", text="Position")
tree.heading("Department", text="Department")
tree.grid(row=0, column=1, rowspan=4)

super.mainloop()
