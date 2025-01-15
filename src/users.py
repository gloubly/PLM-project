import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, askokcancel, askyesno
from utils import Placeholder_Entry, date_to_str, str_to_date
from datetime import datetime
from test import TestApp
from bson import ObjectId

USERS_COLUMNS = {
    'email': .2,
    'username': .2,
    'password': .2,
    'admin': .2,
    'creation_date': .2
}


class UsersPage(tk.Frame):
    def __init__(self, parent, database, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.users_collection = database['users']
        self.user_id = None
        screen_width = self.parent.notebook.winfo_screenwidth()

        tk.Label(self, text='Users', font=('Cascadia Code', 20), relief='groove', anchor='center', borderwidth=2, bg='#d1d1d1').pack(fill='both', pady=5)
        tree_users_frame = tk.Frame(self)
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
        self.menu.add_command(label="Promote/downgrade", command=self.switch_admin)
        self.menu.add_command(label="Remove", command=self.remove_user)
        self.tree_users.bind("<Button-3>", self.on_right_click)
        
        self.load_users()

        add_user_frame = tk.Frame(self, borderwidth=10)
        add_user_frame.pack(pady=30)
        self.email_var = tk.StringVar(add_user_frame, "")
        self.username_var = tk.StringVar(add_user_frame, "")
        self.password_var = tk.StringVar(add_user_frame, "")
        self.checkbox_var = tk.BooleanVar(add_user_frame)
        self.error_var = tk.StringVar(add_user_frame, "")

        tk.Label(add_user_frame, text="Add an user", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        tk.Label(add_user_frame, text="Email", anchor='w').grid(row=1, column=0, sticky='we', pady=10, padx=10)
        self.email_entry = Placeholder_Entry(add_user_frame, placeholder="Email", textvariable=self.email_var)
        self.email_entry.grid(row=1, column=1, pady=10, padx=10)
        tk.Label(add_user_frame, text="Username", anchor='w').grid(row=2, column=0, sticky='we', pady=10, padx=10)
        self.username_entry = Placeholder_Entry(add_user_frame, placeholder="Username", textvariable=self.username_var)
        self.username_entry.grid(row=2, column=1, pady=10, padx=10)
        tk.Label(add_user_frame, text="Password", anchor='w').grid(row=3, column=0, sticky='we', pady=10, padx=10)
        self.password_entry = Placeholder_Entry(add_user_frame, placeholder="Password", textvariable=self.password_var)
        self.password_entry.grid(row=3, column=1, pady=10, padx=10)
        tk.Label(add_user_frame, text="Admin", anchor='w').grid(row=4, column=0, sticky='we', pady=10, padx=10)
        ttk.Checkbutton(add_user_frame, variable=self.checkbox_var).grid(row=4, column=1, pady=10, padx=10)
        ttk.Button(add_user_frame, text="Add User", command=self.add_user).grid(row=5, column=0, columnspan=2, pady=10, padx=10)
        ttk.Label(add_user_frame, textvariable=self.error_var, foreground='red').grid(row=6, column=0, columnspan=2, pady=10, padx=10)


    def load_users(self):
        req = self.users_collection.find({}, {"_id": 1, "email": 1, "username": 1, "pwd_length": {"$strLenCP": "$password"}, 'admin':1, 'creation_date':1})
        for user in req:
            self.tree_users.insert("", "end", iid=user["_id"], values=[user["email"], user["username"], user["pwd_length"]*"*", 'Yes' if user["admin"] else 'No', date_to_str(user['creation_date'])])

    def add_user(self):
        is_valid = True
        if self.email_var.get()=='Email' or self.username_var.get()=='Username' or self.password_var.get()=='Password':
            self.error_var.set("Please fill out all the entries")
            return None
        req = self.users_collection.find({ "$or": [{ "email": self.email_var.get() }, {"username": self.username_var.get()}]}, {"_id": 0, "email":1, "username": 1})
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
                new_user = {'email': self.email_var.get(), 'username': self.username_var.get(), 'password': self.password_var.get(), 'admin':self.checkbox_var.get(), 'creation_date':datetime.now()}
                self.users_collection.insert_one(new_user)
                self.tree_users.insert("", "end", iid=new_user["_id"], values=[new_user["email"], new_user["username"], len(new_user["password"])*"*", 'Yes' if new_user['admin'] else 'No', date_to_str(new_user['creation_date'])])
                self.email_entry.reset_placeholder()
                self.username_entry.reset_placeholder()
                self.password_entry.reset_placeholder()
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
    
    def switch_admin(self):
        values = self.tree_users.item(self.user_id)["values"]
        admin = values[3]=='Yes'
        message = f'Are you sure you want to {'downgrade' if admin else 'promote'} user "{values[1]}" ?'
        proceed = askyesno(title="Warning", message=message, icon='warning')
        if not proceed:
            return None
        if admin:
            req = self.users_collection.find({'admin': True}).to_list()
            if len(req)<2:
                showerror("Error", "There can't be no admins")
                return None
        values[3] = 'No' if admin else 'Yes'
        self.tree_users.item(self.user_id, values=values)
        self.users_collection.update_one({ "_id": ObjectId(self.user_id)}, { "$set": {"admin": False if admin else True}})


#############
## Testing ##
#############
if __name__ == '__main__':
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["db_plm"]
    app = TestApp(database, 20000)

    app.page = UsersPage(app, app.database)
    
    app.notebook.add(app.page, text="Users")
    app.notebook.select(app.page)
    app.mainloop()