import tkinter as tk
from tkinter import ttk
from utils import Placeholder_Entry, TreeEntryPopup, str_to_date, date_to_str, validate_float, date_popup
from tkinter.messagebox import showerror, askyesno
from test import TestApp
from datetime import datetime
import tkinter.font as tkfont
import locale

DATE_FORMAT = "%d/%m/%Y"

INGREDIENTS_COLUMNS = {
    "name": 0.4,
    "quantity": 0.3,
    "unit": 0.3
}

class SingleProductPage(tk.Frame):
    def __init__(self, parent, database, product_id:int=-1, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        tk.Label(self, text='Product', font=('Cascadia Code', 20), relief='groove', anchor='center', borderwidth=2, bg='#d1d1d1').pack(fill='both', pady=5)
        self.products_collection = database['products']
        self.history_collection = database['productsHistory']
        self.product_id = product_id
        self.parent = parent
        screen_width = parent.notebook.winfo_screenwidth()

        self.content_frame = tk.Frame(self)
        self.content_frame.pack()

        form_frame = tk.Frame(self.content_frame)
        form_frame.grid(row=0, column=0, sticky='n', padx=10)

        self.launching_date_var = tk.StringVar(form_frame, date_to_str(datetime.now()))
        self.version_var = tk.StringVar(form_frame, "")
        self.change_type_var = tk.StringVar(form_frame, "")
        self.new_version_var = tk.StringVar(form_frame, "1.0.0")
        self.error_var = tk.StringVar(form_frame, "")

        tk.Label(form_frame, text="Name", width=12, anchor='w').grid(row=0, column=0, sticky='nw', pady=5)
        self.name_entry = Placeholder_Entry(form_frame, placeholder="Name", width=17)
        self.name_entry.bind('<KeyPress>', self.on_change)
        self.name_entry.grid(row=0, column=1, pady=5, sticky="ne")

        tk.Label(form_frame, text="Category", width=12, anchor='w').grid(row=0, column=2, sticky='nw', pady=5)
        self.category_entry = Placeholder_Entry(form_frame, placeholder="Category", width=17)
        self.category_entry.bind('<KeyPress>', self.on_change)
        self.category_entry.grid(row=0, column=3, pady=5, sticky="ne")
        
        tk.Label(form_frame, text="Launching Date", width=12, anchor='w').grid(row=1, column=0, sticky='nw', pady=5)
        self.date_label = tk.Label(form_frame, textvariable=self.launching_date_var, width=14, bg='white', anchor='w')
        self.date_label.bind("<Button-1>", lambda event: date_popup(self.launching_date_var, event))
        self.date_label.grid(row=1, column=1, pady=5, sticky="ne")

        tk.Label(form_frame, text="Price", width=12, anchor='w').grid(row=1, column=2, sticky='nw', pady=5)
        self.price_entry = Placeholder_Entry(form_frame, placeholder="Price", width=17)
        self.price_entry.bind('<KeyPress>', self.on_change)
        self.price_entry.configure(validatecommand=(self.register(validate_float), '%P'), validate="key")
        self.price_entry.grid(row=1, column=3, pady=5, sticky="ne")

        tk.Label(form_frame, text="Batch Yield", width=12, anchor='w').grid(row=2, column=0, sticky='nw', pady=5)
        self.batch_yield_entry = Placeholder_Entry(form_frame, placeholder="Batch Yield", width=17)
        self.batch_yield_entry.configure(validatecommand=(self.register(validate_float), '%P'), validate="key")
        self.batch_yield_entry.bind('<KeyPress>', self.on_change)
        self.batch_yield_entry.grid(row=2, column=1, pady=5, sticky="ne")

        tk.Label(form_frame, text="Unit", width=12, anchor='w').grid(row=2, column=2, sticky='nw', pady=5)
        self.unit_entry = Placeholder_Entry(form_frame, placeholder="Unit", width=17)
        self.unit_entry.bind('<KeyPress>', self.on_change)
        self.unit_entry.grid(row=2, column=3, pady=5, sticky="ne")

        if product_id==-1:
            tk.Label(form_frame, text="Version", width=12, anchor='w').grid(row=3, column=1, sticky='nw', pady=5)
            tk.Label(form_frame, textvariable=self.new_version_var, background='white', width=14, anchor='w').grid(row=3, column=2, pady=5, sticky="ne")
        else:
            tk.Label(form_frame, text="Change Type", width=12, anchor='w').grid(row=3, column=0, sticky='nw', columnspan=2)
            change_type_frame = tk.Frame(form_frame)
            change_type_frame.grid(row=3, column=1, columnspan=3)
            self.radio1 = ttk.Radiobutton(change_type_frame, text="Major", value="0", variable=self.change_type_var)
            self.radio1.grid(column=0, row=0)
            self.radio2 = ttk.Radiobutton(change_type_frame, text="Minor", value="1", variable=self.change_type_var)
            self.radio2.grid(column=1, row=0)
            self.radio3 = ttk.Radiobutton(change_type_frame, text="Patch", value="2", variable=self.change_type_var)
            self.radio3.grid(column=2, row=0)
            self.change_type_var.set("2")
            self.change_type_var.trace_add('write', self.update_new_version)

            tk.Label(form_frame, text="Version", width=12, anchor='w').grid(row=4, column=0, sticky='nw', pady=5)
            tk.Label(form_frame, textvariable=self.version_var, background='white', width=14, anchor='w').grid(row=4, column=1, pady=5, sticky="ne")

            tk.Label(form_frame, text="Next Version", width=12, anchor='w').grid(row=4, column=2, sticky='nw', pady=5)
            tk.Label(form_frame, textvariable=self.new_version_var, background='white', width=14, anchor='w').grid(row=4, column=3, pady=5, sticky="ne")


        tree_frame = tk.Frame(self.content_frame)
        tree_frame.grid(row=1, column=0, sticky='n', padx=10)

        self.selected_row = None
        tree_ingredients_width = screen_width * 0.3
        tk.Label(tree_frame, text="Ingredients").pack(pady=5)
        self.tree_ingredients = ttk.Treeview(tree_frame, columns=INGREDIENTS_COLUMNS.keys(), show="headings", height=8)
        self.tree_ingredients.pack()
        for (col, prop), tree_col in zip(INGREDIENTS_COLUMNS.items(), self.tree_ingredients["columns"]):
            self.tree_ingredients.heading(tree_col, text=col.replace("_", " ").title())
            self.tree_ingredients.column(tree_col, width=int(tree_ingredients_width*prop), anchor="w")

        self.tree_ingredients_menu = tk.Menu(tree_frame, tearoff=0)
        self.tree_ingredients_menu.add_command(label="Remove", command=self.remove_ingredient)
        self.tree_ingredients.bind("<Button-3>", self.on_right_click)
        self.tree_ingredients.bind("<Double-1>", self.on_double_click)

        self.button_ingredients = ttk.Button(tree_frame, text="Add an ingredient", command=self.add_ingredient)
        self.button_ingredients.pack(pady=5)

        recipe_frame = tk.Frame(self.content_frame)
        recipe_frame.grid(row=2, column=0, sticky='n', padx=10)
        tk.Label(recipe_frame, text="Recipe").pack(pady=(5,0))
        recipe_text_frame = tk.Frame(recipe_frame)
        recipe_text_frame.pack(pady=(0,5))
        self.recipe_text = tk.Text(recipe_text_frame, height=8)
        text_font = tkfont.nametofont(self.recipe_text.cget('font'))
        recipe_scrollbar = tk.Scrollbar(recipe_text_frame, command=self.recipe_text.yview)
        self.recipe_text.configure(yscrollcommand=recipe_scrollbar.set)
        self.recipe_text.pack(side='left')
        recipe_scrollbar.pack(side='right', fill='y')
        self.recipe_text.configure(width=int((tree_ingredients_width-float(recipe_scrollbar.cget('width')))/text_font.measure("m")))

        buttons_frame = tk.Frame(recipe_frame)
        buttons_frame.pack(pady=5)
        self.button_save = ttk.Button(buttons_frame, text="Save changes" if product_id!=-1 else "Add product", command=self.update_product)
        self.button_save.grid(row=0, column=0, padx=5)
        if self.product_id!=-1:
            self.button_restore  = ttk.Button(buttons_frame, text="Restore a previous version", command=self.load_history)
            self.button_restore.grid(row=0, column=1, padx=5)
        tk.Label(recipe_frame, textvariable=self.error_var, fg='red').pack(pady=5)

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
            self.launching_date_var.set(date_to_str(data['launching_date']))
            self.batch_yield_entry.set(data['batch_yield'])
            self.unit_entry.set(data['unit'])
            self.price_entry.set(data['price'])
            self.version_var.set(data['version'])
            self.recipe_text.insert("1.0", data['recipe'])
            for i, item in enumerate(data['ingredients']):
                self.tree_ingredients.insert("", "end", values=[item[col] for col in INGREDIENTS_COLUMNS], tags = ('Blue' if i%2==0 else 'White'))
            self.update_new_version()
            self.launching_date_var.trace_add('write', self.on_change)

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
            'launching_date': str_to_date(self.launching_date_var.get()),
            'ingredients': self.get_ingredients(),
            'recipe': self.recipe_text.get("1.0", "end").strip(),
            'batch_yield': float(self.batch_yield_entry.get()),
            'unit': self.unit_entry.get(),
            'price': float(self.price_entry.get()),
            'version': self.new_version_var.get()
        }
        self.products_collection.update_one({"product_id": self.product_id}, {"$set": values}, upsert=True)
        self.error_var.set("")

    def remove_ingredient(self):
        self.tree_ingredients.delete(self.selected_row)
        self.on_change()

    def close(self):
        self.parent.notebook.forget(self.parent.product_page)
        self.product_page = None
        self.parent.notebook.select(self.parent.products_page)
        self.parent.products_page.refresh_products()

    def update_new_version(self, *args):
        version_array = self.version_var.get().split(".")
        index = int(self.change_type_var.get())
        version_array[index] = str(int(version_array[index]) + 1)
        self.new_version_var.set(".".join(version_array))
        
    def get_ingredients(self):
        return [{column:float(value) if column=='quantity' else value for value, column in zip(self.tree_ingredients.item(row)["values"], INGREDIENTS_COLUMNS)} for row in self.tree_ingredients.get_children()]

    def add_ingredient(self):
        self.tree_ingredients.insert("", "end", values=["name", "0", "unit"])
        self.on_change()

    def on_double_click(self, event):
        row = self.tree_ingredients.identify_row(event.y)
        column = self.tree_ingredients.identify_column(event.x)
        try:
            x, y, width, _ = self.tree_ingredients.bbox(row, column) # crash when not double clicking on cell
        except: 
            pass
        else:
            cell_text = self.tree_ingredients.item(row, 'text') or self.tree_ingredients.set(row, column)
            self.entryPopup = TreeEntryPopup(self.tree_ingredients, row, column, cell_text, exit_fct=self.on_cell_change)
            if int(column[1])==2: # column = #1, #2, ...
                self.entryPopup.configure(validatecommand=(self.register(validate_float), '%P'), validate="key")
            self.entryPopup.place(x=x, y=y, anchor='w', width=width)
            self.tree_ingredients.bind("<Button-1>", lambda event: self.entryPopup.destroy())

    def on_right_click(self, event):
        self.selected_row = self.tree_ingredients.identify_row(event.y)
        if self.selected_row:
            self.tree_ingredients.selection_set(self.selected_row)
            try:
                self.tree_ingredients_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.tree_ingredients_menu.grab_release()

    def on_cell_change(self, column, new_val, previous_val):
        if new_val!=previous_val:
            self.on_change()
        return True

    def on_change(self, *args):
        self.error_var.set("Warning, you have unsaved changes !")

    def toggle_readonly(self, readonly:bool):
        if readonly:
            self.name_entry.config(state='readonly')
            self.category_entry.config(state='readonly')
            self.price_entry.config(state='readonly')
            self.unit_entry.config(state='readonly')
            self.batch_yield_entry.config(state='readonly')
            self.radio1.config(state='disabled')
            self.radio2.config(state='disabled')
            self.radio3.config(state='disabled')
            self.date_label.unbind("<Button-1>")
            self.button_ingredients.config(state="disabled")
            self.button_restore.config(state="disabled")
            self.button_save.config(state="disabled")
        else:
            self.name_entry.config(state='normal')
            self.category_entry.config(state='normal')
            self.price_entry.config(state='normal')
            self.unit_entry.config(state='normal')
            self.batch_yield_entry.config(state='normal')
            self.radio1.config(state='normal')
            self.radio2.config(state='normal')
            self.radio3.config(state='normal')
            self.date_label.bind("<Button-1>", lambda event: date_popup(self.launching_date_var, event))
            self.button_ingredients.config(state="normal")
            self.button_restore.config(state="normal")
            self.button_save.config(state="normal")

    #############
    ## History ##
    #############

    def load_history(self):
        assert(isinstance(self.product_id, int)), "product_id should be an integer"
        req = self.history_collection.find({"fk_product_id": self.product_id}).to_list()
        if len(req)==0:
            showerror("Versions not found", "There is no previous version to restore")
            return None
        self.toggle_readonly(True)
        self.history = {item['version']:item for item in req}
        self.version_choice = tk.StringVar(self, "Version")
        form_frame = tk.Frame(self.content_frame)
        form_frame.grid(row=0, column=1, sticky='n', padx=10)
        self.combobox = ttk.Combobox(form_frame, textvariable=self.version_choice, values=list(self.history.keys()))
        self.combobox.bind('<<ComboboxSelected>>', self.load_version)
        self.combobox.config(state='readonly')
        self.combobox.grid(row=0, column=0, columnspan=4)

        self.name_var2 = tk.StringVar(self, "")
        self.category_var2 = tk.StringVar(self, "")
        self.launching_date_var2 = tk.StringVar(self, "")
        self.batch_yield_var2 = tk.StringVar(self, "")
        self.unit_var2 = tk.StringVar(self, "")
        self.price_var2 = tk.StringVar(self, "")
        self.error_var2 = tk.StringVar(self, "")
    
        screen_width = self.parent.notebook.winfo_screenwidth()
        
        tk.Label(form_frame, text="Name", width=12, anchor='w').grid(row=1, column=0, sticky='nw', pady=5)
        tk.Label(form_frame, textvariable=self.name_var2, width=14, bg='white').grid(row=1, column=1, pady=5, sticky='ne')

        tk.Label(form_frame, text="Category", width=12, anchor='w').grid(row=1, column=2, sticky='nw', pady=5)
        tk.Label(form_frame, textvariable=self.category_var2, width=14, bg='white').grid(row=1, column=3, pady=5, sticky='ne')
        
        tk.Label(form_frame, text="Launching Date", width=12, anchor='w').grid(row=2, column=0, sticky='nw', pady=5)
        tk.Label(form_frame, textvariable=self.launching_date_var2, width=14, bg='white').grid(row=2, column=1, pady=5, sticky='ne')

        tk.Label(form_frame, text="Price", width=12, anchor='w').grid(row=2, column=2, sticky='nw', pady=5)
        tk.Label(form_frame, textvariable=self.price_var2, width=14, bg='white').grid(row=2, column=3, pady=5, sticky='ne')

        tk.Label(form_frame, text="Batch Yield", width=12, anchor='w').grid(row=3, column=0, sticky='nw', pady=5)
        tk.Label(form_frame, textvariable=self.batch_yield_var2, width=14, bg='white').grid(row=3, column=1, pady=5, sticky='ne')

        tk.Label(form_frame, text="Unit", width=12, anchor='w').grid(row=3, column=2, sticky='nw', pady=5)
        tk.Label(form_frame, textvariable=self.unit_var2, width=14, bg='white').grid(row=3, column=3, pady=5, sticky='ne')

        tree_frame = tk.Frame(self.content_frame)
        tree_frame.grid(row=1, column=1, sticky='n', padx=10)

        self.selected_row = None
        tree_ingredients_width = screen_width * 0.3
        tk.Label(tree_frame, text="Ingredients").pack(pady=5)
        self.tree_ingredients2 = ttk.Treeview(tree_frame, columns=INGREDIENTS_COLUMNS.keys(), show="headings", height=8)
        self.tree_ingredients2.pack()
        for (col, prop), tree_col in zip(INGREDIENTS_COLUMNS.items(), self.tree_ingredients2["columns"]):
            self.tree_ingredients2.heading(tree_col, text=col.replace("_", " ").title())
            self.tree_ingredients2.column(tree_col, width=int(tree_ingredients_width*prop), anchor="w")

        recipe_frame = tk.Frame(self.content_frame)
        recipe_frame.grid(row=2, column=1, sticky='n', padx=10)
        tk.Label(recipe_frame, text="Recipe").pack(pady=(5,0))
        recipe_text_frame = tk.Frame(recipe_frame)
        recipe_text_frame.pack()
        self.recipe_text2 = tk.Text(recipe_text_frame, height=8)
        text_font = tkfont.nametofont(self.recipe_text2.cget('font'))
        recipe_scrollbar = tk.Scrollbar(recipe_text_frame, command=self.recipe_text2.yview)
        self.recipe_text2.configure(yscrollcommand=recipe_scrollbar.set)
        self.recipe_text2.pack(side='left')
        recipe_scrollbar.pack(side='right', fill='y')
        self.recipe_text2.configure(width=int((tree_ingredients_width-float(recipe_scrollbar.cget('width')))/text_font.measure("m")))
        
        buttons_frame = tk.Frame(recipe_frame)
        buttons_frame.pack(pady=(10,5))
        ttk.Button(buttons_frame, text="Restore this version", command=self.restore_version).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=self.clear_right_grid).grid(row=0, column=1, padx=5)

        tk.Label(recipe_frame, textvariable=self.error_var2, fg='red').pack()

    def clear_right_grid(self):
        for label in self.content_frame.grid_slaves():
            if int(label.grid_info()["column"]) > 0:
                label.grid_forget()
        self.toggle_readonly(False)

    def load_version(self, *args):
        product = self.history[self.version_choice.get()]
        
        self.name_var2.set(product['name'])
        self.category_var2.set(product['category'])
        self.batch_yield_var2.set(product['batch_yield'])
        self.unit_var2.set(product['unit'])
        self.price_var2.set(product['price'])
        self.recipe_text2.delete("1.0", "end")
        self.recipe_text2.insert("1.0", product['recipe'])
        self.launching_date_var2.set(date_to_str(product['launching_date']))
        for row in self.tree_ingredients2.get_children():
            self.tree_ingredients2.delete(row)
        for i, item in enumerate(product['ingredients']):
                self.tree_ingredients2.insert("", "end", values=[item[col] for col in INGREDIENTS_COLUMNS], tags = ('Blue' if i%2==0 else 'White'))
        
    def restore_version(self):
        if self.version_choice.get()=="Version":
            self.error_var2.set("Please select a version")
            return None
        proceed = askyesno("Restore ?", "Restore this version ?", icon="warning")
        if not proceed:
            return None
        req = self.history_collection.find({"fk_product_id": self.product_id}, {'_id':0}).to_list()
        history = {item['version']:item for item in req}

        # get the version string of the current product
        req = self.products_collection.find_one({"product_id": self.product_id}, {'version'})
        if not req:
            return None
        current_version = req['version']

        # copy the current version in the history collection
        self.products_collection.aggregate([{"$match": {"product_id": self.product_id}},{"$set":{"fk_product_id": "$product_id"}},{"$project": {"product_id": 0}}, {"$merge": {"into": "productsHistory"}}]) 

        values = history[self.version_choice.get()]
        values.pop('fk_product_id')
        values['version'] = self.increase_version(current_version) # increase the version (current version + MAJOR change)
        # replace the current product with the version-to-be-restored's values
        self.products_collection.update_one({'product_id': self.product_id}, {"$set": values})
        # delete restored version in history
        self.history_collection.delete_one({"fk_product_id": self.product_id,"version": self.version_choice.get()})
        self.close()
    
    def increase_version(self, version:str):
        return str(int(version[0])+1) + version[1:]

if __name__ == '__main__':
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["db_plm"]
    app = TestApp(database, 20000)

    app.product_page = SingleProductPage(app, app.database, product_id=4)
    
    app.notebook.add(app.product_page, text="Product")
    app.notebook.select(app.product_page)
    app.mainloop()