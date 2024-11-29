import tkinter as tk

class LoginPage(tk.Frame):
    def __init__(self, parent, database, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.database = database
        login_frame = tk.Frame(self.parent)
        error_var = tk.StringVar(login_frame, "")
        login_frame.pack()
        tk.Entry(self.parent)
        tk.Label(login_frame, text="Username").pack()
        username_entry = tk.Entry(login_frame)
        username_entry.pack()
        tk.Label(login_frame, text="Password").pack()
        password_entry = tk.Entry(login_frame)
        password_entry.pack()
        tk.Button(login_frame, text="Login", command=lambda: self.login(username_entry.get(), password_entry.get(), error_var)).pack()
        tk.Label(login_frame, textvariable=error_var).pack()

    def login(self, username, password, stringvar):
        if username!="" and password!="":
            project = self.database.find_one({"users":{"$elemMatch":{"username":username, "password":password}}})
            if project:
                stringvar.set("")
                print('yay')
            else:
                stringvar.set("error")
