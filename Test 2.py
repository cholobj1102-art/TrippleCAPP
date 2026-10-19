import tkinter as tk
from tkinter import ttk, msagebox

materials = []
next_id = 1


class TripleCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Construction Cost Calculator")
        self.root.geometry("1050x650")
        self.root.minsize(900, 580)

        # Theme state: False = Light Mode, True = Dark Mode
        self.is_dark_mode = False
        self.load_theme_colors()

        self.materials = []
        self.next_id = 1

        self.setup_styles()
        self.build_ui()
        self.update_summary()

    def load_theme_colors(self):
        if self.is_dark_mode:
            # Dark Mode Palette
            self.bg_root = "#1e1e1e"
            self.bg_main = "#121212"
            self.bg_panel = "#1e1e1e"
            self.fg_text = "#e0e0e0"
            self.fg_muted = "#a0a0a0"
            self.header_bg = "#2d2d2d"
            self.header_fg = "#ffffff"
            self.header_sub_fg = "#b0b0b0"
            self.border_color = "#333333"
            self.amount_box_bg = "#1b3324"
            self.amount_box_fg = "#4ade80"
            self.note_bg = "#1e293b"
            self.note_fg = "#93c5fd"
            self.note_title_fg = "#bfdbfe"
            self.tree_bg = "#1e1e1e"
            self.tree_fg = "#e0e0e0"
            self.tree_heading_bg = "#2d2d2d"
            self.tree_heading_fg = "#ffffff"
            self.tree_selected = "#2563eb"
            self.btn_primary_bg = "#2563eb"
            self.btn_primary_fg = "#ffffff"
            self.toggle_text = "☀ Light Mode"
        else:
            # Light Mode Palette (Original Clean Look)
            self.bg_root = "#edf3f8"
            self.bg_main = "#edf3f8"
            self.bg_panel = "white"
            self.fg_text = "#213e5b"
            self.fg_muted = "#5a6d7e"
            self.header_bg = "#d9eafa"
            self.header_fg = "#173b62"
            self.header_sub_fg = "#365570"
            self.border_color = "#d5e1ed"
            self.amount_box_bg = "#d8f3e7"
            self.amount_box_fg = "#173d32"
            self.note_bg = "#e2efff"
            self.note_fg = "#355775"
            self.note_title_fg = "#285a8c"
            self.tree_bg = "white"
            self.tree_fg = "#243447"
            self.tree_heading_bg = "#dce9f6"
            self.tree_heading_fg = "#183b61"
            self.tree_selected = "#c8e0ff"
            self.btn_primary_bg = "#347fdf"
            self.btn_primary_fg = "white"
            self.toggle_text = "🌙 Dark Mode"

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview",
                        background=self.tree_bg,
                        fieldbackground=self.tree_bg,
                        foreground=self.tree_fg,
                        rowheight=29,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                        background=self.tree_heading_bg,
                        foreground=self.tree_heading_fg,
                        font=("Segoe UI", 9, "bold"),
                        padding=7)
        style.map("Treeview", background=[("selected", self.tree_selected)])
        style.configure("TEntry", padding=6)
        style.configure("TCombobox", padding=5)

    def build_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg=self.bg_root)

        self.header = tk.Frame(self.root, bg=self.header_bg, padx=22, pady=15)
        self.header.pack(fill="x")

        title_box = tk.Frame(self.header, bg=self.header_bg)
        title_box.pack(side="left", fill="x", expand=True)

        tk.Label(title_box, text="Construction Cost Calculator",
                 font=("Segoe UI", 20, "bold"), bg=self.header_bg,
                 fg=self.header_fg).pack(anchor="w")
        tk.Label(title_box, text="Estimate your construction material costs easily!",
                 font=("Segoe UI", 9), bg=self.header_bg,
                 fg=self.header_sub_fg).pack(anchor="w", pady=(3, 0))

        tk.Button(self.header, text=self.toggle_text, command=self.toggle_dark_mode,
                  bg=self.btn_primary_bg, fg=self.btn_primary_fg, relief="flat",
                  font=("Segoe UI", 9, "bold"), cursor="hand2",
                  padx=10, pady=6).pack(side="right", anchor="center")

        self.main = tk.Frame(self.root, bg=self.bg_main, padx=16, pady=14)
        self.main.pack(fill="both", expand=True)

        left = tk.Frame(self.main, bg=self.bg_main)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = tk.Frame(self.main, bg=self.bg_main, width=300)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self.build_input_panel(left)
        self.build_material_table(left)
        self.build_summary_panel(right)
        self.build_notes(right)

        self.status_var = tk.StringVar(value="Ready. Enter material details to begin.")
        tk.Label(self.root, textvariable=self.status_var, anchor="w",
                 bg=self.bg_root, fg=self.fg_muted, font=("Segoe UI", 9),
                 padx=18, pady=6).pack(fill="x")

        self.name_entry.focus_set()
        self.root.bind("<Return>", lambda event: self.add_material())

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.load_theme_colors()
        self.setup_styles()
        self.build_ui()
        for item in self.materials:
            self.table.insert("", "end", iid=item["id"], values=(
                self.table.get_children().__len__(), item["name"], self.number(item["quantity"]), item["unit"],
                self.money(item["price"]), self.money(item["cost"])))
        self.update_summary()

    def build_input_panel(self, parent):
        panel = tk.Frame(parent, bg=self.bg_panel, highlightbackground=self.border_color,
                         highlightthickness=1, padx=12, pady=10)
        panel.pack(fill="x", pady=(0, 10))
        tk.Label(panel, text="Add Material", font=("Segoe UI", 11, "bold"),
                 bg=self.bg_panel, fg=self.fg_text).pack(anchor="w", pady=(0, 10))

        fields = tk.Frame(panel, bg=self.bg_panel)
        fields.pack(fill="x")
        for col in range(4):
            fields.columnconfigure(col, weight=1)

        labels = ["Material Name:", "Quantity:", "Unit Price (₱):", "Unit:"]
        for col, label in enumerate(labels):
            tk.Label(fields, text=label, bg=self.bg_panel, fg=self.fg_text,
                     font=("Segoe UI", 8, "bold")).grid(
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
                  bg=self.btn_primary_bg, fg=self.btn_primary_fg, relief="flat",
                  font=("Segoe UI", 10, "bold"), cursor="hand2",
                  pady=7).pack(fill="x", pady=(10, 0))

    def build_material_table(self, parent):
        panel = tk.Frame(parent, bg=self.bg_panel, highlightbackground=self.border_color,
                         highlightthickness=1, padx=10, pady=10)
        panel.pack(fill="both", expand=True)
        tk.Label(panel, text="Material List", font=("Segoe UI", 11, "bold"),
                 bg=self.bg_panel, fg=self.fg_text).pack(anchor="w", pady=(0, 8))

        table_area = tk.Frame(panel, bg=self.bg_panel)
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
        self.table.column
