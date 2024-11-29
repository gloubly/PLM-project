import tkinter as tk
import pymongo
from products import ProductsPage
from login import LoginPage
from ingredients import IngredientsPage
from recipes import RecipesPage

# https://stackoverflow.com/questions/17466561/what-is-the-best-way-to-structure-a-tkinter-application
class App(tk.Tk):
    def __init__(self, database, timeout=None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.database = database
        self.wm_title("App")
        self.state('zoomed')
        if timeout is not None:
            self.after(timeout, lambda:self.destroy()) # for testing
        
        self.login_page()


    def menu(self):
        self.pages = {
            "Products": ProductsPage,
            "Ingredients": IngredientsPage,
            "Recipes": RecipesPage,
            "Ingredients3": IngredientsPage,
        }
        self.current_page = None

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=10)
        for i, label in enumerate(self.pages):
            tk.Button(buttons_frame, text=label, command=lambda page=label: self.load_page(page), padx=10).grid(row=0, column=i, padx=5)

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill='both', expand=True)
    
    def load_page(self, page_name):
        if self.current_page == page_name:
            return  # Avoid reloading the same page
        
        # Clear the content frame and load the new page
        self.clear_frame()
        page_class = self.pages[page_name]
        self.current_page = page_name
        page_class(self.content_frame, self.database).pack(fill="both", expand=True)

    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
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
        password_entry.pack(pady=(0, 20))

        # buttons
        tk.Button(login_frame, text="Login", font=(17), padx=10, pady=0, relief="groove", borderwidth=2, fg='white', bg=INNER_BG_COLOR,
                  activebackground='white', activeforeground=INNER_BG_COLOR,
                  command=lambda: self.login(username_entry.get(), password_entry.get(), error_var)).pack()
        tk.Label(login_frame, textvariable=error_var, bg=FRAME_BG_COLOR, fg='red').pack()

    def login(self, username, password, stringvar):
        if username!="" and password!="":
            project = self.database["users"].find_one({"username":username, "password":password})
            if project:
                stringvar.set("")
                for widget in self.winfo_children():
                    widget.destroy()
                self.menu()
            else:
                stringvar.set("error login")


mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
database = mongo_client["db_plm"]

app = App(database, 20000)
app.mainloop()