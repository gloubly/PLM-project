import tkinter as tk

FRAME_BG_COLOR = "#4287f5"
INNER_BG_COLOR = "#194fa6"

class LoginPage(tk.Frame):
    def __init__(self, parent, database, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.users_collection = database["users"]
        login_frame = tk.Frame(self.parent, bg=FRAME_BG_COLOR, padx=20, pady=10)
        login_frame.pack(anchor="center", padx=20, pady=20, expand=True)
        error_var = tk.StringVar(login_frame, "")
        tk.Entry(self.parent)

        # username
        tk.Label(login_frame, text="Username", bg=INNER_BG_COLOR, fg='white', font=(20)).pack(fill="both", pady=(20,0))
        username_entry = tk.Entry(login_frame)
        username_entry.pack()

        # password
        tk.Label(login_frame, text="Password", bg=INNER_BG_COLOR, fg='white', font=(20)).pack(pady=(20,0), fill="both")
        password_entry = tk.Entry(login_frame)
        password_entry.pack(pady=(0, 20))

        # buttons
        tk.Button(login_frame, text="Login", font=(17), padx=10, pady=0, relief="groove", borderwidth=2, fg='white', bg=INNER_BG_COLOR,
                  activebackground='white', activeforeground=INNER_BG_COLOR,
                  command=lambda: self.login(username_entry.get(), password_entry.get(), error_var)).pack()
        tk.Label(login_frame, textvariable=error_var, bg=FRAME_BG_COLOR, fg='red').pack()

    def login(self, username, password, stringvar):
        if username!="" and password!="":
            project = self.users_collection.find_one({"username":username, "password":password})
            if project:
                stringvar.set("")
                self.load_menu()
            else:
                stringvar.set("error login")

    def load_menu(self):
        self.parent.clear_frame()
        self.parent.menu()
