import tkinter as tk
from tkinter import ttk
from bson import ObjectId
from tkinter.messagebox import showerror, askokcancel
from utils import scrollable_label, clear_frame
from single_product import Product

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
        self.database = database
        self.products_collection = database['products']
        self.product_id = None

        screen_width = parent.notebook.winfo_screenwidth()

        tk.Label(self, text='Products', font=('Cascadia Code', 20), relief='groove', anchor='center', borderwidth=2, bg='#d1d1d1').pack(fill='both', pady=5)

        content_frame = tk.Frame(self)
        content_frame.pack(fill='both', expand=True)

        #tree products
        left_frame = tk.Frame(content_frame)
        left_frame.grid(row=1, column=0, sticky="nw", padx=20)
        tree_frame = tk.Frame(left_frame)
        tree_frame.pack()
        tree_style = ttk.Style()
        tree_style.theme_use('vista')
        tree_style.configure("Treeview.Heading", padding=5, relief='flat')
        tree_style.map('Treeview', background=[('selected', 'green')])
        self.tree_products = ttk.Treeview(tree_frame, columns=PRODUCTS_COLUMNS.keys(), show="headings", height=20)
        products_scrollbar = tk.Scrollbar(tree_frame, command=self.tree_products.yview)
        products_scrollbar.pack(side="right", fill="y")
        self.tree_products.configure(yscrollcommand=products_scrollbar.set)
        tree_products_width = screen_width * 0.6
        for (col, prop), tree_col in zip(PRODUCTS_COLUMNS.items(), self.tree_products["columns"]):
            self.tree_products.heading(tree_col, text=col.replace("_", " ").title())
            self.tree_products.column(tree_col, width=int(tree_products_width*prop), anchor="w")
        
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
        ttk.Style().theme_use('vista')
        ttk.Button(left_frame, text="Add a product", command=self.add_product).pack(pady=10)
        self.error_var = tk.StringVar(left_frame, "")
        tk.Label(left_frame, textvariable=self.error_var).pack()
        
        # right part
        right_frame = tk.Frame(content_frame)
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
            self.tree_ingredients.column(tree_col, width=int(tree_ingredients_width*prop), anchor="w")

        #recipe        
        recipe_frame = tk.Frame(right_frame)
        recipe_frame.pack(pady=10)
        tk.Label(recipe_frame, text="Recipe").pack()
        self.recipe_text_var = tk.StringVar(recipe_frame, "")
        scrollable_label(recipe_frame, width=tree_ingredients_width, height=150, stringvar=self.recipe_text_var)


    
    def load_products(self):
        req = self.products_collection.find({})
        for i, item in enumerate(req):
            self.tree_products.insert("", "end", iid=item["product_id"], values=[item[col] for col in PRODUCTS_COLUMNS], tags = ('Blue' if i%2==0 else 'White'))

    def refresh_products(self):
        for row in self.tree_products.get_children():
            self.tree_products.delete(row)
        self.load_products()
        self.clear_ingredients()
        self.recipe_text_var.set("")

    def update_tree_products_tags(self):
        for i, row in enumerate(self.tree_products.get_children()):
            self.tree_products.item(row, tags = ('Blue' if i%2==0 else 'White'))

    def load_recipe_ingredients(self):
        assert(isinstance(self.product_id, int)), "product_id should be an integer"
        self.clear_ingredients()
        req = self.products_collection.find_one({"product_id": self.product_id}, {"name":1, "ingredients":1, "recipe":1})
        self.product_name_var.set(req['name'])
        for i, item in enumerate(req['ingredients']):
            self.tree_ingredients.insert("", "end", values=[item[col] for col in INGREDIENTS_COLUMNS], tags = ('Blue' if i%2==0 else 'White'))
        self.recipe_text_var.set(req["recipe"])
    
    def clear_ingredients(self):
        for row in self.tree_ingredients.get_children():
            self.tree_ingredients.delete(row)
    
    def on_double_click(self, event):
        self.product_id = int(self.tree_products.focus())
        self.error_var.set("")
        self.load_recipe_ingredients()

    def on_right_click(self, event):
        self.last_product_id = self.product_id
        self.product_id = self.tree_products.identify_row(event.y)
        if self.product_id:
            self.tree_products.selection_set(self.product_id)
            self.product_id = int(self.product_id)
            try:
                self.menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.menu.grab_release()
    
    def remove_product(self):
        name = self.tree_products.item(self.product_id)['values'][0]
        proceed = askokcancel(title="Remove Product", message=f'Remove Product "{name}"?')
        if not proceed:
            self.product_id = None
            return None
        assert(isinstance(self.product_id, int)), "product_id should be an integer"
        product_object_id = self.products_collection.find({"product_id": self.product_id}, {"_id":1})[0]['_id']
        req = self.products_collection.delete_one({ "_id": ObjectId(product_object_id)})
        if req.deleted_count>0:
            self.tree_products.delete(self.product_id)
            self.update_tree_products_tags()
            if self.product_id==self.last_product_id:
                self.clear_ingredients()
                self.recipe_text_var.set("")

        else:
            showerror(title="Remove Product", message="Couldn't remove product")

        self.product_id = None

    def edit_product(self):
        assert(isinstance(self.product_id, int)), "product_id should be an integer"
        # clear_frame(self.parent)
        # Product(self.parent, self.database, product_id=self.product_id).pack(fill='both', expand=True)
    
    def add_product(self):
        self.parent.load_product_page()

if __name__ == "__main__":
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["db_plm"]
    root = tk.Tk()
    ProductsPage(root, database).pack(fill='both', expand=True)
    root.state('zoomed')
    root.after(20000, lambda: root.destroy())
    root.mainloop()