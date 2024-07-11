def simplex(c, A, b):
    # Inicialización
    m = len(A)    # Número de restricciones
    n = len(A[0]) # Número de variables
    
    # Construir la tabla inicial
    table = [[0] * (n + m + 1) for _ in range(m + 1)]
    
    # Llenar la tabla con los datos iniciales
    for i in range(m):
        for j in range(n):
            table[i][j] = A[i][j]
        table[i][n + i] = 1
        table[i][-1] = b[i]
    
    for j in range(n):
        table[-1][j] = -c[j]
    
    # Etiquetas de las variables básicas y no básicas
    basic_vars = ['S' + str(i + 1) for i in range(m)]
    non_basic_vars = ['x' + str(i + 1) for i in range(n)]
    all_vars = non_basic_vars + basic_vars
    
    # Función para imprimir la tabla
    def print_table():
        print("Tabla Simplex:")
        header = all_vars + ['Z']
        print(" | ".join(header))
        for row in table:
            print(" | ".join(f"{val:.2f}" for val in row))
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
                ratios.append(table[i][-1] / table[i][pivot_col])
            else:
                ratios.append(float('inf'))
        
        pivot_row = min(range(m), key=lambda i: ratios[i])
        if ratios[pivot_row] == float('inf'):
            raise Exception("El problema no tiene solución acotada")
        
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
    
    # Imprimir la tabla final
    print(f"Iteración {iteration}:")
    print_table()
    
    # Extraer la solución
    solution = [0] * n
    for i in range(m):
        if basic_vars[i] in non_basic_vars:
            idx = non_basic_vars.index(basic_vars[i])
            solution[idx] = table[i][-1]
    
    optimal_value = table[-1][-1]
    return solution, optimal_value

# Ejemplo de uso
c = [6.5, 7]   #Funcion objetivo
A = [[2, 3], [1, 1], [2, 1]]    #Restricciones
b = [600, 500, 400] #Disponibilidad de recursos

solution, optimal_value = simplex(c, A, b)
print("Solución óptima:", solution)
print("Valor óptimo (Z):", optimal_value)
