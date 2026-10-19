import tkinter as tk
from tkinter import ttk, messagebox

materials = []
next_id = 1


class TripleCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Construction Cost Calculator")
        self.root.geometry("1050x650")
        self.root.minsize(900, 580)
        self.root.configure(bg="#edf3f8")
        self.materials = []
        self.next_id = 1
        self.setup_styles()
        self.build_ui()
        self.update_summary()

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", background="white", fieldbackground="white",
                        foreground="#243447", rowheight=29, font=("Arial", 9))
        style.configure("Treeview.Heading", background="#dce9f6",
                        foreground="#183b61", font=("Arial", 9, "bold"), padding=7)
        style.map("Treeview", background=[("selected", "#c8e0ff")])
        style.configure("TEntry", padding=6)
        style.configure("TCombobox", padding=5)

    def build_ui(self):
        header = tk.Frame(self.root, bg="#d9eafa", padx=22, pady=15)
        header.pack(fill="x")
        self.logo_image = tk.PhotoImage(
            file=r"C:\Users\chris\OneDrive\Desktop\Construction Cost Calculator\Test 1\logo.png.png"
        )
        title_box = tk.Frame(header, bg="#d9eafa")
        title_box.pack(side="left", fill="x", expand=True)
        tk.Label(title_box, text="Construction Cost Calculator",
                 font=("Arial", 22, "bold"), bg="#d9eafa",
                 fg="#173b62").pack(anchor="w")
        tk.Label(title_box, text="Estimate your construction material costs easily!",
                 font=("Arial", 10), bg="#d9eafa",
                 fg="#365570").pack(anchor="w", pady=(3, 0))

        main = tk.Frame(self.root, bg="#edf3f8", padx=16, pady=14)
        main.pack(fill="both", expand=True)
        left = tk.Frame(main, bg="#edf3f8")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right = tk.Frame(main, bg="#edf3f8", width=300)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self.build_input_panel(left)
        self.build_material_table(left)
        self.build_summary_panel(right)
        self.build_notes(right)

        self.status_var = tk.StringVar(value="Ready. Enter material details to begin.")
        tk.Label(self.root, textvariable=self.status_var, anchor="w",
                 bg="#edf3f8", fg="#5a6d7e", font=("Arial", 9),
                 padx=18, pady=6).pack(fill="x")
        self.name_entry.focus_set()
        self.root.bind("<Return>", lambda event: self.add_material())

    def build_input_panel(self, parent):
        panel = tk.Frame(parent, bg="white", highlightbackground="#d5e1ed",
                         highlightthickness=1, padx=12, pady=10)
        panel.pack(fill="x", pady=(0, 10))
        tk.Label(panel, text="Add Material", font=("Arial", 11, "bold"),
                 bg="white", fg="#213e5b").pack(anchor="w", pady=(0, 10))
        fields = tk.Frame(panel, bg="white")
        fields.pack(fill="x")
        for col in range(4):
            fields.columnconfigure(col, weight=1)

        labels = ["Material Name:", "Quantity:", "Unit Price (₱):", "Unit:"]
        for col, label in enumerate(labels):
            tk.Label(fields, text=label, bg="white", fg="#35495e",
                     font=("Arial", 8, "bold")).grid(
                         row=0, column=col, sticky="w",
                         padx=(0, 7) if col < 3 else 0, pady=(0, 5))

        self.name_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.unit_var = tk.StringVar(value="bags")

        self.name_entry = ttk.Entry(fields, textvariable=self.name_var)
        self.name_entry.grid(row=1, column=0, sticky="ew", padx=(0, 7))
        self.quantity_entry = ttk.Entry(fields, textvariable=self.quantity_var)
        self.quantity_entry.grid(row=1, column=1, sticky="ew", padx=(0, 7))
        self.price_entry = ttk.Entry(fields, textvariable=self.price_var)
        self.price_entry.grid(row=1, column=2, sticky="ew", padx=(0, 7))
        self.unit_combo = ttk.Combobox(
            fields, textvariable=self.unit_var,
            values=("bags", "kg", "pcs", "m", "m²", "m³", "cu.m", "loads", "liters"),
            state="normal")
        self.unit_combo.grid(row=1, column=3, sticky="ew")

        tk.Button(panel, text="＋  Add Material", command=self.add_material,
                  bg="#347fdf", activebackground="#286bc1", fg="white",
                  activeforeground="white", relief="flat",
                  font=("Arial", 10, "bold"), cursor="hand2",
                  pady=7).pack(fill="x", pady=(10, 0))

    def build_material_table(self, parent):
        panel = tk.Frame(parent, bg="white", highlightbackground="#d5e1ed",
                         highlightthickness=1, padx=10, pady=10)
        panel.pack(fill="both", expand=True)
        tk.Label(panel, text="Material List", font=("Arial", 11, "bold"),
                 bg="white", fg="#213e5b").pack(anchor="w", pady=(0, 8))
        table_area = tk.Frame(panel, bg="white")
        table_area.pack(fill="both", expand=True)
        columns = ("number", "name", "quantity", "unit", "price", "total")
        self.table = ttk.Treeview(table_area, columns=columns,
                                  show="headings", selectmode="extended")
        headings = {"number": "#", "name": "Material", "quantity": "Quantity",
                    "unit": "Unit", "price": "Unit Price (₱)", "total": "Total (₱)"}
        for col, heading in headings.items():
            self.table.heading(col, text=heading)
        self.table.column("number", width=35, minwidth=30, anchor="center")
        self.table.column("name", width=130, minwidth=90, anchor="w")
        self.table.column("quantity", width=75, minwidth=55, anchor="center")
        self.table.column("unit", width=60, minwidth=45, anchor="center")
        self.table.column("price", width=100, minwidth=80, anchor="e")
        self.table.column("total", width=105, minwidth=85, anchor="e")
        scrollbar = ttk.Scrollbar(table_area, orient="vertical",
                                  command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        buttons = tk.Frame(panel, bg="white")
        buttons.pack(fill="x", pady=(10, 0))
        tk.Button(buttons, text="▤  Clear All", command=self.clear_all,
                  bg="#27975b", activebackground="#207d4b", fg="white",
                  activeforeground="white", relief="flat", font=("Arial", 9, "bold"),
                  cursor="hand2", padx=14, pady=6).pack(side="left", padx=(0, 8))
        tk.Button(buttons, text="⟳  Reset", command=self.reset_inputs,
                  bg="#718096", activebackground="#5c6878", fg="white",
                  activeforeground="white", relief="flat", font=("Arial", 9, "bold"),
                  cursor="hand2", padx=14, pady=6).pack(side="left")
        tk.Button(buttons, text="Remove Selected", command=self.remove_selected,
                  bg="#d9534f", activebackground="#bd3d39", fg="white",
                  activeforeground="white", relief="flat", font=("Arial", 9, "bold"),
                  cursor="hand2", padx=10, pady=6).pack(side="right")

    def build_summary_panel(self, parent):
        panel = tk.Frame(parent, bg="white", highlightbackground="#d5e1ed",
                         highlightthickness=1, padx=14, pady=12)
        panel.pack(fill="x", pady=(0, 10))
        tk.Label(panel, text="Total Cost", font=("Arial", 12, "bold"),
                 bg="white", fg="#213e5b").pack(anchor="w")
        amount_box = tk.Frame(panel, bg="#d8f3e7", highlightbackground="#b7dfce",
                              highlightthickness=1, padx=8, pady=13)
        amount_box.pack(fill="x", pady=(9, 13))
        self.total_var = tk.StringVar(value="₱ 0.00")
        tk.Label(amount_box, textvariable=self.total_var, font=("Arial", 21, "bold"),
                 bg="#d8f3e7", fg="#173d32").pack(anchor="center")
        tk.Label(panel, text="Cost Breakdown", font=("Arial", 10, "bold"),
                 bg="white", fg="#213e5b").pack(anchor="w", pady=(0, 7))
        self.breakdown_frame = tk.Frame(panel, bg="white")
        self.breakdown_frame.pack(fill="x")
        self.build_notes(parent)

    def build_notes(self, parent):
        note = tk.Frame(parent, bg="#e2efff", highlightbackground="#c8def6",
                        highlightthickness=1, padx=10, pady=10)
        note.pack(fill="x", pady=(0, 10))
        tk.Label(note, text="ℹ  Note", font=("Arial", 10, "bold"),
                 bg="#e2efff", fg="#285a8c").pack(anchor="w")
        tk.Label(note, text="Prices and quantities are estimates.\n"
                            "Actual costs may vary depending on\n"
                            "location and supplier.",
                 justify="left", font=("Arial", 9), bg="#e2efff",
                 fg="#355775").pack(anchor="w", pady=(5, 0))
        tk.Button(parent, text="Exit", command=self.exit_app,
                  bg="#e8edf3", fg="#263b50", relief="flat",
                  cursor="hand2", font=("Arial", 9, "bold"),
                  pady=7).pack(fill="x")

    @staticmethod
    def money(value):
        return "₱ " + format(value, ",.2f")

    @staticmethod
    def number(value):
        if value.is_integer():
            return format(int(value), ",")
        return format(value, ",.3f").rstrip("0").rstrip(".")

    def add_material(self):
        name = self.name_var.get().strip()
        quantity_text = self.quantity_var.get().strip().replace(",", "")
        price_text = self.price_var.get().strip().replace(",", "").replace("₱", "")
        unit = self.unit_var.get().strip()

        if not name or not quantity_text or not price_text or not unit:
            messagebox.showerror("Missing Information",
                                 "Please enter the material name, quantity, unit price, and unit.")
            return
        try:
            quantity = float(quantity_text)
            price = float(price_text)
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Quantity and unit price must be valid numbers.")
            return
        if quantity <= 0 or price <= 0:
            messagebox.showerror("Invalid Values",
                                 "Quantity and unit price must be greater than zero.")
            return

        cost = quantity * price
        item = {"id": str(self.next_id), "name": name, "quantity": quantity,
                "unit": unit, "price": price, "cost": cost}
        self.materials.append(item)
        self.table.insert("", "end", iid=item["id"], values=(
            len(self.materials), name, self.number(quantity), unit,
            self.money(price), self.money(cost)))
        self.next_id += 1

        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.name_entry.focus_set()
        self.status_var.set("Added " + name + ".")
        self.update_summary()

    def update_summary(self):
        total = sum(item["cost"] for item in self.materials)
        self.total_var.set(self.money(total))
        for widget in self.breakdown_frame.winfo_children():
            widget.destroy()

        if not self.materials:
            tk.Label(self.breakdown_frame, text="No materials added yet.",
                     bg="white", fg="#718096", font=("Arial", 9)).pack(
                         anchor="w", pady=4)
        else:
            totals_by_name = {}
            for item in self.materials:
                totals_by_name[item["name"]] = (
                    totals_by_name.get(item["name"], 0) + item["cost"])
            for name, amount in totals_by_name.items():
                row = tk.Frame(self.breakdown_frame, bg="white")
                row.pack(fill="x", pady=3)
                tk.Label(row, text=name, bg="white", fg="#35495e",
                         font=("Arial", 9)).pack(side="left", anchor="w")
                tk.Label(row, text=self.money(amount), bg="white",
                         fg="#35495e", font=("Arial", 9)).pack(side="right", anchor="e")

            ttk.Separator(self.breakdown_frame, orient="horizontal").pack(
                fill="x", pady=7)
            total_row = tk.Frame(self.breakdown_frame, bg="white")
            total_row.pack(fill="x")
            tk.Label(total_row, text="Total", bg="white", fg="#213e5b",
                     font=("Arial", 10, "bold")).pack(side="left")
            tk.Label(total_row, text=self.money(total), bg="white", fg="#213e5b",
                     font=("Arial", 10, "bold")).pack(side="right")

        for index, item in enumerate(self.materials, start=1):
            if self.table.exists(item["id"]):
                values = list(self.table.item(item["id"], "values"))
                values[0] = index
                self.table.item(item["id"], values=values)

    def remove_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("No Selection",
                                   "Select one or more materials to remove.")
            return
        selected_ids = set(selected)
        self.materials = [item for item in self.materials
                          if item["id"] not in selected_ids]
        for item_id in selected:
            self.table.delete(item_id)
        self.status_var.set("Selected material(s) removed.")
        self.update_summary()

    def clear_all(self):
        if not self.materials:
            messagebox.showinfo("Clear All", "The material list is already empty.")
            return
        if not messagebox.askyesno("Clear All",
                                   "Are you sure you want to remove all materials?"):
            return
        self.materials.clear()
        for item_id in self.table.get_children():
            self.table.delete(item_id)
        self.update_summary()
        self.status_var.set("All materials cleared.")

    def reset_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.unit_var.set("bags")
        self.name_entry.focus_set()
        self.status_var.set("Input fields reset. Material list was not changed.")

    def exit_app(self):
        if self.materials and not messagebox.askyesno(
                "Exit", "Your material list will not be saved. Do you want to exit?"):
            return
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TripleCApp(root)
    root.mainloop()
