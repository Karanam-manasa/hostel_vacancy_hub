from tkinter import Tk, Frame, Label, Entry, Button, Listbox,Scrollbar, messagebox, Toplevel,ttk
from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
import csv
import re
from tkinter import scrolledtext
from tkinter import END,VERTICAL
from tkinter import Label
# Establishing connection to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='M@n@s@64',
    database='mydatabase1'
)
cursor = conn.cursor()

# Define font styles for consistency across UI elements
fonts = ('Calibri', 25, 'bold')
font1 = ('Arial', 15,'bold')

class Login:
    def __init__(self, root, cursor):
        self.root = root
        self.cursor = cursor
        self.root.configure(bg="white")
        # Header Frame
        self.header = Frame(self.root, bg="white", height=120)
        self.header.pack(fill="x")

        # Logo
        logo_image = Image.open("D:\\manasa\\projects\\newlogo.bmp")
        logo_image = logo_image.resize((100, 100), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = Label(self.header, image=self.logo_photo, bg="white")
        logo_label.pack(side="left", padx=10, pady=10)

        #title
        title_label = Label(
            self.header,
            text="SHRI VISHNU ENGINEERING COLLEGE FOR WOMEN\nVishnupur, BHIMAVARAM, West Godavari Dist. - 534202",
            font=("Arial", 18, "bold"),
            fg="DarkOrange",
            bg="white"
        )
        title_label.pack(pady=10)

        # Main Login Frame
        self.login_frame = Frame(self.root, bg='white')
        self.login_frame.pack(expand=True)

        # Student Login Section
        student_login_frame = Frame(self.login_frame, bg="light green",width=350, height=250, padx=20, pady=20)
        student_login_frame.grid(row=0, column=1, padx=40, pady=40)

        title_label = Label(student_login_frame, text='Student Login', font=font1, fg="black", bg="lightgreen")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        Label(student_login_frame, text="User Name:", font=("Arial", 12,'bold'), bg="lightgreen",fg='black').grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.user_name_entry = Entry(student_login_frame, font=("Arial", 12),width=20)
        self.user_name_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(student_login_frame, text="Password:", font=("Arial", 12,'bold'), bg="lightgreen",fg='black').grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.user_pass_entry = Entry(student_login_frame, font=("Arial", 12), show="*", width=20)
        self.user_pass_entry.grid(row=2, column=1, padx=5, pady=5)

        submit_btn = Button(student_login_frame, text="Login", activebackground='lightgray',
                            bd=0, cursor='hand2', width=10, font=("Arial", 12, "bold"), bg="darkorange", fg="white",
                                  command=self.check_student_login)
        submit_btn.grid(row=3, column=0, columnspan=2, pady=10)

        student_image = Image.open("D:\manasa\projects\student_logo.jpg")  
        student_image = student_image.resize((60, 60))
        self.student_logo = ImageTk.PhotoImage(student_image)
        Label(student_login_frame, image=self.student_logo, bg="lightgreen").grid(row=3, column=0, padx=5, pady=10, sticky="w")

        self.user_name_entry.bind("<Return>", lambda event: self.user_pass_entry.focus())
        self.user_pass_entry.bind("<Return>", lambda event: self.check_student_login())

        # Admin Login Section
        admin_login_frame = Frame(self.login_frame,bg="light gray", width=350, height=250, padx=20, pady=20)
        admin_login_frame.grid(row=0, column=0, padx=40, pady=40)

        title_label = Label(admin_login_frame, text='Admin Login', font=("Arial", 14, "bold"), fg="black", bg="light gray")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        Label(admin_login_frame, text="User Name:", font=("Arial", 12,'bold'), bg="light gray").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.admin_user_name_entry = Entry(admin_login_frame, font=("Arial", 12))
        self.admin_user_name_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(admin_login_frame, text="Password:", font=("Arial", 12,'bold'), bg="light gray").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.admin_user_pass_entry = Entry(admin_login_frame, font=("Arial", 12), show="*")
        self.admin_user_pass_entry.grid(row=2, column=1, padx=5, pady=5)

        admin_submit_btn = Button(admin_login_frame, text="Login", activebackground='lightgreen',
                            bd=0, cursor='hand2', width=10, font=("Arial", 12, "bold"), bg="darkorange", fg="white",
                                  command=self.check_admin_login)
        admin_submit_btn.grid(row=3, column=0, columnspan=2, pady=10)

        admin_image = Image.open("D:\manasa\projects\admin_logo.jpg") 
        admin_image = admin_image.resize((60, 60)) 
        self.admin_logo = ImageTk.PhotoImage(admin_image)
        Label(admin_login_frame, image=self.admin_logo, bg="lightgray").grid(row=3, column=0, padx=5, pady=10, sticky="w")

        self.admin_user_name_entry.bind("<Return>", lambda event: self.admin_user_pass_entry.focus())
        self.admin_user_pass_entry.bind("<Return>", lambda event: self.check_admin_login())

    def check_student_login(self):
        name = self.user_name_entry.get().upper()
        password = self.user_pass_entry.get()
        pattern = r"^22B01A05([0-9][0-9]|[A-J][0-9])$"
        if not re.match(pattern, name):
            messagebox.showerror('INVALID USERNAME','INVALID USERNAME')
            return
        if password != "svecw":
            messagebox.showerror('WRONG PASSWORD', 'Incorrect password. Please try again.')
            return

        cursor.execute("SELECT * FROM student WHERE name = %s", (name,))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo('WELCOME', f'WELCOME {name}')
        else:
            cursor.execute("INSERT INTO student (name, password) VALUES (%s, %s)", (name, password))
            conn.commit()
            messagebox.showinfo('WELCOME', f'WELCOME {name}')
        self.logged_in_username = name  

        # Remove Header when switching pages
        self.header.pack_forget()
        self.login_frame.destroy()
        dashboard = Dashboard(self.root, self.logged_in_username, self.cursor,admin=False)
    
    def check_admin_login(self):
        name = self.admin_user_name_entry.get()
        password = self.admin_user_pass_entry.get()

        # Check if admin already exists in the database
        cursor.execute("SELECT * FROM admin1 WHERE name = %s", (name,))
        admin = cursor.fetchone()

        if admin:  
            if password == admin[1]:  # Verify password
                messagebox.showinfo('WELCOME', 'WELCOME ADMIN')
                self.logged_in_username = name
                self.login_frame.destroy()
                dashboard = Dashboard(self.root, self.logged_in_username, self.cursor, admin=True)

            else:
                messagebox.showerror('WRONG PASSWORD', 'CHECK YOUR PASSWORD')
            
        else:  # New admin, insert into database
            cursor.execute("INSERT INTO admin1 (name, password) VALUES (%s, %s)", (name, password))
            conn.commit()
            messagebox.showinfo('WELCOME', 'WELCOME ADMIN')
            self.logged_in_username = name 
            self.header.pack_forget()
            self.login_frame.destroy()
            dashboard = Dashboard(self.root, self.logged_in_username, self.cursor, admin=True)

class Dashboard:
    def __init__(self, root,logged_in_username,cursor, admin=False):
        self.root = root
        self.root.state('zoomed')  # Makes the window full screen
        self.logged_in_username = logged_in_username 
        self.admin = admin
        self.cursor = cursor
        if admin:
            self.root.title('ADMIN DASHBOARD')
            self.root.geometry("800x500")
            self.root.configure(bg="#f0f0f0")

            self.admin_dashboard()
        else:
            self.root.title('STUDENT DASHBOARD')
            bg_color = 'Light Green'
            self.student_dashboard()
    def on_hover(self,button, color):
        button.config(bg=color)

    def on_leave(self,button, color):
        button.config(bg=color)
        
    def student_dashboard(self):
        student_dashboard_frame = Frame(self.root, bg='#A8E6A3')
        student_dashboard_frame.pack(fill='both', expand=True)

        self.header = Frame(student_dashboard_frame, bg="#A8E6A3", height=60)
        self.header.pack(fill="x")

        def go_back():
            student_dashboard_frame.pack_forget() 
            self.previous_frame.pack(fill="both", expand=True)  
    
        back_button = Button(self.header, text="⬅", font=("Calibri", 20, "bold"), bg="#A8E6A3", fg="black",
                                padx=2, pady=0, cursor="hand2", command=go_back, borderwidth=0)
        back_button.place(x=10, y=5)  

        title_label = Label(self.header, text="\nSHRI VISHNU ENGINEERING COLLEGE FOR WOMEN\n"
                                                "Vishnupur, BHIMAVARAM, West Godavari Dist. - 534202",
                                font=("Arial", 20, "bold"), fg="dark green", bg="#A8E6A3")
        title_label.pack(pady=5)

        welcome_text = f"Welcome {self.logged_in_username}!"
        welcome_label = Label(self.header, text=welcome_text, font=("Calibri", 18, "bold"),
                            fg="blue", bg="#A8E6A3")
        welcome_label.pack(side=LEFT, padx=20, pady=10)

        logout_button = Button(self.header, text="Logout", font=("Calibri", 14, "bold"), bg="red", fg="white",
                            padx=10, pady=5, cursor="hand2", command=self.logout)
        logout_button.pack(side=RIGHT, padx=20, pady=10)

        def logout(self):
            response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
            if response:
                self.root.destroy()

        # Configure the grid to center elements
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        container = Frame(root, bg="Light Green", bd=5, relief=FLAT)
        container.pack(pady=9, padx=20)

        search_frame = Frame(container, bg="white", bd=2, relief=GROOVE)
        search_frame.grid(row=0, column=0, columnspan=3, padx=0, pady=5, sticky="ew")
        search_frame.columnconfigure(0, weight=1)
  
        self.search_entry = Entry(search_frame, font=('Calibri', 14), bg='white', fg='#333', bd=0, width=25)
        self.search_entry.grid(row=0, column=0, padx=10, pady=5, ipady=5, sticky="ew")

        def on_enter(e):
            search_button.config(bg="darkGreen")

        def on_leave(e):
            search_button.config(bg="Dark Orange")

        search_button = Button(search_frame, text="Search", bg='Dark Orange', fg='white',
                            font=('Calibri', 14, 'bold'), activebackground='Dark Orange',
                            bd=0, cursor='hand2', width=10, relief=FLAT,command=self.perform_search)

        search_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")
        search_button.bind("<Enter>", on_enter)
        search_button.bind("<Leave>", on_leave)

        # Create a frame to hold the Listbox and Scrollbar
        listbox_frame = Frame(container, bg="Light Green")
        listbox_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # Add a label as the header for the Listbox
        listbox_label = Label(container, text="Find Your Hostel", font=('Calibri', 16, 'bold'), bg="light green", fg="darkgreen")
        listbox_label.grid(row=1, column=0, columnspan=3, padx=5, pady=(10,5), sticky="ew")  # Move label to the top of the Listbox

        # Create Listbox and Scrollbar
        self.hostel_listbox = Listbox(container, font=('Calibri', 14), bg='white')
        self.hostel_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        hostel_scrollbar = Scrollbar(container, orient='vertical', command=self.hostel_listbox.yview)
        hostel_scrollbar.grid(row=2, column=3, sticky="ns")

        # Link scrollbar to Listbox
        self.hostel_listbox.config(yscrollcommand=hostel_scrollbar.set)

        # Retrieve unique hostel names from the database
        cursor.execute("SELECT DISTINCT hostel_name FROM hostel")
        hostels = cursor.fetchall()
        
        for hostel in hostels:
            self.hostel_listbox.insert(END, hostel[0])

        # Bind a function to handle hostel selection
        self.hostel_listbox.bind("<<ListboxSelect>>", self.perform_search)

        # Create a Treeview widget to display hostel details
        self.hostel_details_tree = ttk.Treeview(container, columns=("Hostel Name","Room No", "Beds"), show="headings")
        self.hostel_details_tree.grid(row=3, column=0, columnspan=3, padx=10, pady=20, sticky="ew")

        # Define column headings
        self.hostel_details_tree.heading("Hostel Name", text="Hostel Name",anchor="center")
        self.hostel_details_tree.heading("Room No", text="Room No",anchor="center")
        self.hostel_details_tree.heading("Beds", text="Beds",anchor="center")
        self.hostel_details_tree.column("Hostel Name", width=150, anchor="center")
        self.hostel_details_tree.column("Room No", width=100, anchor="center")
        self.hostel_details_tree.column("Beds", width=50, anchor="center")

        # Create a scrollbar for the hostel details treeview
        details_scrollbar = Scrollbar(container, orient='vertical', command=self.hostel_details_tree.yview)
        details_scrollbar.grid(row=3, column=3, sticky="ns")
        self.hostel_details_tree.config(yscrollcommand=details_scrollbar.set)
        
    def perform_search(self, event=None):
        query = self.search_entry.get()
        if not query and self.hostel_listbox.curselection():
            query = self.hostel_listbox.get(self.hostel_listbox.curselection())

        if not query:
            messagebox.showwarning("Empty Query", "Please enter a search query.")
            return

        cursor.execute("SELECT hostel_name, room_no, beds FROM hostel WHERE hostel_name LIKE %s", ('%' + query + '%',))
        search_results = cursor.fetchall()
        
        if not search_results:
            messagebox.showinfo("No Results", "No matching results found.")
            return

        self.hostel_details_tree.delete(*self.hostel_details_tree.get_children())

        for result in search_results:
            self.hostel_details_tree.insert("", "end", values=result)
    
    def admin_dashboard(self):
        self.sidebar = Frame(self.root, bg="#2c3e50", width=100, height=600)
        self.sidebar.pack(side="left", fill="y")

        img_path ="D:\manasa\projects\admin_logo.jpg" 
        try:
            img = Image.open(img_path)
            img = img.resize((50, 50), Image.LANCZOS)
            self.icon = ImageTk.PhotoImage(img)  
            logo_label = Label(self.sidebar, image=self.icon, bg="#2c3e50")
            logo_label.pack(pady=20)
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not load image: {e}")

        buttons = [
            ("Add", self.add_data),
            ("Update", self.update_data),
            ("Delete", self.delete_data),
            ("History", self.show_history),
            ("Logout", self.logout)
        ]
        
        for text, command in buttons:
            button = Button(
                self.sidebar, text=text, command=command,
                bg="#34495e", fg="white", font=("Arial", 12, "bold"),
                width=20, height=2, bd=0, cursor="hand2"
            )
            button.pack(pady=10)
            button.bind("<Enter>", lambda e, b=button: self.on_hover(b, "#16a085"))
            button.bind("<Leave>", lambda e, b=button: self.on_leave(b, "#34495e"))

        self.container = Frame(self.root, bg="white")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)

        self.content_label = Label(self.container, text="WELCOME TO ADMIN DASHBOARD",
                                   font=("Arial", 18, "bold"), bg="white",fg='#2c3e50')
        self.content_label.grid(row=0, column=1, pady=10, sticky="nsew")

        # Create a label for the history section
        self.history_label = Label(self.container, text="History Records", font=('Calibri', 16, 'bold'),
                              bg="light green", fg="darkgreen")
        
        # Create a Treeview widget for history
        self.history_tree = ttk.Treeview(self.container,
                                         columns=("ID", "Hostel Name", "Room No",  "Action","Beds", "Timestamp"),
                                         show="headings")
        
        # Define column headings
        for col in ("ID", "Hostel Name", "Room No", "Beds", "Action", "Timestamp"):
            self.history_tree.heading(col, text=col, anchor="center")
            self.history_tree.column(col, width=100, anchor="center")

        # Add a scrollbar for the history Treeview
        self.history_scrollbar = Scrollbar(self.container, orient='vertical', command=self.history_tree.yview)
        self.history_tree.config(yscrollcommand=self.history_scrollbar.set)
        self.history_label.grid_remove()
        self.history_tree.grid_remove()
        self.history_scrollbar.grid_remove()

    def show_history(self):
        self.history_label.grid(row=1, column=0, columnspan=3, padx=5, pady=(10, 5), sticky="ew")
        self.history_tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.history_scrollbar.grid(row=2, column=3, sticky="ns")
        self.display_history()
    def display_history(self):
        try:
            for row in self.history_tree.get_children():
                self.history_tree.delete(row)

            self.cursor.execute("SELECT id, hostel_name, room_no,action, beds, timestamp FROM hostel_history ORDER BY timestamp DESC")
            rows = self.cursor.fetchall()

            for row in rows:
                self.history_tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching history: {err}")
    
    def center_window(self, window, width=400, height=250):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def add_data(self):
        add_window = Toplevel(self.root)
        add_window.title("Add Data")
        self.center_window(add_window)

        Label(add_window, text="Hostel Name:", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10)
        hostel_entry = Entry(add_window, font=('Calibri', 14))
        hostel_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(add_window, text="Room No:", font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=10)
        room_entry = Entry(add_window, font=('Calibri', 14))
        room_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(add_window, text="Number of Beds:", font=('Arial', 14)).grid(row=2, column=0, padx=10, pady=10)
        beds_entry = Entry(add_window, font=('Calibri', 14))
        beds_entry.grid(row=2, column=1, pady=10)

        Button(add_window, text="ADD", command=lambda: self.store_data(hostel_entry.get(), room_entry.get(), beds_entry.get()),
                  bg='Dark Orange', fg='white', font=('Arial', 14, 'bold'), width=10).grid(row=3, column=0, columnspan=2, pady=10)
        hostel_entry.bind("<Return>", lambda event: room_entry.focus())
        room_entry.bind("<Return>", lambda event: beds_entry.focus())
        beds_entry.bind("<Return>", lambda event: self.store_data(hostel_entry.get(), room_entry.get(), beds_entry.get()))

    def update_data(self):
        update_window = Toplevel(self.root)
        update_window.title("Update Data")
        self.center_window(update_window)

        Label(update_window, text="Hostel Name:", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10)
        hostel_entry = Entry(update_window, font=('Calibri', 14))
        hostel_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(update_window, text="Room No:", font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=10)
        room_entry = Entry(update_window, font=('Calibri', 14))
        room_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(update_window, text="Number of Beds:", font=('Arial', 14)).grid(row=2, column=0, padx=10, pady=10)
        beds_entry = Entry(update_window, font=('Calibri', 14))
        beds_entry.grid(row=2, column=1, pady=10)

        Button(update_window, text="UPDATE", command=lambda: self.update_data_in_db(hostel_entry.get(), room_entry.get(), beds_entry.get()),
                  bg='Dark Orange', fg='white', font=('Arial', 14, 'bold'), width=10).grid(row=3, column=0, columnspan=2, pady=10)
        hostel_entry.bind("<Return>", lambda event: room_entry.focus())
        room_entry.bind("<Return>", lambda event: beds_entry.focus())
        beds_entry.bind("<Return>", lambda event: self.update_data_in_db(hostel_entry.get(), room_entry.get(), beds_entry.get()))

    def delete_data(self):
        delete_window = Toplevel(self.root)
        delete_window.title("Delete Data")
        self.center_window(delete_window)

        Label(delete_window, text="Hostel Name:", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10)
        hostel_entry = Entry(delete_window, font=('Arial', 14))
        hostel_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(delete_window, text="Room No:", font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=10)
        room_entry = Entry(delete_window, font=('Arial', 14))
        room_entry.grid(row=1, column=1, padx=10, pady=10)

        Button(delete_window, text="DELETE", command=lambda: self.delete_data_from_db(hostel_entry.get(), room_entry.get()),
                  bg='Dark Orange', fg='white', font=('Arial', 14, 'bold'), width=10).grid(row=3, column=0, columnspan=2, pady=10)
        hostel_entry.bind("<Return>", lambda event: room_entry.focus())
        room_entry.bind("<Return>", lambda event: self.delete_data_from_db(hostel_entry.get(), room_entry.get()))

    def show_form(self, title, command, delete=False):
        window = Toplevel(self.root)
        window.title(title)
        self.center_window(window)

        Label(window, text="Hostel Name:", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10)
        hostel_entry = Entry(window, font=('Calibri', 14))
        hostel_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(window, text="Room No:", font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=10)
        room_entry = Entry(window, font=('Calibri', 14))
        room_entry.grid(row=1, column=1, padx=10, pady=10)

        if not delete:
            Label(window, text="Number of Beds:", font=('Arial', 14)).grid(row=2, column=0, padx=10, pady=10)
            beds_entry = Entry(window, font=('Calibri', 14))
            beds_entry.grid(row=2, column=1, pady=10)

        Button(window, text=title.upper(), command=lambda: command(hostel_entry.get(), room_entry.get(),
                                                                   beds_entry.get() if not delete else None),
               bg='Dark Orange', fg='white', font=('Arial', 14, 'bold'), width=10).grid(row=3, column=0, columnspan=2, pady=10)

    def store_data(self, hostel_name, room_no, beds):
        if not hostel_name or not room_no or not beds:
            messagebox.showwarning("Input Error", "All fields must be filled!")
            return
        try:
            cursor.execute("INSERT INTO hostel (hostel_name, room_no, beds) VALUES (%s, %s, %s)", (hostel_name, room_no, beds))
            cursor.execute("INSERT INTO hostel_history (action, hostel_name, room_no, beds) VALUES ('ADD', %s, %s, %s)", (hostel_name, room_no, beds))
            conn.commit()  
            self.display_history()
            messagebox.showinfo("Success", "Data added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")

    def update_data_in_db(self, hostel_name, room_no, beds):
        if not hostel_name or not room_no or not beds:
            messagebox.showwarning("Input Error", "All fields must be filled!")
            return
        try:
            cursor.execute("UPDATE hostel SET beds = %s WHERE hostel_name = %s AND room_no = %s", (beds, hostel_name, room_no))
            cursor.execute("INSERT INTO hostel_history (action, hostel_name, room_no, beds) VALUES ('UPDATE', %s, %s, %s)", (hostel_name, room_no, beds))
            conn.commit()  
            self.display_history()
            messagebox.showinfo("Success", "Data updated successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")

    def delete_data_from_db(self, hostel_name, room_no):
        if not hostel_name or not room_no:
            messagebox.showwarning("Input Error", "All fields must be filled!")
            return
        try:
            cursor.execute("DELETE FROM hostel WHERE hostel_name = %s AND room_no = %s", (hostel_name, room_no))
            cursor.execute("INSERT INTO hostel_history (action, hostel_name, room_no, beds) VALUES ('DELETE', %s, %s, NULL)", (hostel_name, room_no))
            conn.commit()  
            self.display_history()
            messagebox.showinfo("Success", "Data deleted successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")
    
    def logout(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if response:
            for widget in self.root.winfo_children():
                widget.destroy()
        
            self.root.state('normal')
            self.root.geometry('1200x500+200+140') 
            self.root.resizable(False, False)
            Login(self.root, self.cursor)

if __name__ == "__main__":
    root = Tk()
    root.title('LOGIN')
    root.geometry('1200x500+200+140')
    root.resizable(False, False)
    login = Login(root,cursor)
    root.mainloop()
