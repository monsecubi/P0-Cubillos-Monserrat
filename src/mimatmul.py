"""Implementación de multiplicación de matrices (versión inicial)."""


def mimatmul(A, B):
    """Multiplica las matrices A (m x n) y B (n x p).

    Devuelve una matriz C (m x p) con C[i][j] = sum_k A[i][k] * B[k][j].
    """
    n_filas_a = len(A)
    n_cols_a = len(A[0]) if n_filas_a else 0
    n_filas_b = len(B)
    n_cols_b = len(B[0]) if n_filas_b else 0

    if n_cols_a != n_filas_b:
        raise ValueError(
            "Las dimensiones de las matrices no son compatibles para multiplicar."
        )

    C = [[0.0 for _ in range(n_cols_b)] for _ in range(n_filas_a)]
    for i in range(n_filas_a):
        for j in range(n_cols_b):
            total = 0.0
            for k in range(n_cols_a):
                total += A[i][k] * B[k][j]
            C[i][j] = total
    return C
