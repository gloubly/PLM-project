import tkinter as tk
import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
database = mongo_client["db_plm"]["projects"]

#https://stackoverflow.com/questions/17466561/what-is-the-best-way-to-structure-a-tkinter-application
class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.login_page()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def login_page(self):
        #clear()
        login_frame = tk.Frame(self.parent)
        error_var = tk.StringVar(login_frame, "")
        login_frame.pack()
        tk.Entry(main_window, )
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
            project = database.find_one({"users":{"$elemMatch":{"username":username, "password":password}}})
            if project:
                stringvar.set("")
                print('yay')
            else:
                stringvar.set("error")
                

    
main_window = tk.Tk()
App(main_window).pack()
main_window.mainloop()