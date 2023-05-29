import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from tkinter import Toplevel
from tkinter import Label
from tkinter import simpledialog


# ................................Main window............................................................................................................
window = tk.Tk()
window.title("Data Entry Form")
window.geometry("800x500")
window.configure(bg="lightgray")
frame = tk.Frame(window)
frame.pack()
# ........................................MySQL database connection .......................................................................................
con = mysql.connector.connect(host='localhost', user='root', password='Nimish@1234')
cur = con.cursor(buffered=True)

# Create database and table
try:
    cur.execute('USE Student_Details')
except mysql.connector.Error as err:
    # if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        # Create the database if it doesn't exist
        cur.execute('CREATE DATABASE Student_Details')
        cur.execute('USE Student_Details')

        # Create the table
        cur.execute('''CREATE TABLE person_Details(
            id INT AUTO_INCREMENT PRIMARY KEY,
            firstname VARCHAR(255) NOT NULL,
            lastname VARCHAR(255) NOT NULL,
            title VARCHAR(10),
            age INT,
            state VARCHAR(255),
            mobile_number VARCHAR(10),
            ENGG_Branch VARCHAR(50),
            course_name VARCHAR(50),
            passout_year INT)''')
#.............................................Databse and table creation done....................................................................................

#..........................................Insert statement execution after pressing the Enter Data button...........................................................................................
def enter_data():
    accepted = accept_var.get()

    if accepted == "Accepted":
        # User info
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()

        
        title = title_combobox.get()
        age = age_spinbox.get()
        state = state_combobox.get()
        mobile_number = mobile_number_entry.get()

            # Course info
        Engg_Branch_name= Engg_branch_combobox.get()
        course_name = course_combobox.get()
        passout_year = passout_year_spinbox.get()

        if firstname and lastname and title and age and state and mobile_number and Engg_Branch_name and course_name and passout_year:
            if not mobile_number.isdigit() or len(mobile_number) != 10:
                messagebox.showerror(title="Error", message="Mobile number should have 10 digits.")
                return
            # Insert data into the database
            try:
                cur.execute('''INSERT INTO person_Details(firstname, lastname, title, age, state, mobile_number,
                              Engg_Branch, course_name, passout_year)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                            (firstname, lastname, title, age, state, mobile_number,
                             Engg_Branch_name, course_name, passout_year))
                con.commit()
                messagebox.showinfo(title="Success", message="Data saved successfully!")

                #........Clearing The Values After Data Is Saved..................
                first_name_entry.delete(0, "end")
                last_name_entry.delete(0, "end")
                mobile_number_entry.delete(0, "end")
                title_combobox.set("")
                age_spinbox.delete(0, "end")
                state_combobox.set("")
                Engg_branch_combobox.set("")
                course_combobox.set("")
                passout_year_spinbox.delete(0, "end")
                accept_var.set("Not Accepted")
            #..................................................................................

            except mysql.connector.Error as err:
                messagebox.showerror(title="Error", message=f"Error occurred: {err}")
        else:
            messagebox.showwarning(title="Error", message="Filling of all Fields are required.")
    else:
        messagebox.showwarning(title="Error", message="You have not accepted the terms")

#.......................................................................................................................................................


# def validate_mobile_number():
#     mobile_number = mobile_number_entry.get()
#     if len(mobile_number) != 10:
#         messagebox.showerror(title="Error", message="Mobile number should have 10 digits.")
#         return False
#     return True
#...................................................Execution Of SHOW DATA ENtries Button.....................................................................................................

def show_data_entries():
    # Prompt for the password
    password = simpledialog.askstring("Password", "Enter the password", show='*')

    if password == "1":  # Replace "password123" with your desired password
        # Fetch all the data from the database
        try:
            cur.execute("SELECT * FROM person_Details")
            rows = cur.fetchall()
            if len(rows) > 0:
                # Create a new window for displaying the data
                data_window = Toplevel(window)                 # New window
                data_window.title("Data Entries")

                # Create labels for the column names
                column_names = ["ID", "First Name", "Last Name", "Title", "Age", "State", "Mobile Number",
                                "State", "Course Name", "Passout Year"]
                for i, column in enumerate(column_names):
                    label = Label(data_window, text=column, padx=10, pady=5,font="bold",relief='groove' ,bg="lightgray")
                    label.grid(row=0, column=i)

                # Display the data rows
                for row_index, row_data in enumerate(rows):
                    for column_index, column_data in enumerate(row_data):
                        label = Label(data_window, text=column_data, padx=10, pady=5)
                        label.grid(row=row_index + 1, column=column_index)
                for i in range(len(column_names)):
                    data_window.grid_columnconfigure(i, weight=1)

            else:
                messagebox.showinfo(title="No Data", message="No data entries found.")
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", message=f"Error occurred: {err}")
    else:
        messagebox.showerror(title="Error", message="Invalid password")
#...............................................................................................................................................................
#.......................................First frame............................................................................................................
# Saving User Info
user_info_frame = tk.LabelFrame(frame, text="User Information")
user_info_frame.grid(row=0, column=0)

#.........................................................................................................................................................

#............................................Labels and Entries making  and placing in First Frame..........................................................................

first_name_label = tk.Label(user_info_frame, text="First Name",font=('Times New Roman',16),relief="groove")
first_name_label.grid(row=0, column=0)
last_name_label = tk.Label(user_info_frame, text="Last Name", font=('Times New Roman', 16), relief="groove")
last_name_label.grid(row=0, column=1)
mobile_number_label = tk.Label(user_info_frame, text="Mobile Number", font=('Times New Roman', 16), relief="groove")
mobile_number_label.grid(row=2, column=0)

first_name_entry = tk.Entry(user_info_frame,width=20,font=('Times New Roman', 16), relief="groove")
last_name_entry = tk.Entry(user_info_frame,width=20,font=('Times New Roman', 16), relief="groove")
mobile_number_entry = tk.Entry(user_info_frame,width=10,font=('Times New Roman', 16), relief="groove")

first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)
mobile_number_entry.grid(row=3, column=0)
# mobile_number_entry.config(validate="focusout", validatecommand=validate_mobile_number)

title_label = tk.Label(user_info_frame, text="Title", font=('Times New Roman', 16), relief="groove")
title_combobox = ttk.Combobox(user_info_frame, values=["", "Mr.", "Ms.", "Mrs."],width=5,font=('Times New Roman', 16))
title_label.grid(row=0, column=2)
title_combobox.grid(row=1, column=2)

age_label = tk.Label(user_info_frame, text="Age", font=('Times New Roman', 16), relief="groove")
age_spinbox = tk.Spinbox(user_info_frame, from_=18, to=110,font=('Times New Roman', 16),width=10)
age_label.grid(row=2, column=2)
age_spinbox.grid(row=3, column=2)

state_label = tk.Label(user_info_frame, text="State" ,font=('Times New Roman', 16), relief="groove")
state_combobox = ttk.Combobox(user_info_frame, values=["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
                                                       "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
                                                       "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
                                                       "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
                                                       "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
                                                       "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
                                                       "West Bengal"])
state_label.grid(row=2, column=1)
state_combobox.grid(row=3, column=1)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10,sticky='nsew')

#..............................................Second Frame and Its labels and ENtry boxes............................................................
# Saving Course Info
courses_frame = tk.LabelFrame(frame,text='Other Information')                              # Second frame in First window
courses_frame.grid(row=1, column=0,  padx=10, pady=20)

Engg_branch_label = tk.Label(courses_frame, text="Engg Branch",font=('Times New Roman', 16), relief="groove",width=20)
Engg_branch_label.grid(row=0, column=0)
Engg_branch_var = tk.StringVar(value=" ")
Engg_branch_combobox = ttk.Combobox(courses_frame, textvariable=Engg_branch_var, values=[" ","Mechanical", "Civil","Electrical", 
                                                                                       "Electronic","Computer Science","Information Technology","Others"]
                                                                                       ,font=('Times New Roman', 16))
Engg_branch_combobox.grid(row=1, column=0)

course_label = tk.Label(courses_frame, text="Course",font=('Times New Roman', 16), relief="groove",width=16)
course_label.grid(row=0, column=1)
course_combobox = ttk.Combobox(courses_frame, values=["DAC", "DBDA", "MSCIT"],font=('Times New Roman', 14))
course_combobox.grid(row=1, column=1)

passout_year_label = tk.Label(courses_frame, text="Passout Year",font=('Times New Roman', 16),relief='groove',width=10)
passout_year_label.grid(row=0, column=2)
passout_year_spinbox = tk.Spinbox(courses_frame, from_=2012, to=2050,font=('Times New Roman', 16),width=10)
passout_year_spinbox.grid(row=1, column=2)

#...................................................End of Second Frame Design....................................................................................
for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Accept Terms
accept_var = tk.StringVar(value="Not Accepted")
accept_checkbutton = tk.Checkbutton(frame, text="I accept the terms and conditions", variable=accept_var,
                                   onvalue="Accepted", offvalue="Not Accepted",font=('Times New Roman', 14), relief="groove")

accept_checkbutton.grid(row=2, column=0,sticky='news', padx=10, pady=10)

# Buttons
button_frame = tk.Frame(frame)
button_frame.grid(row=3, column=0, pady=10)

submit_button = tk.Button(button_frame, text="Submit", command=enter_data,font=('Times New Roman', 18), relief="groove",bg='Light Green',width=15)
submit_button.pack(side="left", padx=5)
show_entries_button = tk.Button(button_frame, text="Show Data Entries", command=show_data_entries,font=('Times New Roman', 18), relief="groove",bg='Light Blue',width=15)
show_entries_button.pack(side="left", padx=10)
exit_button = tk.Button(button_frame, text="Exit", command=window.destroy,font=('Times New Roman', 18), relief="groove",bg='Red',width=10)
exit_button.pack(side="left", padx=10)

window.mainloop()

# Close the connection
cur.close()
con.close()