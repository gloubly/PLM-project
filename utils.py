import tkinter as tk

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
