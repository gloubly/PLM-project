import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, askokcancel
from utils import Custom_Entry

import pymongo
from bson import ObjectId

USERS_COLUMNS = {
    'email': .33,
    'username': .33,
    'password': .33,
}


class AdminPage(tk.Frame):
    def __init__(self, parent, database, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.users_collection = database['users']
        self.user_id = None
        screen_width = self.parent.winfo_screenwidth()

        tree_users_frame = tk.Frame(self.parent)
        tree_users_frame.pack()
        self.tree_users = ttk.Treeview(tree_users_frame, columns=USERS_COLUMNS.keys(), show='headings')
        tree_users_scrollbar = tk.Scrollbar(tree_users_frame, command=self.tree_users.yview)
        tree_users_scrollbar.pack(side='right', fill="y")
        self.tree_users.configure(yscrollcommand=tree_users_scrollbar.set)
        self.tree_users.pack(fill="both")

        tree_users_width = screen_width * 0.9
        for (col, prop), tree_col in zip(USERS_COLUMNS.items(), self.tree_users["columns"]):
            self.tree_users.heading(tree_col, text=col.replace("_", " ").title())
            self.tree_users.column(tree_col, width=int(tree_users_width*prop), anchor='w')

        self.menu = tk.Menu(tree_users_frame, tearoff=0)
        self.menu.add_command(label="Remove", command=self.remove_user)

        self.tree_users.bind("<Button-3>", self.on_right_click)
        
        self.load_users()

        add_user_frame = tk.Frame(self.parent, borderwidth=10)
        add_user_frame.pack(pady=50)
        self.email_var = tk.StringVar(add_user_frame, "")
        self.username_var = tk.StringVar(add_user_frame, "")
        self.password_var = tk.StringVar(add_user_frame, "")
        self.error_var = tk.StringVar(add_user_frame, "")

        ttk.Label(add_user_frame, text="Add an user", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        ttk.Label(add_user_frame, text="Email", anchor='w').grid(row=1, column=0, sticky='we', pady=10, padx=10)
        Custom_Entry(add_user_frame, placeholder="Email", textvariable=self.email_var).grid(row=1, column=1, pady=10, padx=10)
        ttk.Label(add_user_frame, text="Username", anchor='w').grid(row=2, column=0, sticky='we', pady=10, padx=10)
        Custom_Entry(add_user_frame, placeholder="Username", textvariable=self.username_var).grid(row=2, column=1, pady=10, padx=10)
        ttk.Label(add_user_frame, text="Password", anchor='w').grid(row=3, column=0, sticky='we', pady=10, padx=10)
        Custom_Entry(add_user_frame, placeholder="Password", textvariable=self.password_var).grid(row=3, column=1, pady=10, padx=10)
        ttk.Button(add_user_frame, text="Add User", command=self.add_user).grid(row=4, column=0, columnspan=2, pady=10, padx=10)
        ttk.Label(add_user_frame, textvariable=self.error_var, foreground='red').grid(row=5, column=0, columnspan=2, pady=10, padx=10)



    def load_users(self):
        req = self.users_collection.find({}, {"_id": 1, "email": 1, "username": 1, "pwd_length": {"$strLenCP": "$password"}})
        for user in req:
            self.tree_users.insert("", "end", iid=user["_id"], values=[user["email"], user["username"], user["pwd_length"]*"*"])

    def add_user(self):
        is_valid = True
        if self.email_var.get()=='Email' or self.username_var.get()=='Username' or self.password_var.get()=='Password':
            self.error_var.set("Please fill out all the entries")
            return None
        req = self.users_collection.find({ "$or": [{ "email": "etienne.goury@edu.devinci.fr" }, {"username": "gloubly"}]}, {"_id": 0, "email":1, "username": 1})
        for user in req:
            if user['email']==self.email_var.get():
                error_message = "This email already exists"
                is_valid = False
                break
            elif user['username']==self.username_var.get():
                error_message = "This username already exists"
                is_valid = False
                break
        if is_valid:
            self.error_var.set('')
            try:
                new_user = {'email': self.email_var.get(), 'username': self.username_var.get(), 'password': self.password_var.get()}
                self.users_collection.insert_one(new_user)
                self.tree_users.insert("", "end", iid=new_user["_id"], values=[new_user["email"], new_user["username"], len(new_user["password"])*"*"])
                self.email_var.set('')
                self.username_var.set('')
                self.password_var.set('')
                self.error_var.set('')
            except:
                showerror(title="Add User", message=f"Couldn't remove user")
        else:
            self.error_var.set(error_message)
            



    def remove_user(self):
        proceed = askokcancel(title="Remove User", message="Remove user ?")
        if not proceed:
            self.user_id = None
            return None
        req = self.users_collection.delete_one({ "_id": ObjectId(self.user_id)})
        if req.deleted_count>0:
            self.tree_users.delete(self.user_id)
        else:
            showerror(title="Remove User", message=f"Couldn't remove user")

        self.user_id = None

    def on_right_click(self, event):
        self.user_id = self.tree_users.identify_row(event.y)
        if self.user_id:
            self.tree_users.selection_set(self.user_id)
            try:
                self.menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.menu.grab_release()


if __name__ == "__main__":
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["db_plm"]
    root = tk.Tk()
    AdminPage(root, database)
    root.state('zoomed')
    root.after(20000, lambda: root.destroy())
    root.mainloop()