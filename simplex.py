from fractions import Fraction

def simplex(c, A, b):
    # Inicialización
    m = len(A)    # Número de restricciones
    n = len(A[0]) # Número de variables
    
    # Convertir todos los números a fracciones
    c = [Fraction(num) for num in c]
    A = [[Fraction(num) for num in row] for row in A]
    b = [Fraction(num) for num in b]
    
    # Construir la tabla inicial
    table = [[Fraction(0)] * (n + m + 1) for _ in range(m + 1)]
    
    # Llenar la tabla con los datos iniciales
    for i in range(m):
        for j in range(n):
            table[i][j] = A[i][j]
        table[i][n + i] = Fraction(1)
        table[i][-1] = b[i]
    
    for j in range(n):
        table[-1][j] = -c[j]
    
    # Etiquetas de las variables básicas y no básicas
    basic_vars = ['S' + str(i + 1) for i in range(m)]
    non_basic_vars = ['X' + str(i + 1) for i in range(n)]
    all_vars = non_basic_vars + basic_vars
    
    # Función para imprimir la tabla
    def print_table():
        print("Tabla Simplex:")
        header = all_vars + ['Z']
        print(" | ".join(header))
        for row in table:
            print(" | ".join(str(val) for val in row))
        print()
    
    # Bucle principal del método simplex
    iteration = 0
    while True:
        print(f"Iteración {iteration}:")
        print_table()
        
        # Encontrar la columna pivote (columna de entrada)
        pivot_col = min(range(n + m), key=lambda j: table[-1][j])
        if table[-1][pivot_col] >= 0:
            break  # La solución es óptima

        # Encontrar la fila pivote (fila de salida)
        ratios = []
        for i in range(m):
            if table[i][pivot_col] > 0:
                ratios.append((table[i][-1] / table[i][pivot_col], i))
        
        if not ratios:
            raise Exception("El problema no tiene solución acotada")
        
        pivot_row = min(ratios)[1]
        
        entering_var = all_vars[pivot_col]
        leaving_var = basic_vars[pivot_row]
        
        print(f"Variable que entra: {entering_var}")
        print(f"Variable que sale: {leaving_var}\n")
        
        # Realizar la operación de pivote
        pivot_value = table[pivot_row][pivot_col]
        table[pivot_row] = [x / pivot_value for x in table[pivot_row]]
        
        for i in range(m + 1):
            if i != pivot_row:
                row_factor = table[i][pivot_col]
                table[i] = [table[i][j] - row_factor * table[pivot_row][j] for j in range(n + m + 1)]
        
        # Actualizar las variables básicas
        basic_vars[pivot_row] = entering_var
        
        iteration += 1

    
    # Extraer la solución y las variables de holgura
    solution = {var: Fraction(0) for var in non_basic_vars + basic_vars}
    for i in range(m):
        solution[basic_vars[i]] = table[i][-1]
    
    optimal_value = table[-1][-1]
    print("Solución óptima:")
    # Imprimir variables de decisión
    for var in non_basic_vars:
        print(f"{var} = {solution[var]}")
    # Imprimir variables de holgura
    for var in basic_vars:
        if var.startswith('S'):
            print(f"{var} (holgura) = {solution[var]}")
    print(f"Valor óptimo (Z) = {optimal_value}")

#main
if '__main__' == __name__:
    # Ejemplo de uso
    c = [20, 30, 25]    #Funcion Objetivo
    A = [[1, 1, 3], [1, 2, 1], [1, 1,1]]    #Restricciones
    b = [600, 500, 300] #Disponibilidad de recursos

    simplex(c, A, b)
