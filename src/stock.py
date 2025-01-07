import tkinter as tk
from tkinter import ttk
from datetime import datetime
from bson import ObjectId
from utils import Placeholder_Entry, str_to_date, date_to_str, validate_float, date_popup, clear_frame, TreeEntryPopup
from tkinter.messagebox import showerror
from tkcalendar import Calendar
from test import TestApp

STOCK_COLUMNS = {
    'name': .2,
    'quantity': .2,
    'unit': .2,
    'expiry_date': .2,
    'price': .2
}

class StockPage(tk.Frame):
    def __init__(self, parent, database, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.stock_collection = database['stock']
        screen_width = parent.notebook.winfo_screenwidth()
        self.selected_row = None

        tree_frame = tk.Frame(self)
        tree_frame.pack()
        self.combobox = ttk.Combobox(tree_frame, values=['products', 'ingredients'], state='readonly')
        self.combobox.current(0)
        self.combobox.bind('<<ComboboxSelected>>', self.toggle_item_type)
        self.combobox.pack()

        tree_ingredients_width = screen_width * 0.5

        self.tree = ttk.Treeview(tree_frame, columns=STOCK_COLUMNS.keys(), show="headings", height=15)
        self.tree.tag_configure('Blue', background="light sky blue")
        self.tree.tag_configure('White', background="white")
        self.tree.tag_configure('Expired', background="red")
        self.tree.pack(side='left')
        for (col, prop), tree_col in zip(STOCK_COLUMNS.items(), self.tree["columns"]):
            self.tree.heading(tree_col, text=col.replace("_", " ").title())
            self.tree.column(tree_col, width=int(tree_ingredients_width*prop), anchor="w")

        tree_scrollbar = tk.Scrollbar(tree_frame, command=self.tree.yview)
        tree_scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree_menu = tk.Menu(tree_frame, tearoff=0)
        self.tree_menu.add_command(label="Remove", command=self.remove_item)
        self.tree.bind("<Button-3>", self.on_right_click)
        self.tree.bind("<Double-1>", self.on_double_click)

        self.tree_error_var = tk.StringVar(self, value='')
        tk.Label(self, textvariable=self.tree_error_var, fg='red').pack(pady=3)

        self.load_stock()

        self.form_frame = tk.Frame(self, relief='groove', borderwidth=1, padx=5, pady=5)
        self.form_frame.pack(pady=(20,0))
        item_type = self.combobox.get().rstrip('s')
        tk.Label(self.form_frame, text='Name', width=10, anchor='w').grid(row=0, column=0, sticky='nw', pady=5)
        self.name_entry = Placeholder_Entry(self.form_frame, placeholder='Name', width=18)
        self.name_entry.grid(row=0, column=1, pady=5, sticky="ne")

        tk.Label(self.form_frame, text='Quantity', width=10, anchor='w').grid(row=1, column=0, sticky='nw', pady=5)
        self.quantity_entry = Placeholder_Entry(self.form_frame, placeholder='Quantity', width=18)
        self.quantity_entry.grid(row=1, column=1, pady=5, sticky="ne")

        tk.Label(self.form_frame, text='Unit', width=10, anchor='w').grid(row=2, column=0, sticky='nw', pady=5)
        self.unit_entry = Placeholder_Entry(self.form_frame, placeholder='Unit', width=18)
        self.unit_entry.configure(validatecommand=(self.register(validate_float), '%P'), validate="key")
        self.unit_entry.grid(row=2, column=1, pady=5, sticky="ne")

        tk.Label(self.form_frame, text='Expiry Date', width=10, anchor='w').grid(row=3, column=0, sticky='nw', pady=5)
        self.expiry_date_var = tk.StringVar(self.form_frame, value=date_to_str(datetime.now()))
        date_label = tk.Label(self.form_frame, textvariable=self.expiry_date_var, width=15, bg='white', anchor='w')
        date_label.bind("<Button-1>", lambda event: date_popup(self.expiry_date_var, event))
        date_label.grid(row=3, column=1)

        tk.Label(self.form_frame, text='Price', width=10, anchor='w').grid(row=4, column=0, sticky='nw', pady=5)
        self.price_entry = Placeholder_Entry(self.form_frame, placeholder='Price', width=18)
        self.price_entry.configure(validatecommand=(self.register(validate_float), '%P'), validate="key")
        self.price_entry.grid(row=4, column=1, pady=5, sticky="ne")

        tk.Label(self.form_frame, text='Type', width=10, anchor='w').grid(row=5, column=0, sticky='nw', pady=5)
        self.label_type_var = tk.StringVar(self, value=item_type.capitalize())
        tk.Label(self.form_frame, textvariable=self.label_type_var, width=15, bg='white', anchor='w').grid(row=5, column=1)

        self.button_var = tk.StringVar(self, value=f'Add {item_type.capitalize()}')
        ttk.Button(self.form_frame, textvariable=self.button_var, command=self.add_item, width=15).grid(row=6, column=0, columnspan=2, pady=5)
        self.form_error_var = tk.StringVar(self, value='')
        tk.Label(self.form_frame, textvariable=self.form_error_var, fg='red').grid(row=7, column=0, columnspan=2)
    
    def add_item(self):
        item_type = self.combobox.get().rstrip('s')
        assert(item_type=='ingredient' or item_type=='product'), item_type
        if any(var.get()=="" or var.get()==var.placeholder for var in [self.name_entry, self.quantity_entry, self.unit_entry, self.price_entry]):
            self.form_error_var.set('Please fill out all the entries')
            return None
        values = {
            'name':self.name_entry.get(),
            'quantity':self.quantity_entry.get(),
            'unit':self.unit_entry.get(),
            'expiry_date':str_to_date(self.expiry_date_var.get()),
            'price':float(self.price_entry.get()),
            'type':item_type,
        }
        req = self.stock_collection.insert_one(values)
        n_rows = len(self.tree.get_children())
        tag = 'Expired' if values['expiry_date']<=datetime.now() else 'Blue' if n_rows%2==0 else 'White'
        if 'Expired'==tag:
            self.warn_expired()
        self.tree.insert("", "end", iid=req.inserted_id, values=[values[col] if 'date' not in col else date_to_str(values[col]) for col in STOCK_COLUMNS], tags = (tag))
        self.reset_form()

    def update_tree_tags(self):
        has_expired=False
        now = datetime.now()
        for i, row in enumerate(self.tree.get_children()):
            expiry_date = self.tree.item(row)["values"][list(STOCK_COLUMNS.keys()).index('expiry_date')]
            tag = 'Expired' if str_to_date(expiry_date)<=now else 'Blue' if i%2==0 else 'White'
            if 'Expired'==tag:
                has_expired=True
                self.warn_expired()
            self.tree.item(row, tags = (tag))
        if not has_expired:
            self.tree_error_var.set('')

    def remove_item(self):
        print(self.selected_row)
        req = self.stock_collection.delete_one({'_id': ObjectId(self.selected_row)})
        if req.deleted_count==0:
            showerror("DB error", f'Could not remove item {self.selected_row}')
        else:
            self.tree.delete(self.selected_row)
            self.update_tree_tags()
    
    def on_right_click(self, event):
        self.selected_row = self.tree.identify_row(event.y)
        if self.selected_row:
            self.tree.selection_set(self.selected_row)
            try:
                self.tree_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.tree_menu.grab_release()
    
    def on_double_click(self, event):
        self.selected_row = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        try:
            x, y, width, _ = self.tree.bbox(self.selected_row, column)
        except:
            pass
        else:
            cell_text = self.tree.item(self.selected_row, 'text') or self.tree.set(self.selected_row, column)
            entryPopup = TreeEntryPopup(self.tree, self.selected_row, column, cell_text, exit_fct=self.update_item)
            col_index = int(column[1])-1 # column = #1, #2, ... begins at 1
            col = list(STOCK_COLUMNS.keys())[col_index]
            if col in ['quantity', 'price']:
                entryPopup.configure(validatecommand=(self.register(validate_float), '%P'), validate="key")
            if col!='expiry_date':
                entryPopup.place(x=x, y=y, anchor='w', width=width)
                self.tree.bind("<Button-1>", lambda event: entryPopup.destroy())
            else:
                self.date_cell_var = tk.StringVar(self, cell_text)
                self.tree_date_popup(event)

    def tree_date_popup(self, event):
        def validate(event=None):
            self.date_cell_var.set(date_to_str(datetime.strptime(calendar.get_date(), '%m/%d/%y')))
            self.tree.item(self.selected_row)
            if self.update_item(column, self.date_cell_var.get(), previous_val):
                self.tree.set(self.selected_row, column, self.date_cell_var.get())
                self.update_tree_tags()
            new_window.destroy()
        
        column = self.tree.identify_column(event.x)
        date_split = self.date_cell_var.get().split("/")
        previous_val = self.date_cell_var.get()
        new_window = tk.Toplevel()
        calendar = Calendar(new_window, selectmode = 'day', day=int(date_split[0]), month=int(date_split[1]), year=int(date_split[2]))
        for row in calendar._calendar:
            for lbl in row:
                lbl.bind('<Double-1>', validate)
        calendar.pack()
        ttk.Button(new_window, text="Validate", command=validate).pack()
        new_window.geometry("+%d+%d" % (event.x_root-new_window.winfo_reqwidth()//2,event.y_root))
    
    def update_item(self, column, new_val, previous_val):
        if previous_val==new_val:
            return True
        col_index = int(column[1])-1
        col = list(STOCK_COLUMNS.keys())[col_index]
        new_val = float(new_val) if col in ['quantity', 'price'] else str_to_date(new_val) if col=='expiry_date' else new_val

        req = self.stock_collection.update_one({'_id':ObjectId(self.selected_row)}, {"$set": {col:new_val}})
        if req.modified_count==0:
            showerror('DB error', f'Could not update item {self.selected_row}')
        return True

    def toggle_item_type(self, event):
        self.load_stock()
        self.reset_form()
        item_type = self.combobox.get().rstrip('s')
        self.label_type_var.set(item_type.capitalize())
        self.button_var.set(f'Add {item_type.capitalize()}')

    def reset_form(self):
        self.name_entry.reset_placeholder()
        self.unit_entry.reset_placeholder()
        self.price_entry.reset_placeholder()
        self.quantity_entry.reset_placeholder()
        self.expiry_date_var.set(date_to_str(datetime.now()))
        self.form_error_var.set('')

    def load_stock(self):
        self.tree_error_var.set('')
        now = datetime.now()
        item_type = self.combobox.get().rstrip('s')
        assert(item_type=='product' or item_type=='ingredient'), item_type
        self.clear_tree()
        req = self.stock_collection.find({'type':item_type}).to_list()
        for i, item in enumerate(req):
            tag = 'Expired' if item['expiry_date']<=now else 'Blue' if i%2==0 else 'White'
            if tag == 'Expired':
                self.warn_expired()
            self.tree.insert("", "end", iid=item["_id"], values=[item[col] if 'date' not in col else date_to_str(item[col]) for col in STOCK_COLUMNS], tags = (tag))
    
    def clear_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
    
    def warn_expired(self):
        self.tree_error_var.set(f'Warning: some {self.combobox.get()} have expired')



if __name__ == '__main__':
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["db_plm"]
    app = TestApp(database, timeout=20000)

    app.stock = StockPage(app, app.database)
    
    app.notebook.add(app.stock, text="Stock")
    app.notebook.select(app.stock)
    app.mainloop()