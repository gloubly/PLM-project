import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from utils import create_checkboxes


class ProductsPage(tk.Frame):
    def __init__(self, parent, database, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.database = database
        self.selected_row = None

        title_frame = tk.Frame(self.parent, bg="#4CAF50", relief=tk.RAISED, bd=2)
        title_frame.pack(side='top', fill='x')
        tk.Label(
            title_frame, 
            text="Products", font=("Helvetica", 20, "bold"), 
            fg="white", bg="#4CAF50", pady=4
        ).pack(pady=10)

        columns = ["name", "category", "launching_date", "conservation_date",
        "milk_type_used", "ingredients", "properties"]
        
        tree_frame = tk.Frame(self.parent)
        tree_frame.pack(pady=20)
        tree_style = ttk.Style()
        tree_style.theme_use('clam')
        tree_style.configure("Treeview.Heading", padding=5, relief='flat')
        tree_style.map('Treeview', background=[('selected', 'green')])
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        tree_scrollbar = tk.Scrollbar(tree_frame, command=self.tree.yview)
        tree_scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        for col, tree_col in zip(columns, self.tree["columns"]):
            self.tree.heading(tree_col, text=col.replace("_", " ").title())
            self.tree.column(tree_col, anchor="center")
        
        self.tree.pack(fill="both")
        #self.tree.bind("<Button-1>", self.disable_single_click)
        self.tree.unbind("<Button-1>")
        self.tree.unbind("<ButtonRelease-1>")
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.tag_configure('Blue', background="light sky blue")
        self.tree.tag_configure('White', background="white")
        self.load_data()


        buttons_frame = tk.Frame(self.parent)
        buttons_frame.pack()
        tk.Button(buttons_frame, text="Add Product", command=self.add_product).grid(column=0, row=0, pady=10, padx=10)
        tk.Button(buttons_frame, text="Modify Product", command=self.modify_product).grid(column=1, row=0, pady=10, padx=10)
        tk.Button(buttons_frame, text="Delete Product", command=self.delete_product).grid(column=2, row=0, pady=10, padx=10)
        self.stringvar = tk.StringVar(self.parent, value="")
        tk.Label(self.parent, textvariable=self.stringvar, fg="red").pack()
    
    def load_data(self):
        pass
        # with mongo
        
        # for i, item in enumerate(data):
        #     self.tree.insert("", "end", iid=item["_id"], values=(
        #     item["name"], item["category"], item["launching_date"],
        #     item["conservation_date"], item["milk_type_used"], 
        #     item["ingredients"], item["properties"]),
        #     tags = ('Blue' if i%2==0 else 'White')
        # )
    
    def on_double_click(self, event):
        self.selected_row = self.tree.focus()
        self.stringvar.set("")
        
    
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

        self.stringvar.set("")
        self.selected_row = None

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
        


    def modify_product(self):
        if self.selected_row is None:
            self.stringvar.set("Please select a row")
            return None
        values = self.tree.item(self.selected_row, 'values')
        print(values)
        self.selected_row = None


    def delete_product(self):
        if self.selected_row is None:
            self.stringvar.set("Please select a row")
            return None
        values = self.tree.item(self.selected_row, 'values')
        print(values)
        self.selected_row = None
