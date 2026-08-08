"""Mi versión de la multiplicación de matrices, hecha a mano (sin numpy)."""


def mimatmul(A, B):
    """Multiplica dos matrices A y B usando la definición clásica.

    Para obtener el resultado sigo la regla de la clase: el elemento
    (i, j) del resultado es la suma de los productos de la fila i de
    A con la columna j de B.
    """
    if not A or not B:
        raise ValueError("Las matrices no pueden estar vacías.")

    filas_a = len(A)
    columnas_a = len(A[0])
    filas_b = len(B)
    columnas_b = len(B[0])

    # Reviso que las matrices sean "rectas": todas las filas con el mismo largo.
    if any(len(fila) != columnas_a for fila in A):
        raise ValueError("La matriz A no es rectangular: todas sus filas deben medir lo mismo.")
    if any(len(fila) != columnas_b for fila in B):
        raise ValueError("La matriz B no es rectangular: todas sus filas deben medir lo mismo.")

    # Condición para poder multiplicar: el ancho de A debe ser el alto de B.
    if columnas_a != filas_b:
        raise ValueError(
            "No se pueden multiplicar: el ancho de A debe ser igual al alto de B."
        )

    resultado = []
    for i in range(filas_a):
        fila_resultado = []
        for j in range(columnas_b):
            suma = 0.0
            for k in range(columnas_a):
                suma += A[i][k] * B[k][j]
            fila_resultado.append(suma)
        resultado.append(fila_resultado)
    return resultado
