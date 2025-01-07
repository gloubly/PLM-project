import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkcalendar import Calendar
import re
from collections.abc import Callable

def create_checkboxes(frame:tk.Frame, properties:list[str]):
    checkboxes = []
    for i, prop in enumerate(properties):
        checkbox_var = tk.BooleanVar()
        tk.Checkbutton(frame, text=prop, variable=checkbox_var).grid(row=i+1, sticky='w')
        checkboxes.append(checkbox_var)
    return checkboxes
    #to get the list of the checked properties: [prop for prop, box in zip(properties, checkboxes) if box.get()]

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def scrollable_label(parent, width, height, stringvar=None, text=None):

    def scroll(event):
        if scrollbar.get()!=(0.0, 1.0): # scroll only if needed
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    assert(not(text is not None and stringvar is not None)), "Use stringvar OR text" # ensure only one is declared

    # Create a frame to hold the canvas and scrollbar
    outer_frame = tk.Frame(parent, width=width, height=height, borderwidth=1, relief="groove", bg='white')
    outer_frame.pack(fill='both')
    
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

###########
## DATES ##
###########

DATE_FORMAT = "%d/%m/%Y"

def str_to_date(s):
    return datetime.strptime(s, DATE_FORMAT)

def date_to_str(date):
    return datetime.strftime(date, DATE_FORMAT)

#################
## Check entry ##
#################

def validate_float(s):
    return re.match(r"^[0-9]+(\.[0-9]*)?$", s) is not None or s==""

def validate_int(s:str):
    return s.isdecimal() or s==""

# allow to add a placeholder text on an entry

class Placeholder_Entry(ttk.Entry):
    def __init__(self, parent, placeholder='', **kwargs):
        super().__init__(parent, **kwargs)
        self.placeholder = placeholder
        self.parent = parent
        self.add_placeholder()

    def add_placeholder(self):
        self.delete(0, 'end')
        self.insert(0, self.placeholder)
        self.config(foreground="gray")
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, event):
        self.config(foreground="black")
        if self.get() == self.placeholder:
            self.delete(0, 'end')
        self.config(validate='key')
    
    def on_focus_out(self, event):
        self.config(validate='none')
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(foreground="gray")
    
    def reset_placeholder(self):
        self.config(validate='none')
        self.delete(0, 'end')
        self.insert(0, self.placeholder)
        self.config(foreground="gray")
        self.parent.focus()

    def set(self, s:str):
        self.delete(0, 'end')
        self.insert(0, s)
        self.config(foreground="black")


class TreeEntryPopup(tk.Entry):
    def __init__(self, parent, iid, column:str, text, exit_fct:Callable=None, **kw):
        super().__init__(parent, **kw)
        self.tv = parent
        self.iid = iid
        self.column = column
        self.exit_fct = exit_fct
        self.original_text = text

        self.insert(0, text) 
        self['exportselection'] = False

        self.focus_force()
        self.bind("<Return>", self.on_return)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", lambda *args: self.destroy())

    def on_return(self, event):
        if self.exit_fct:
            if self.exit_fct(self.column, self.get(), self.original_text):
                # exit performed normally
                self.tv.set(self.iid, self.column, self.get())
        else:
            self.tv.set(self.iid, self.column, self.get())
        self.tv.unbind('<Button-1>')
        self.destroy()

    def select_all(self, *ignore):
        self.selection_range(0, 'end') # Ctrl+A
        return 'break' # returns 'break' to interrupt default key-bindings


def date_popup(stringvar:tk.StringVar, event):
    def validate(event=None):
        stringvar.set(date_to_str(datetime.strptime(calendar.get_date(), '%m/%d/%y')))
        new_window.destroy()
    
    date_split = stringvar.get().split("/")
    new_window = tk.Toplevel()
    calendar = Calendar(new_window, selectmode = 'day', day=int(date_split[0]), month=int(date_split[1]), year=int(date_split[2]))
    for row in calendar._calendar:
        for lbl in row:
            lbl.bind('<Double-1>', validate)
    calendar.pack()
    ttk.Button(new_window, text="Validate", command=validate).pack()
    new_window.geometry("+%d+%d" % (event.x_root-new_window.winfo_reqwidth()//2,event.y_root))