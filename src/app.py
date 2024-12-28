import tkinter as tk
from tkinter import ttk
import pymongo
from products import ProductsPage
from single_product import Product
from users import UsersPage
from utils import clear_frame

# https://stackoverflow.com/questions/17466561/what-is-the-best-way-to-structure-a-tkinter-application
class App(tk.Tk):
    def __init__(self, database, timeout=None, skip=False, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.database = database
        self.wm_title("App")
        self.state('zoomed')
        if timeout is not None:
            self.after(timeout, lambda:self.destroy()) # for testing
        
        self.login_page()
    
    def login_page(self):
        FRAME_BG_COLOR = "#4287f5"
        INNER_BG_COLOR = "#194fa6"

        login_frame = tk.Frame(self, bg=FRAME_BG_COLOR, padx=20, pady=10)
        login_frame.pack(anchor="center", padx=20, pady=20, expand=True)
        error_var = tk.StringVar(login_frame, "")

        # username
        tk.Label(login_frame, text="Username", bg=INNER_BG_COLOR, fg='white', font=(20)).pack(fill="both", pady=(20,0))
        username_entry = tk.Entry(login_frame)
        username_entry.pack()

        # password
        tk.Label(login_frame, text="Password", bg=INNER_BG_COLOR, fg='white', font=(20)).pack(pady=(20,0), fill="both")
        password_entry = tk.Entry(login_frame)
        password_entry.bind("<Return>", lambda event: self.login(username_entry.get(), password_entry.get(), error_var))
        password_entry.pack(pady=(0, 20))

        # buttons
        tk.Button(login_frame, text="Login", font=(17), padx=10, pady=0, relief="groove", borderwidth=2, fg='white', bg=INNER_BG_COLOR,
                  activebackground='white', activeforeground=INNER_BG_COLOR,
                  command=lambda: self.login(username_entry.get(), password_entry.get(), error_var)).pack()
        tk.Label(login_frame, textvariable=error_var, bg=FRAME_BG_COLOR, fg='red').pack()

    def login(self, username, password, stringvar):
        username, password = "gloubly", 'root'
        if username!="" and password!="":
            self.user = self.database["users"].find_one({"username":username, "password":password})
            if self.user:
                stringvar.set("")
                clear_frame(self)
                self.load_notebook()
                # ProductsPage(self, self.database).pack(fill="both", expand=True)
            else:
                stringvar.set("error login")

    def load_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.products_page = ProductsPage(self, database)
        self.products_page.pack(fill='both', expand=True)
        self.notebook.add(self.products_page, text="Products")
        if self.user['admin']:
            self.user_page = UsersPage(self, database)
            self.user_page.pack(fill='both', expand=True)
            self.notebook.add(self.user_page, text="Users")
    
    def load_product_page(self):
        self.product_page = Product(self, database)
        self.notebook.pack(fill='both', expand=True)
        self.notebook.add(self.product_page, text="Product")
        self.notebook.select(self.product_page)
        
        



mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
database = mongo_client["db_plm"]

app = App(database)
app.mainloop()