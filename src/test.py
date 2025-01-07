import tkinter as tk
from tkinter import ttk

# test class to test each page individually
class TestApp(tk.Tk):
    def __init__(self, database, timeout=None, skip=False, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.database = database
        self.wm_title("App")
        self.state('zoomed')
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        if timeout is not None:
            self.after(timeout, lambda:self.destroy()) # auto delete window after x seconds