"""Pruebas iniciales para src/mimatmul.py."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from mimatmul import mimatmul  # noqa: E402


class TestMimatmul(unittest.TestCase):
    def test_matriz_identidad(self):
        A = [[1.0, 0.0], [0.0, 1.0]]
        B = [[2.0, 3.0], [4.0, 5.0]]
        self.assertEqual(mimatmul(A, B), [[2.0, 3.0], [4.0, 5.0]])

    def test_multiplicacion_2x2(self):
        A = [[1.0, 2.0], [3.0, 4.0]]
        B = [[5.0, 6.0], [7.0, 8.0]]
        self.assertEqual(mimatmul(A, B), [[19.0, 22.0], [43.0, 50.0]])

    def test_matrices_rectangulares(self):
        A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        B = [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]]
        self.assertEqual(mimatmul(A, B), [[58.0, 64.0], [139.0, 154.0]])

    def test_dimensiones_incompatibles(self):
        A = [[1.0, 2.0]]
        B = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
        with self.assertRaises(ValueError):
            mimatmul(A, B)


if __name__ == "__main__":
    unittest.main()
