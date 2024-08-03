import tkinter as tk
from tkinter import ttk
from fractions import Fraction

class SimplexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método Simplex")
        self.root.geometry("1000x500")  # Tamaño inicial de la ventana
        self.root.minsize(1000, 500)  # Tamaño mínimo para evitar el redimensionamiento hacia abajo

        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para los inputs
        self.input_frame = tk.Frame(self.main_frame, padx=10, pady=10, borderwidth=2, relief="groove")
        self.input_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Frame para la tabla y la solución
        self.result_frame = tk.Frame(self.main_frame, padx=10, pady=10)
        self.result_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.num_vars_label = tk.Label(self.input_frame, text="Número de variables:")
        self.num_vars_label.grid(row=0, column=0, pady=5, sticky="e")
        self.num_vars_entry = tk.Entry(self.input_frame, width=5)
        self.num_vars_entry.grid(row=0, column=1, pady=5, padx=(0, 20), sticky="w")

        self.num_constraints_label = tk.Label(self.input_frame, text="Número de restricciones:")
        self.num_constraints_label.grid(row=1, column=0, pady=5, sticky="e")
        self.num_constraints_entry = tk.Entry(self.input_frame, width=5)
        self.num_constraints_entry.grid(row=1, column=1, pady=5, padx=(0, 20), sticky="w")

        self.next_button = tk.Button(self.input_frame, text="Siguiente", command=self.setup_input_fields)
        self.next_button.grid(row=2, column=0, columnspan=2, pady=10)

    def setup_input_fields(self):
        self.num_vars = int(self.num_vars_entry.get())
        self.num_constraints = int(self.num_constraints_entry.get())

        self.c_entries = []
        self.A_entries = []
        self.b_entries = []
        self.relation_vars = []

        for widget in self.input_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 2:
                widget.grid_forget()

        tk.Label(self.input_frame, text="Coeficientes de la función objetivo:").grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

        # Agregar etiquetas de variables para la función objetivo
        for i in range(self.num_vars):
            entry = tk.Entry(self.input_frame, width=5)
            entry.grid(row=4, column=i * 4, pady=5, padx=(0, 10), sticky="e")
            var_label = tk.Label(self.input_frame, text=f"X{i + 1}")
            var_label.grid(row=4, column=i * 4 + 1, pady=5, padx=(0, 10), sticky="w")
            self.c_entries.append(entry)

        tk.Label(self.input_frame, text="Coeficientes de las restricciones:").grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

        for i in range(self.num_constraints):
            row_entries = []
            # Etiquetas de variables para las restricciones
            for j in range(self.num_vars):
                entry = tk.Entry(self.input_frame, width=5)
                entry.grid(row=6 + i, column=j * 4, pady=5, padx=(0, 10), sticky="e")
                var_label = tk.Label(self.input_frame, text=f"X{j + 1}")
                var_label.grid(row=6 + i, column=j * 4 + 1, pady=5, padx=(0, 10), sticky="w")
                row_entries.append(entry)
            self.A_entries.append(row_entries)
            
            relation = tk.Label(self.input_frame, text="<=")
            relation.grid(row=6 + i, column=self.num_vars * 4, pady=5, padx=5, sticky="w")
            self.relation_vars.append(relation)
            
            b_entry = tk.Entry(self.input_frame, width=5)
            b_entry.grid(row=6 + i, column=self.num_vars * 4 + 1, pady=5, padx=5, sticky="e")
            self.b_entries.append(b_entry)

        self.solve_button = tk.Button(self.input_frame, text="Resolver", command=self.solve)
        self.solve_button.grid(row=7 + self.num_constraints, column=0, columnspan=self.num_vars * 4 + 2, pady=10)

        self.iteration_label = tk.Label(self.input_frame, text="")
        self.iteration_label.grid(row=8 + self.num_constraints, column=0, columnspan=self.num_vars * 4 + 2, pady=5)

        self.next_iteration_button = tk.Button(self.input_frame, text="Siguiente Iteración", command=self.next_iteration, state=tk.DISABLED)
        self.next_iteration_button.grid(row=9 + self.num_constraints, column=0, columnspan=self.num_vars * 4 + 2, pady=10)

    def solve(self):
        c = [Fraction(entry.get()) for entry in self.c_entries]
        A = [[Fraction(entry.get()) for entry in row] for row in self.A_entries]
        b = [Fraction(entry.get()) for entry in self.b_entries]

        self.simplex(c, A, b)

    def print_table(self, table, all_vars, basic_vars, entering_var=None, leaving_var=None, is_final=False):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        iteration_text = f"Iteración {self.iteration}:"
        if not is_final and entering_var and leaving_var:
            pivot_value = table[self.pivot_row][self.pivot_col]
            iteration_text += f" Variable que entra: {entering_var}, Variable que sale: {leaving_var}, Elemento pivote: {pivot_value}"
        if is_final:
            iteration_text = "Final"

        iteration_label = tk.Label(self.result_frame, text=iteration_text, font=("Helvetica", 12, "bold"))
        iteration_label.pack(pady=(0, 10))

        table_frame = tk.Frame(self.result_frame, padx=10, pady=10)
        table_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        header = [''] + all_vars + ['SOL']
        for i, text in enumerate(header):
            font_style = ("Helvetica", 10, "bold") if text in all_vars or text == 'SOL' else ("Helvetica", 10)
            label = tk.Label(table_frame, text=text, relief="solid", padx=5, pady=5, borderwidth=1, font=font_style)
            label.grid(row=0, column=i, sticky="nsew")
            if not is_final:
                if entering_var and text == entering_var:
                    label.config(bg="#90EE90")  # Verde claro
                if leaving_var and text == entering_var:
                    label.config(bg="#90EE90")

        for i, row in enumerate(table):
            basic_var_label = tk.Label(table_frame, text=basic_vars[i] if i < len(basic_vars) else '', relief="solid", padx=5, pady=5, borderwidth=1, font=("Helvetica", 10, "bold"))
            if i < len(basic_vars) and not is_final and basic_vars[i] == leaving_var:
                basic_var_label.config(bg="#FFB6C1")  # Rojo claro para la variable que sale
            basic_var_label.grid(row=i + 1, column=0, sticky="nsew")
            for j, val in enumerate(row):
                cell = tk.Label(table_frame, text=str(val), relief="solid", padx=5, pady=5, borderwidth=1)
                if i == self.pivot_row and j == self.pivot_col and not is_final:
                    cell.config(bg="#FFFF00")  # Amarillo para el elemento pivote
                cell.grid(row=i + 1, column=j + 1, sticky="nsew")

        for i in range(len(header)):
            table_frame.grid_columnconfigure(i, weight=1)

        self.root.update_idletasks()
        # El tamaño de la ventana no se ajusta automáticamente
        self.root.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}")

    def simplex(self, c, A, b):
        self.iteration = 0
        m = len(A)
        n = len(A[0])

        c = [Fraction(num) for num in c]
        A = [[Fraction(num) for num in row] for row in A]
        b = [Fraction(num) for num in b]

        table = [[Fraction(0)] * (n + m + 1) for _ in range(m + 1)]

        for i in range(m):
            for j in range(n):
                table[i][j] = A[i][j]
            table[i][n + i] = Fraction(1)
            table[i][-1] = b[i]

        for j in range(n):
            table[-1][j] = -c[j]

        basic_vars = [f"S{i + 1}" for i in range(m)]
        non_basic_vars = [f"X{j + 1}" for j in range(n)]
        all_vars = non_basic_vars + basic_vars

        self.table = table
        self.basic_vars = basic_vars
        self.non_basic_vars = non_basic_vars
        self.all_vars = all_vars
        self.iteration_active = False
        self.entering_var = None
        self.leaving_var = None
        self.next_iteration()

    def next_iteration(self):
        if self.iteration_active:
            table = self.table
            pivot_value = table[self.pivot_row][self.pivot_col]
            table[self.pivot_row] = [x / pivot_value for x in table[self.pivot_row]]

            for i in range(len(table)):
                if i != self.pivot_row:
                    row_factor = table[i][self.pivot_col]
                    table[i] = [table[i][j] - row_factor * table[self.pivot_row][j] for j in range(len(table[0]))]

            self.basic_vars[self.pivot_row] = self.entering_var

        self.iteration_active = False

        table = self.table
        basic_vars = self.basic_vars
        non_basic_vars = self.non_basic_vars
        all_vars = self.all_vars

        pivot_col = min(range(len(non_basic_vars)), key=lambda j: table[-1][j])
        if table[-1][pivot_col] >= 0:
            self.print_table(table, all_vars, basic_vars, is_final=True)
            self.show_solution(table, basic_vars, non_basic_vars)
            self.next_iteration_button.config(state=tk.DISABLED)
            return

        ratios = []
        for i in range(len(basic_vars)):
            if table[i][pivot_col] > 0:
                ratios.append((table[i][-1] / table[i][pivot_col], i))
        if not ratios:
            tk.Label(self.result_frame, text="Problema no acotado.").pack(pady=10)
            return

        pivot_row = min(ratios)[1]

        self.pivot_col = pivot_col
        self.pivot_row = pivot_row
        self.entering_var = non_basic_vars[pivot_col]
        self.leaving_var = basic_vars[pivot_row]
        self.iteration += 1
        self.iteration_active = True

        self.print_table(table, all_vars, basic_vars, self.entering_var, self.leaving_var)

        self.next_iteration_button.config(state=tk.NORMAL)

    def show_solution(self, table, basic_vars, non_basic_vars):
        solution = {var: 0 for var in non_basic_vars}
        for i in range(len(basic_vars)):
            solution[basic_vars[i]] = table[i][-1]
        optimal_value = table[-1][-1]

        solution_label = tk.Label(self.result_frame, text="Solución óptima:", font=("Helvetica", 12, "bold"))
        solution_label.pack(pady=(10, 5))
        
        solution_frame = tk.Frame(self.result_frame, padx=10, pady=10)
        solution_frame.pack(pady=(0, 10))

        for var in non_basic_vars:
            var_label = tk.Label(solution_frame, text=f"{var} = {solution[var]}", font=("Helvetica", 12))
            var_label.pack(pady=2)
        for var in basic_vars:
            if var.startswith('S'):
                var_label = tk.Label(solution_frame, text=f"{var} (holgura) = {solution[var]}", font=("Helvetica", 12))
                var_label.pack(pady=2)
        optimal_value_label = tk.Label(solution_frame, text=f"Valor óptimo (Z) = {optimal_value}", font=("Helvetica", 12))
        optimal_value_label.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimplexApp(root)
    root.mainloop()
