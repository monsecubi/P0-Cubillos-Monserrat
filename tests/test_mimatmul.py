"""Pruebas de mimatmul: verifican que la multiplicación haga lo esperado."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from mimatmul import mimatmul  # noqa: E402


def test_caso_conocido():
    # Caso sencillo con resultado conocido a mano.
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[5.0, 6.0], [7.0, 8.0]]
    assert mimatmul(A, B) == [[19.0, 22.0], [43.0, 50.0]]


def test_matriz_identidad():
    # Multiplicar por la identidad no cambia nada.
    identidad = [[1.0, 0.0], [0.0, 1.0]]
    B = [[2.0, 3.0], [4.0, 5.0]]
    assert mimatmul(identidad, B) == B


def test_matriz_1x1():
    assert mimatmul([[3.0]], [[4.0]]) == [[12.0]]


def test_con_ceros_y_negativos():
    A = [[0.0, -1.0], [2.0, 3.0]]
    B = [[-5.0, 0.0], [4.0, 6.0]]
    assert mimatmul(A, B) == [[-4.0, -6.0], [2.0, 18.0]]


def test_matrices_cuadradas_con_numpy():
    rng = np.random.default_rng(0)
    A = rng.random((8, 8))
    B = rng.random((8, 8))
    resultado = mimatmul(A.tolist(), B.tolist())
    np.testing.assert_allclose(resultado, A @ B, atol=1e-12)


def test_matrices_rectangulares():
    A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    B = [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]]
    assert mimatmul(A, B) == [[58.0, 64.0], [139.0, 154.0]]


def test_matrices_rectangulares_con_numpy():
    rng = np.random.default_rng(1)
    A = rng.random((4, 7))
    B = rng.random((7, 3))
    resultado = mimatmul(A.tolist(), B.tolist())
    np.testing.assert_allclose(resultado, A @ B, atol=1e-12)


def test_dimensiones_incompatibles():
    A = [[1.0, 2.0]]
    B = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    with pytest.raises(ValueError, match="ancho de A"):
        mimatmul(A, B)


def test_matriz_no_rectangular():
    A = [[1.0, 2.0], [3.0]]
    B = [[1.0], [2.0]]
    with pytest.raises(ValueError, match="rectangular"):
        mimatmul(A, B)


def test_matriz_vacia():
    with pytest.raises(ValueError, match="vacías"):
        mimatmul([], [[1.0, 2.0]])
