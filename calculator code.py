import tkinter as tk
from tkinter import ttk
import math

class ModernScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator-You have never seen before")
        self.root.geometry("520x720")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(True, False)

        # Style TTK widgets for dark theme
        self.setup_styles()

        # Application State
        self.is_degree = True
        self.expression = ""
        self.latest_result = "0"
        self.touch_start_x = 0

        # Build UI Structure
        self.create_nav_bar()
        
        self.content_container = tk.Frame(self.root, bg="#1e1e2e")
        self.content_container.pack(expand=True, fill="both")

        self.create_calculator_view()
        self.create_converter_view()

        # Bind Swipe Gestures across root window
        self.root.bind("<Button-1>", self.on_touch_start, add="+")
        self.root.bind("<ButtonRelease-1>", self.on_touch_end, add="+")

        # Default to Calculator View
        self.show_view("calc")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.TCombobox", 
            fieldbackground="#313244", 
            background="#45475a", 
            foreground="#cdd6f4",
            arrowcolor="#89b4fa",
            bordercolor="#1e1e2e",
            darkcolor="#1e1e2e",
            lightcolor="#1e1e2e"
        )
        self.root.option_add('*TCombobox*Listbox.background', '#313244')
        self.root.option_add('*TCombobox*Listbox.foreground', '#cdd6f4')
        self.root.option_add('*TCombobox*Listbox.selectBackground', '#89b4fa')
        self.root.option_add('*TCombobox*Listbox.selectForeground', '#11111b')

    # ----------------- NAVIGATION & GESTURES -----------------

    def create_nav_bar(self):
        nav_frame = tk.Frame(self.root, bg="#181825", height=45)
        nav_frame.pack(fill="x", side="top")

        self.btn_nav_calc = tk.Label(
            nav_frame, text="Calculator", font=("Arial", 12, "bold"),
            fg="#89b4fa", bg="#181825", cursor="hand2", padx=20, pady=10
        )
        self.btn_nav_calc.pack(side="left")
        self.btn_nav_calc.bind("<Button-1>", lambda e: self.show_view("calc"))

        self.btn_nav_conv = tk.Label(
            nav_frame, text="Converter", font=("Arial", 12, "bold"),
            fg="#6c7086", bg="#181825", cursor="hand2", padx=20, pady=10
        )
        self.btn_nav_conv.pack(side="left")
        self.btn_nav_conv.bind("<Button-1>", lambda e: self.show_view("conv"))

    def show_view(self, view_name):
        if view_name == "calc":
            self.converter_frame.pack_forget()
            self.calculator_frame.pack(expand=True, fill="both")
            self.btn_nav_calc.config(fg="#89b4fa")
            self.btn_nav_conv.config(fg="#6c7086")
            self.current_view = "calc"
        else:
            self.calculator_frame.pack_forget()
            self.converter_frame.pack(expand=True, fill="both")
            self.btn_nav_calc.config(fg="#6c7086")
            self.btn_nav_conv.config(fg="#89b4fa")
            self.current_view = "conv"

    def on_touch_start(self, event):
        self.touch_start_x = event.x_root

    def on_touch_end(self, event):
        delta_x = event.x_root - self.touch_start_x
        # Swipe Left (mid/right to left) -> open Converter
        if delta_x < -80 and self.current_view == "calc":
            self.show_view("conv")
        # Swipe Right (left to right) -> open Calculator
        elif delta_x > 80 and self.current_view == "conv":
            self.show_view("calc")

    # ----------------- CALCULATOR VIEW -----------------

    def create_calculator_view(self):
        self.calculator_frame = tk.Frame(self.content_container, bg="#1e1e2e")
        self.create_display()
        self.create_buttons()

    def create_display(self):
        display_frame = tk.Frame(self.calculator_frame, bg="#1e1e2e", bd=10)
        display_frame.pack(expand=False, fill="both")

        self.mode_label = tk.Label(display_frame, text="DEG", font=("Arial", 10, "bold"), fg="#89b4fa", bg="#1e1e2e")
        self.mode_label.pack(anchor="w", padx=10)

        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(
            display_frame, 
            textvariable=self.display_var, 
            font=("Arial", 28, "bold"), 
            fg="#cdd6f4", 
            bg="#181825", 
            bd=0, 
            justify="right"
        )
        self.display.pack(expand=True, fill="both", padx=10, pady=5)

    def create_buttons(self):
        button_frame = tk.Frame(self.calculator_frame, bg="#1e1e2e", padx=5, pady=5)
        button_frame.pack(expand=True, fill="both")

        buttons = [
            ['DEG/RAD', 'C', '⌫', '(', ')', '/'],
            ['sin', 'cos', 'tan', 'log10', 'Ans', '*'],
            ['asin', 'acos', 'atan', 'log', 'mod', '-'],
            ['x²', 'x³', 'y⁶', '√', '∛', '+'],
            ['7', '8', '9', 'π', 'e', '='],
            ['4', '5', '6', '.', '', ''],
            ['1', '2', '3', '0', '', '']
        ]

        btn_colors = {
            "operator": {"bg": "#f38ba8", "fg": "#11111b"},
            "scientific": {"bg": "#313244", "fg": "#cdd6f4"},
            "number": {"bg": "#45475a", "fg": "#cdd6f4"},
            "special": {"bg": "#fab387", "fg": "#11111b"}
        }

        for r, row in enumerate(buttons):
            for c, text in enumerate(row):
                if text == '':
                    continue

                if text in ['+', '-', '*', '/', '=', 'mod']:
                    colors = btn_colors["operator"]
                elif text in ['C', '⌫', 'DEG/RAD', 'Ans']:
                    colors = btn_colors["special"]
                elif text.isdigit() or text == '.':
                    colors = btn_colors["number"]
                else:
                    colors = btn_colors["scientific"]

                colspan = 2 if text == '0' else 1
                if text == '.' and r == 5: 
                    continue 

                btn = tk.Button(
                    button_frame, 
                    text=text, 
                    font=("Arial", 11, "bold"),
                    bg=colors["bg"], 
                    fg=colors["fg"],
                    activebackground=colors["fg"],
                    activeforeground=colors["bg"],
                    bd=0, 
                    cursor="hand2",
                    command=lambda t=text: self.on_button_click(t)
                )
                
                grid_c = c
                if text == '.': grid_c = 3
                if text == '=': 
                    btn.grid(row=r, column=c, rowspan=3, sticky="nsew", padx=4, pady=4)
                    continue

                btn.grid(row=r, column=grid_c, columnspan=colspan, sticky="nsew", padx=4, pady=4)

        for i in range(7):
            button_frame.rowconfigure(i, weight=1)
        for i in range(6):
            button_frame.columnconfigure(i, weight=1)

    def on_button_click(self, char):
        current_text = self.display_var.get()

        if current_text in ["Error", "Invalid Input"]:
            self.expression = ""
            self.display_var.set("0")

        match char:
            case "C":
                self.expression = ""
                self.display_var.set("0")
            
            case "⌫":
                if self.expression:
                    if self.expression.endswith("math.sqrt("):
                        self.expression = self.expression[:-10]
                    elif self.expression.endswith("math.log("):
                        self.expression = self.expression[:-9]
                    elif any(self.expression.endswith(f"{f}(") for f in ["sin", "cos", "tan", "asin", "acos", "atan", "log10", "ln"]):
                        self.expression = self.expression[:-4]
                    else:
                        self.expression = self.expression[:-1]
                self.display_var.set(self.expression if self.expression else "0")
            
            case "DEG/RAD":
                self.is_degree = not self.is_degree
                self.mode_label.config(text="DEG" if self.is_degree else "RAD")
            
            case "Ans":
                self.expression += self.latest_result
                self.display_var.set(self.expression)

            case "=":
                self.evaluate_expression()

            case "x²": self.append_expression("**2")
            case "x³": self.append_expression("**3")
            case "y⁶": self.append_expression("**")
            case "∛": self.append_expression("**(1/3)")
            case "π": self.append_expression("pi")
            case "e": self.append_expression("e")
            
            case "sin" | "cos" | "tan" | "asin" | "acos" | "atan" | "log10" | "ln" | "log" | "√":
                if self.expression and self.expression.replace('.','',1).isdigit():
                    val = float(self.expression)
                    if char == "sin": res = math.sin(math.radians(val)) if self.is_degree else math.sin(val)
                    elif char == "cos": res = math.cos(math.radians(val)) if self.is_degree else math.cos(val)
                    elif char == "tan": res = math.tan(math.radians(val)) if self.is_degree else math.tan(val)
                    elif char == "asin": res = math.degrees(math.asin(val)) if self.is_degree else math.asin(val)
                    elif char == "acos": res = math.degrees(math.acos(val)) if self.is_degree else math.acos(val)
                    elif char == "atan": res = math.degrees(math.atan(val)) if self.is_degree else math.atan(val)
                    elif char == "log10": res = math.log10(val)
                    elif char == "ln": res = math.log(val)
                    elif char == "log": res = math.log(val)
                    elif char == "√": res = math.sqrt(val)
                    
                    res = round(res, 8) if isinstance(res, float) else res
                    self.expression = str(res)
                    self.latest_result = str(res)
                    self.display_var.set(self.expression)
                else:
                    macro = "math.sqrt(" if char == "√" else ("math.log(" if char == "log" else f"{char}(")
                    self.append_expression(macro)
            
            case _:
                if self.display_var.get() == "0" and char not in [".", "+", "-", "*", "/", "mod"]:
                    self.expression = char
                else:
                    self.expression += str(char)
                self.display_var.set(self.expression)

    def append_expression(self, text):
        self.expression += text
        self.display_var.set(self.expression)

    def evaluate_expression(self):
        try:
            open_count = self.expression.count("(")
            close_count = self.expression.count(")")
            if open_count > close_count:
                self.expression += ")" * (open_count - close_count)

            expr = self.expression.replace('mod', '%')
            if not expr: return
            
            result = eval(expr, {"__builtins__": None}, {
                "math": math,
                "sin": lambda x: math.sin(math.radians(x)) if self.is_degree else math.sin(x),
                "cos": lambda x: math.cos(math.radians(x)) if self.is_degree else math.cos(x),
                "tan": lambda x: math.tan(math.radians(x)) if self.is_degree else math.tan(x),
                "asin": lambda x: math.degrees(math.asin(x)) if self.is_degree else math.asin(x),
                "acos": lambda x: math.degrees(math.acos(x)) if self.is_degree else math.acos(x),
                "atan": lambda x: math.degrees(math.atan(x)) if self.is_degree else math.atan(x),
                "log10": math.log10,
                "ln": math.log,
                "math.log": math.log,
                "pi": math.pi,
                "e": math.e
            })
            
            if isinstance(result, float):
                result = round(result, 8)

            self.display_var.set(str(result))
            self.latest_result = str(result)
            self.expression = str(result)
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    # ----------------- CONVERTER VIEW -----------------

    def create_converter_view(self):
        self.converter_frame = tk.Frame(self.content_container, bg="#1e1e2e", padx=25, pady=20)

        # Conversion ratios to Base Units (Meters for Distance, Sq. Meters for Land)
        self.conversion_rates = {
            "Distance": {
                "Meters (m)": 1.0,
                "Kilometers (km)": 1000.0,
                "Centimeters (cm)": 0.01,
                "Millimeters (mm)": 0.001,
                "Miles (mi)": 1609.344,
                "Yards (yd)": 0.9144,
                "Feet (ft)": 0.3048,
                "Inches (in)": 0.0254
            },
            "Land / Area": {
                "Square Meters (m²)": 1.0,
                "Square Kilometers (km²)": 1_000_000.0,
                "Square Feet (ft²)": 0.092903,
                "Square Yards (yd²)": 0.836127,
                "Acres": 4046.8564224,
                "Hectares": 10000.0,
                "Guntha": 101.17141056,
                "Bigha (Standard)": 2529.285264
            }
        }

        # Category Selector Buttons
        cat_frame = tk.Frame(self.converter_frame, bg="#1e1e2e")
        cat_frame.pack(fill="x", pady=(0, 20))

        self.selected_category = tk.StringVar(value="Distance")
        
        self.btn_dist = tk.Button(
            cat_frame, text="Distance", font=("Arial", 11, "bold"),
            bg="#89b4fa", fg="#11111b", bd=0, padx=15, pady=8, cursor="hand2",
            command=lambda: self.set_category("Distance")
        )
        self.btn_dist.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_land = tk.Button(
            cat_frame, text="Land / Area", font=("Arial", 11, "bold"),
            bg="#313244", fg="#cdd6f4", bd=0, padx=15, pady=8, cursor="hand2",
            command=lambda: self.set_category("Land / Area")
        )
        self.btn_land.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # "From" Section
        tk.Label(self.converter_frame, text="From", font=("Arial", 11, "bold"), fg="#a6adc8", bg="#1e1e2e").pack(anchor="w")
        
        self.from_unit_var = tk.StringVar()
        self.from_combo = ttk.Combobox(self.converter_frame, textvariable=self.from_unit_var, state="readonly", style="Custom.TCombobox", font=("Arial", 11))
        self.from_combo.pack(fill="x", pady=(5, 10), ipady=5)
        self.from_combo.bind("<<ComboboxSelected>>", lambda e: self.convert())

        self.conv_input_var = tk.StringVar(value="1")
        self.conv_input_var.trace_add("write", lambda *args: self.convert())
        self.input_entry = tk.Entry(
            self.converter_frame, textvariable=self.conv_input_var,
            font=("Arial", 20, "bold"), fg="#cdd6f4", bg="#181825", bd=0, justify="left"
        )
        self.input_entry.pack(fill="x", ipady=8, padx=2, pady=(0, 20))

        # "To" Section
        tk.Label(self.converter_frame, text="To", font=("Arial", 11, "bold"), fg="#a6adc8", bg="#1e1e2e").pack(anchor="w")
        
        self.to_unit_var = tk.StringVar()
        self.to_combo = ttk.Combobox(self.converter_frame, textvariable=self.to_unit_var, state="readonly", style="Custom.TCombobox", font=("Arial", 11))
        self.to_combo.pack(fill="x", pady=(5, 10), ipady=5)
        self.to_combo.bind("<<ComboboxSelected>>", lambda e: self.convert())

        self.conv_output_var = tk.StringVar(value="0")
        output_display = tk.Entry(
            self.converter_frame, textvariable=self.conv_output_var,
            font=("Arial", 20, "bold"), fg="#a6e3a1", bg="#181825", bd=0, justify="left", state="readonly"
        )
        output_display.pack(fill="x", ipady=8, padx=2, pady=(0, 20))

        # Gesture hint at the bottom
        hint_label = tk.Label(
            self.converter_frame, 
            text="Tip: Swipe right anywhere to return to the calculator.", 
            font=("Arial", 9, "italic"), 
            fg="#6c7086", 
            bg="#1e1e2e"
        )
        hint_label.pack(side="bottom", pady=10)

        # Initialize Dropdowns
        self.set_category("Distance")

    def set_category(self, category):
        self.selected_category.set(category)
        if category == "Distance":
            self.btn_dist.config(bg="#89b4fa", fg="#11111b")
            self.btn_land.config(bg="#313244", fg="#cdd6f4")
            units = list(self.conversion_rates["Distance"].keys())
            self.from_combo['values'] = units
            self.to_combo['values'] = units
            self.from_combo.set(units[0])  # Meters
            self.to_combo.set(units[1])    # Kilometers
        else:
            self.btn_dist.config(bg="#313244", fg="#cdd6f4")
            self.btn_land.config(bg="#89b4fa", fg="#11111b")
            units = list(self.conversion_rates["Land / Area"].keys())
            self.from_combo['values'] = units
            self.to_combo['values'] = units
            self.from_combo.set(units[4])  # Acres
            self.to_combo.set(units[0])    # Square Meters
        
        self.convert()

    def convert(self):
        val_str = self.conv_input_var.get().strip()
        if not val_str:
            self.conv_output_var.set("0")
            return

        try:
            val = float(val_str)
            cat = self.selected_category.get()
            u_from = self.from_unit_var.get()
            u_to = self.to_unit_var.get()

            if u_from in self.conversion_rates[cat] and u_to in self.conversion_rates[cat]:
                # Convert to base unit first, then to target unit
                base_val = val * self.conversion_rates[cat][u_from]
                result = base_val / self.conversion_rates[cat][u_to]
                
                # Format output to avoid excessive trailing decimals
                formatted = f"{result:.6g}" if abs(result) < 1e-4 or abs(result) >= 1e7 else f"{round(result, 6):g}"
                self.conv_output_var.set(formatted)
        except ValueError:
            self.conv_output_var.set("Invalid Number")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernScientificCalculator(root)
    root.mainloop()