import tkinter as tk

class RecipesPage(tk.Frame):
    def __init__(self, parent, database, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.database = database

        title_frame = tk.Frame(self.parent, bg="#4CAF50", relief=tk.RAISED, bd=2)
        title_frame.pack(side='top', fill='x')
        tk.Label(
            title_frame, 
            text="Recipes", font=("Helvetica", 20, "bold"), 
            fg="white", bg="#4CAF50", pady=4
        ).pack(pady=10)