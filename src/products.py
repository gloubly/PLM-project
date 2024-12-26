import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from bson import ObjectId
from tkinter.messagebox import showerror, askokcancel
from utils import create_checkboxes, scrollable_label

PRODUCTS_COLUMNS = {
    "name": .14,
    "category": .14,
    "launching_date": .14,
    "batch_yield": .14,
    "unit": .14,
    "price": .14,
    "version": .16
}

INGREDIENTS_COLUMNS = {
    "name": 0.4,
    "quantity": 0.3,
    "unit": 0.3
}

assert(sum(PRODUCTS_COLUMNS.values())<=1)
assert(sum(INGREDIENTS_COLUMNS.values())<=1)

class ProductsPage(tk.Frame):
    def __init__(self, parent, database, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.products_collection = database['products']
        self.product_id = None

        screen_width = self.parent.winfo_screenwidth()

        title_frame = tk.Frame(self.parent, bg="#4CAF50", relief="raised", bd=2)
        # title_frame.pack(side='top', fill='x')
        title_frame.grid(row=0, column=0, sticky="n", columnspan=2, pady=(0, 30))
        tk.Label(title_frame, 
            text="Products", font=("Helvetica", 20, "bold"), 
            fg="white", bg="#4CAF50", pady=4
        ).pack(pady=10)

        #tree products
        left_frame = tk.Frame(self.parent, bg="red")
        # left_frame.pack(side="left", padx=20, pady=10)
        left_frame.grid(row=1, column=0, sticky="nw", padx=20)
        tree_frame = tk.Frame(left_frame)
        tree_frame.pack()
        tree_style = ttk.Style()
        tree_style.theme_use('clam')
        tree_style.configure("Treeview.Heading", padding=5, relief='flat')
        tree_style.map('Treeview', background=[('selected', 'green')])
        self.tree_products = ttk.Treeview(tree_frame, columns=PRODUCTS_COLUMNS.keys(), show="headings", height=20)
        products_scrollbar = tk.Scrollbar(tree_frame, command=self.tree_products.yview)
        products_scrollbar.pack(side="right", fill="y")
        self.tree_products.configure(yscrollcommand=products_scrollbar.set)
        tree_products_width = screen_width * 0.6
        for (col, prop), tree_col in zip(PRODUCTS_COLUMNS.items(), self.tree_products["columns"]):
            self.tree_products.heading(tree_col, text=col.replace("_", " ").title())
            self.tree_products.column(tree_col, width=int(tree_products_width*prop), anchor="center")
        
        self.tree_products.pack(fill="both")
        self.tree_products.unbind("<Button-1>")
        self.tree_products.unbind("<ButtonRelease-1>")
        self.tree_products.bind("<Double-1>", self.on_double_click)
        self.tree_products.tag_configure('Blue', background="light sky blue")
        self.tree_products.tag_configure('White', background="white")

        self.menu = tk.Menu(tree_frame, tearoff=0)
        self.menu.add_command(label="Remove", command=self.remove_product)
        self.menu.add_command(label="Edit", command=self.edit_product)

        self.tree_products.bind("<Button-3>", self.on_right_click)
        self.load_products()

        self.error_var = tk.StringVar(left_frame, "")
        tk.Label(left_frame, textvariable=self.error_var, fg="red").pack()

        right_frame = tk.Frame(self.parent)
        # right_frame.pack(side="right", expand=True)
        right_frame.grid(row=1, column=1, sticky="n")
        self.product_name_var = tk.StringVar(right_frame, "Product Name")
        tk.Label(right_frame, textvariable=self.product_name_var).pack(pady=5)

        #ingredients
        tree_i_frame = tk.Frame(right_frame)
        tree_i_frame.pack()
        self.tree_ingredients = ttk.Treeview(tree_i_frame, columns=INGREDIENTS_COLUMNS.keys(), show="headings", height=8)
        tree_i_scrollbar = tk.Scrollbar(tree_i_frame, command=self.tree_ingredients.yview)
        tree_i_scrollbar.pack(side="right", fill="y")
        self.tree_ingredients.configure(yscrollcommand=tree_i_scrollbar.set)
        self.tree_ingredients.pack(fill="both")


        tree_ingredients_width = screen_width * 0.3
        for (col, prop), tree_col in zip(INGREDIENTS_COLUMNS.items(), self.tree_ingredients["columns"]):
            self.tree_ingredients.heading(tree_col, text=col.replace("_", " ").title())
            self.tree_ingredients.column(tree_col, width=int(tree_ingredients_width*prop), anchor="center")

        #recipe        
        recipe_frame = tk.Frame(right_frame)
        recipe_frame.pack(pady=10)
        tk.Label(recipe_frame, text="Recipe").pack()
        self.recipe_text_var = tk.StringVar(recipe_frame, "")

        # scrollable_label(recipe_frame, stringvar=self.recipe_text_var, width=tree_ingredients_width, height=100)
        scrollable_label(recipe_frame, width=tree_ingredients_width, height=150, stringvar=self.recipe_text_var)
        # tk.Label(recipe_frame, textvariable=self.recipe_text_var, bg='white', relief='groove').pack(fill='both', expand=True)
        

        # frame = tk.Frame(root)
        # frame.pack(fill=tk.BOTH, expand=False)
        # text = tk.Text(frame, wrap=tk.WORD, height=10, width=40)
        # text.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        # scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=text.yview)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # text.config(yscrollcommand=scrollbar.set)

        # scrollable_label(right_frame, tree_ingredients_width, 100, "aa\naaa\naaa\naaa\naaa")

    
    def load_products(self):
        req = self.products_collection.find({})
        for i, item in enumerate(req):
            self.tree_products.insert("", "end", iid=item["product_id"], values=[item[col] for col in PRODUCTS_COLUMNS], tags = ('Blue' if i%2==0 else 'White'))

    def update_tree_products_tags(self):
        for i, row in enumerate(self.tree_products.get_children()):
            self.tree_products.item(row, tags = ('Blue' if i%2==0 else 'White'))

    def load_recipe_ingredients(self):
        self.clear_ingredients()
        req = self.products_collection.find_one({"product_id": self.product_id}, {"name":1, "ingredients":1, "recipe":1})
        self.product_name_var.set(req['name'])
        for i, item in enumerate(req['ingredients']):
            self.tree_ingredients.insert("", "end", values=[item[col] for col in INGREDIENTS_COLUMNS], tags = ('Blue' if i%2==0 else 'White'))
        self.recipe_text_var.set(req["recipe"])
    
    # TODO : clear ingredients/recipe is product deleted is current selected
    def clear_ingredients(self):
        for row in self.tree_ingredients.get_children():
            self.tree_ingredients.delete(row)
    
    def on_double_click(self, event):
        self.product_id = int(self.tree_products.focus())
        self.error_var.set("")
        self.load_recipe_ingredients()

    def on_right_click(self, event):
        self.product_id = self.tree_products.identify_row(event.y)
        if self.product_id:
            self.tree_products.selection_set(self.product_id)
            try:
                self.menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.menu.grab_release()
    
    def remove_product(self):
        proceed = askokcancel(title="Remove Product", message="Remove Product ?")
        if not proceed:
            self.product_id = None
            return None
        product_object_id = self.products_collection.find({"product_id": int(self.product_id)}, {"_id":1})[0]['_id']

        req = self.products_collection.delete_one({ "_id": ObjectId(product_object_id)})
        if req.deleted_count>0:
            self.tree_products.delete(self.product_id)
            self.update_tree_products_tags()
        else:
            showerror(title="Remove Product", message="Couldn't remove product")

        self.product_id = None

    def edit_product(self):
        pass
    
    def add_product(self):

        def add_product_request():
            # TODO
            name = name_entry.get()
            category = category_entry.get()
            product_properties = [prop for prop, box in zip(properties, checkboxes_properties) if box.get()]
            launching_date = launching_cal.get_date() # format américain
            conservation_date = conservation_cal.get_date()
            print(name)
            print(category)
            print(product_properties)
            print(launching_date)
            print(conservation_date)
            request = True #TODO add mongo

            if True:
                error_stringvar.set('Error Adding Product')
            else:
                error_stringvar.set('')

        self.error_var.set("")
        self.product_id = None

        # Create a new window
        new_window = tk.Toplevel(self.parent)
        new_window.title("Add a Product")
        new_window.geometry('600x700')
        new_window.resizable(False, False)

        # Main Title
        title_label = tk.Label(new_window, text="Add a Product", font=("Arial", 16, "bold"))
        title_label.pack(pady=(10, 20))

        form_frame = tk.Frame(new_window, padx=10, pady=10)
        form_frame.pack()

        # Name Entry
        tk.Label(form_frame, text="Name", anchor='w').grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=1, pady=5)

        # Category Entry
        tk.Label(form_frame, text="Category", anchor='w').grid(row=1, column=0, sticky='w', pady=5)
        category_entry = tk.Entry(form_frame, width=30)
        category_entry.grid(row=1, column=1, pady=5)

        # Milk Type Used
        tk.Label(form_frame, text="Milk Type Used", anchor='w').grid(row=4, column=0, sticky='w', pady=5)
        milk_combo = ttk.Combobox(form_frame, values=["Whole", "Low-fat", "Skimmed"])
        milk_combo.current(0)
        milk_combo.grid(row=4, column=1, pady=5)

        # Ingredients
        tk.Label(form_frame, text="Ingredients", anchor='w').grid(row=5, column=0, sticky='w', pady=5)
        tk.Label(form_frame, text="(TODO: Add a list of ingredients from BDD)").grid(row=5, column=1, sticky='w', pady=5)

        dates_frame = tk.Frame(new_window)
        dates_frame.pack()

        # Launching Date
        tk.Label(dates_frame, text="Launching Date", anchor='w').grid(row=0, column=0, sticky='w', pady=5, padx=10)
        launching_cal = Calendar(dates_frame, selectmode='day')
        launching_cal.grid(row=1, column=0, pady=5, padx=10)

        # Conservation Date
        tk.Label(dates_frame, text="Conservation Date", anchor='w').grid(row=0, column=1, sticky='w', pady=5, padx=10)
        conservation_cal = Calendar(dates_frame, selectmode='day')
        conservation_cal.grid(row=1, column=1, pady=5, padx=10)

        # Properties Section
        properties_frame = tk.Frame(new_window, relief='groove', borderwidth=2, padx=10, pady=10)
        properties_frame.pack(fill='x', padx=10, pady=(10, 20))
        tk.Label(properties_frame, text="Properties", font = ("Arial", 13)).grid(row=0)
        properties = ["Bio", "Lactose Free"]
        checkboxes_properties = create_checkboxes(properties_frame, properties)

        tk.Button(new_window, text="Submit", command=add_product_request, bg="#4CAF50", fg="white").pack(pady=10)
        error_stringvar = tk.StringVar(new_window)
        tk.Label(new_window, textvariable=error_stringvar, fg='red').pack()

if __name__ == "__main__":
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["db_plm"]
    root = tk.Tk()
    ProductsPage(root, database)
    root.state('zoomed')
    root.after(20000, lambda: root.destroy())
    root.mainloop()