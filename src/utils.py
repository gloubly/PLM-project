import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, askokcancel
from bson import ObjectId

def add_stringvar(stringvar: tk.StringVar, text, sep='\n'):
    s = stringvar.get()
    stringvar.set(s + sep + text)

def remove_last(stringvar: tk.StringVar, sep='\n'):
    s = stringvar.get()
    index = s.rfind(sep)
    stringvar.set(s[:index])

def create_checkboxes(frame:tk.Frame, properties:list[str]):
    checkboxes = []
    for i, prop in enumerate(properties):
        checkbox_var = tk.BooleanVar()
        tk.Checkbutton(frame, text=prop, variable=checkbox_var).grid(row=i+1, sticky='w')
        checkboxes.append(checkbox_var)
    return checkboxes
    #to get the list of the checked properties: [prop for prop, box in zip(properties, checkboxes) if box.get()]


def scrollable_label(parent, width, height, stringvar=None, text=None):

    def scroll(event):
        if scrollbar.get()!=(0.0, 1.0): # scroll only if needed
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    assert(not(text is not None and stringvar is not None)), "Use stringvar OR text" # ensure only one is declared

    # Create a frame to hold the canvas and scrollbar
    outer_frame = tk.Frame(parent, width=width, height=height, borderwidth=1, relief="groove", bg='white')
    outer_frame.pack(fill='both')
    
    # Create a canvas
    canvas = tk.Canvas(outer_frame, bg='white', width=width, height=height)
    canvas.pack(side='left')
    
    # Add a vertical scrollbar
    scrollbar = tk.Scrollbar(outer_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas_width = canvas.winfo_reqwidth()

    # Create a frame inside the canvas to hold the label
    inner_frame = tk.Frame(canvas)
    inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas_frame = canvas.create_window((0, 0), window=inner_frame, anchor="nw", )
    
    canvas.itemconfig(canvas_frame, width=canvas_width-5)

    if stringvar is not None:
        tk.Label(inner_frame, textvariable=stringvar, justify="left", wraplength=canvas_width-10, bg="white", width=0, anchor='nw').pack(anchor="nw", fill='x', expand=True)
    else:
        tk.Label(inner_frame, text=text, justify="left", wraplength=canvas_width-10, bg="white", width=0, anchor='nw').pack(anchor="nw", fill='x', expand=True)

    canvas.bind_all("<MouseWheel>", scroll)

    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


# allow to add a placeholder text on an entry
class Custom_Entry(ttk.Entry):
    def __init__(self, parent, placeholder='', **kwargs):
        super().__init__(parent, **kwargs)
        self.placeholder = placeholder
        self.add_placeholder()


    def add_placeholder(self):
        self.insert(0, self.placeholder)
        self.config(foreground="gray")
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, 'end')
            self.config(foreground="black")
    
    def on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(foreground="gray")