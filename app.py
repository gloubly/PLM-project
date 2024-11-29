import tkinter as tk
from tkinter import ttk
import pymongo
from products_page import ProductsPage

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
database = mongo_client["db_plm"]["projects"]

#https://stackoverflow.com/questions/17466561/what-is-the-best-way-to-structure-a-tkinter-application
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("App")
        self.state('zoomed')
        #LoginPage(self)
        #ProductsPage(self)
        Menu(self)


class Ingredients(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

class Menu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.current_page = None

        self.pages = {
            "Products": ProductsPage,
            "Ingredients": Ingredients,
            "Ingredients2": Ingredients,
            "Ingredients3": Ingredients,
        }

        buttons_frame = tk.Frame(self.parent)
        buttons_frame.pack(pady=10)
        for i, label in enumerate(self.pages):
            tk.Button(buttons_frame, text=label, command=lambda page=label: self.load_page(page), padx=10).grid(row=0, column=i, padx=5)

        self.content_frame = tk.Frame(self.parent)
        self.content_frame.pack()
    
    def load_page(self, page_name):
        """Load the specified page."""
        if self.current_page == page_name:
            return  # Avoid reloading the same page
        
        # Clear the content frame and load the new page
        self.clear_frame()
        page_class = self.pages[page_name]
        self.current_page = page_name
        page_class(self.content_frame).pack(fill=tk.BOTH, expand=True)

    
    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()



        

########################################---------------------########################################
########################################------TEST PART------########################################
########################################---------------------########################################

class test(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("App")
        self.state('zoomed')
        Menu(self)
        self.after(10000, lambda:self.destroy())
    
    def test(self):
        pass


    
app = App()
app.mainloop()