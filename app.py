import tkinter as tk
import pymongo
from products import ProductsPage
from login import LoginPage
from ingredients import IngredientsPage
from recipes import Recipes

#https://stackoverflow.com/questions/17466561/what-is-the-best-way-to-structure-a-tkinter-application
class App(tk.Tk):
    def __init__(self, database, timeout=None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.database = database
        self.wm_title("App")
        self.state('zoomed')
        if timeout is not None:
            self.after(timeout, lambda:self.destroy()) # for testing
        
        login = LoginPage(self, self.database)
        login.pack()


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
        self.content_frame.pack()
    
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

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
database = mongo_client["db_plm"]["projects"]

app = App(database, 10000)
app.mainloop()