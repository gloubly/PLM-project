import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from utils import Placeholder_Entry, TreeEntryPopup
from tkinter.messagebox import showerror
import pymongo
from datetime import datetime
import re
import tkinter.font as tkfont

DATE_FORMAT = "%d/%m/%Y"

INGREDIENTS_COLUMNS = {
    "name": 0.4,
    "quantity": 0.3,
    "unit": 0.3
}

def validate_float(s):
    return re.match(r"^[0-9]+(\.[0-9]*)?$", s) is not None or s==""

def str_to_date(s):
    return datetime.strptime(s, DATE_FORMAT)

def date_to_str(date):
    return datetime.strftime(date, DATE_FORMAT)

class Product(tk.Frame):
    def __init__(self, parent, database, product_id:int=-1, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        tk.Label(self, text='Products', font=('Cascadia Code', 20), relief='groove', anchor='center', borderwidth=2, bg='#d1d1d1').pack(fill='both', pady=5)
        self.products_collection = database['products']
        self.product_id = product_id
        self.parent = parent
        screen_width = parent.notebook.winfo_screenwidth()

        left_frame = tk.Frame(self)
        left_frame.pack(side="left", padx=(screen_width*0.2, 0))

        self.lauching_date_var = tk.StringVar(left_frame, f"{date_to_str(datetime.now())}")
        self.version_var = tk.StringVar(left_frame, "")
        self.change_type_var = tk.StringVar(left_frame, "")
        self.new_version_var = tk.StringVar(left_frame, "1.0.0")
        self.error_var = tk.StringVar(left_frame, "")

        tk.Label(left_frame, text="Name").grid(row=0, column=0, sticky='nw', pady=5)
        self.name_entry = Placeholder_Entry(left_frame, placeholder="Name")
        self.name_entry.bind('<KeyPress>', self.on_change)
        self.name_entry.grid(row=0, column=1, pady=5)
        tk.Label(left_frame, text="Category").grid(row=1, column=0, sticky='nw', pady=5)
        self.category_entry = Placeholder_Entry(left_frame, placeholder="Category")
        self.category_entry.bind('<KeyPress>', self.on_change)
        self.category_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(left_frame, text="Lauching Date").grid(row=2, column=0, sticky='nw', pady=5)
        date_label = tk.Label(left_frame, textvariable=self.lauching_date_var, width=17, bg='white', anchor='w')
        date_label.bind("<Button-1>", self.choose_date)
        date_label.grid(row=2, column=1, pady=5)

        tk.Label(left_frame, text="Batch Yield").grid(row=5, column=0, sticky='nw', pady=5)
        self.batch_yield_entry = Placeholder_Entry(left_frame, placeholder="Batch Yield")
        self.batch_yield_entry.configure(validatecommand=(self.register(validate_float), '%P'), validate="key")
        self.batch_yield_entry.bind('<KeyPress>', self.on_change)
        self.batch_yield_entry.grid(row=5, column=1, pady=5)
        tk.Label(left_frame, text="Unit").grid(row=6, column=0, sticky='nw', pady=5)
        self.unit_entry = Placeholder_Entry(left_frame, placeholder="Unit")
        self.unit_entry.bind('<KeyPress>', self.on_change)
        self.unit_entry.grid(row=6, column=1, pady=5)
        tk.Label(left_frame, text="Price").grid(row=7, column=0, sticky='nw', pady=5)
        self.price_entry = Placeholder_Entry(left_frame, placeholder="Price")
        self.price_entry.bind('<KeyPress>', self.on_change)
        self.price_entry.configure(validatecommand=(self.register(validate_float), '%P'), validate="key")
        self.price_entry.grid(row=7, column=1, pady=5)
        tk.Label(left_frame, text="Version").grid(row=8, column=0, sticky='nw', pady=5)
        if product_id==-1:
            tk.Label(left_frame, textvariable=self.new_version_var, background='white', width=17, anchor='w').grid(row=8, column=1, pady=5)
        else:
            tk.Label(left_frame, textvariable=self.version_var, background='white', width=17, anchor='w').grid(row=8, column=1, pady=5)

            tk.Label(left_frame, text="Change Type").grid(row=9, column=0, sticky='nw', pady=(5,0))
            change_type_frame = tk.Frame(left_frame)
            change_type_frame.grid(row=10, column=0, pady=(0,5), columnspan=2)
            ttk.Radiobutton(change_type_frame, text="Major", value="0", variable=self.change_type_var).grid(column=0, row=0)
            ttk.Radiobutton(change_type_frame, text="Minor", value="1", variable=self.change_type_var).grid(column=1, row=0)
            ttk.Radiobutton(change_type_frame, text="Patch", value="2", variable=self.change_type_var).grid(column=2, row=0)
            self.change_type_var.set("2")
            self.change_type_var.trace_add('write', self.update_new_version)

            tk.Label(left_frame, text="Next Version").grid(row=11, column=0, sticky='nw', pady=5)
            tk.Label(left_frame, textvariable=self.new_version_var, background='white', width=17, anchor='w').grid(row=11, column=1, pady=5)

        ttk.Button(left_frame, text="Save changes", command=self.update_product).grid(row=12, column=0, columnspan=2, pady=5)
        tk.Label(left_frame, textvariable=self.error_var, fg='red').grid(row=13, column=0, columnspan=2, pady=5)

        # right frame
        right_frame = tk.Frame(self)
        right_frame.pack(side="right", padx=(0, screen_width*0.2))

        self.selected_row = None
        tree_ingredients_width = screen_width * 0.3
        tk.Label(right_frame, text="Ingredients").pack(pady=5)
        self.tree_ingredients = ttk.Treeview(right_frame, columns=INGREDIENTS_COLUMNS.keys(), show="headings", height=8)
        self.tree_ingredients.pack()
        for (col, prop), tree_col in zip(INGREDIENTS_COLUMNS.items(), self.tree_ingredients["columns"]):
            self.tree_ingredients.heading(tree_col, text=col.replace("_", " ").title())
            self.tree_ingredients.column(tree_col, width=int(tree_ingredients_width*prop), anchor="w")

        self.tree_ingredients_menu = tk.Menu(right_frame, tearoff=0)
        self.tree_ingredients_menu.add_command(label="Remove", command=lambda: self.tree_ingredients.delete(self.selected_row))
        self.tree_ingredients.bind("<Button-3>", self.on_right_click)
        self.tree_ingredients.bind("<Double-1>", self.on_double_click)

        ttk.Button(right_frame, text="Add ingredient", command=self.add_ingredient).pack(pady=5)

        tk.Label(right_frame, text="Recipe").pack(pady=(5,0))
        recipe_text_frame = tk.Frame(right_frame)
        recipe_text_frame.pack(pady=(0,5))
        self.recipe_text = tk.Text(recipe_text_frame, height=8)
        text_font = tkfont.nametofont(self.recipe_text.cget('font'))
        recipe_scrollbar = tk.Scrollbar(recipe_text_frame, command=self.recipe_text.yview)
        self.recipe_text.configure(yscrollcommand=recipe_scrollbar.set)
        self.recipe_text.pack(side='left')
        recipe_scrollbar.pack(side='right', fill='y')
        self.recipe_text.configure(width=int((tree_ingredients_width-float(recipe_scrollbar.cget('width')))/text_font.measure("m")))

        if self.product_id!=-1:
            self.load_product()


    def load_product(self):
        assert(isinstance(self.product_id, int)), "product_id should be an integer"
        if self.product_id!=-1:
            req = self.products_collection.find({'product_id': self.product_id}).to_list()
            if len(req)==0:
                showerror("Error", f"Could not load product {self.product_id}")
                return None
            data = req[0]
            self.name_entry.set(data['name'])
            self.category_entry.set(data['category'])
            self.lauching_date_var.set(date_to_str(data['launching_date']))
            self.batch_yield_entry.set(data['batch_yield'])
            self.unit_entry.set(data['unit'])
            self.price_entry.set(data['price'])
            self.version_var.set(data['version'])
            self.recipe_text.insert("1.0", data['recipe'])
            for i, item in enumerate(data['ingredients']):
                self.tree_ingredients.insert("", "end", values=[item[col] for col in INGREDIENTS_COLUMNS], tags = ('Blue' if i%2==0 else 'White'))
            self.update_new_version()
            self.lauching_date_var.trace_add('write', self.on_change)

    def update_product(self):
        assert(isinstance(self.product_id, int)), "product_id should be an integer"
        if self.name_entry.get()=='Name' or self.category_entry.get()=="Category" or self.recipe_text.get("1.0", "end").strip()=="" or self.batch_yield_entry.get()=="Batch Yield" or self.unit_entry.get()=="Unit" or self.price_entry.get()=="Price" or len(self.get_ingredients())==0:
            self.error_var.set('Please fill out all the entries')
            return None
        if self.product_id==-1:
            req = self.products_collection.aggregate([{"$group":{"_id": "null","max": { "$max": "$product_id"}}}])
            self.product_id = req.to_list()[0]['max'] + 1 # set a new id
        else:
            self.products_collection.aggregate([{"$match": {"product_id": self.product_id}},{"$set":{"fk_product_id": "$product_id"}},{"$project": {"product_id": 0}}, {"$merge": {"into": "productsHistory"}}]) # copy into history before 
        values = {
            'name': self.name_entry.get(),
            'category': self.category_entry.get(),
            'launching_date': str_to_date(self.lauching_date_var.get()),
            'ingredients': self.get_ingredients(),
            'recipe': self.recipe_text.get("1.0", "end").strip(),
            'batch_yield': float(self.batch_yield_entry.get()),
            'unit': self.unit_entry.get(),
            'price': float(self.price_entry.get()),
            'version': self.new_version_var.get()
        }
        self.products_collection.update_one({"product_id": self.product_id}, {"$set": values}, upsert=True)
        self.error_var.set("")
        self.parent.notebook.forget(self.parent.product_page)
        self.parent.notebook.select(self.parent.products_page)
        self.parent.products_page.refresh_products()

    def update_new_version(self, *args):
        version_array = self.version_var.get().split(".")
        index = int(self.change_type_var.get())
        version_array[index] = str(int(version_array[index]) + 1)
        self.new_version_var.set(".".join(version_array))

    # def reset_placeholders(self):
    #     self.name_entry.reset_placeholder()
    #     self.category_entry.reset_placeholder()
    #     self.batch_yield_entry.reset_placeholder()
    #     self.unit_entry.reset_placeholder()
    #     self.price_entry.reset_placeholder()
    #     self.version_var.set("1.0.0")
    #     self.lauching_date_var.set(date_to_str(datetime.now()))

    def choose_date(self, event):
        def validate(event=None):
            self.lauching_date_var.set(datetime.strftime(datetime.strptime(calendar.get_date(), '%m/%d/%y'), DATE_FORMAT))
            new_window.destroy()
        
        date_split = self.lauching_date_var.get().split("/")
        new_window = tk.Toplevel()
        calendar = Calendar(new_window, selectmode = 'day', day=int(date_split[0]), month=int(date_split[1]), year=int(date_split[2]))
        for row in calendar._calendar:
            for lbl in row:
                lbl.bind('<Double-1>', validate)
        calendar.pack()
        ttk.Button(new_window, text="Validate", command=validate).pack()
        new_window.geometry("+%d+%d" % (event.x_root-new_window.winfo_reqwidth()//2,event.y_root))
        
    def get_ingredients(self):
        return [{column:float(value) if column=='quantity' else value for value, column in zip(self.tree_ingredients.item(row)["values"], INGREDIENTS_COLUMNS)} for row in self.tree_ingredients.get_children()]

    def add_ingredient(self):
        self.tree_ingredients.insert("", "end", values=["name", "0", "unit"])
        self.on_change()

    def on_double_click(self, event):
        row = self.tree_ingredients.identify_row(event.y)
        column = self.tree_ingredients.identify_column(event.x)
        x, y, width, _ = self.tree_ingredients.bbox(row, column)
        self.cell_text = self.tree_ingredients.item(row, 'text') or self.tree_ingredients.set(row, column)
        self.entryPopup = TreeEntryPopup(self.tree_ingredients, row, column, self.cell_text)
        if int(column[1])==2: # column = #1, #2, ...
            self.entryPopup.configure(validatecommand=(self.register(validate_float), '%P'), validate="key")
        self.entryPopup.place(x=x, y=y, anchor='w', width=width)
        self.tree_ingredients.bind("<Button-1>", lambda event: self.close_popup() if self.entryPopup else None)

    def on_right_click(self, event):
        self.selected_row = self.tree_ingredients.identify_row(event.y)
        if self.selected_row:
            self.tree_ingredients.selection_set(self.selected_row)
            try:
                self.tree_ingredients_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.tree_ingredients_menu.grab_release()

    def close_popup(self):
        if self.entryPopup:
            if self.entryPopup.get()!=self.cell_text:
                self.on_change()
            self.entryPopup.destroy()
            self.entryPopup = None

    def on_change(self, *args):
        self.error_var.set("Warning, you have unsaved changes !")