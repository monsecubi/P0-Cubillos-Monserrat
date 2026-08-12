"""Benchmark: compara mimatmul (Python puro) contra NumPy (A @ B).

Mide el tiempo de cada repetición, guarda todas las mediciones en
data/benchmark_results.csv y genera figures/benchmark.png.
"""

import csv
import os
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import mimatmul

# Tamaños seguros para este computador (8 GB de RAM, Ryzen 5 5600U).
TAMANOS = [32, 64, 128, 256, 384]
REPETICIONES = 5

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
CSV_PATH = os.path.join(DATA_DIR, "benchmark_results.csv")
PNG_PATH = os.path.join(FIGURES_DIR, "benchmark.png")


def medir(mult, A, B):
    """Mide el tiempo de una multiplicación con time.perf_counter()."""
    inicio = time.perf_counter()
    mult(A, B)
    return time.perf_counter() - inicio


def generar_matrices(n):
    """Genera dos matrices float64 de tamaño n y sus versiones como listas."""
    rng = np.random.default_rng(n)
    A = rng.random((n, n))
    B = rng.random((n, n))
    return A, B, A.tolist(), B.tolist()


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    # Calentamiento: una ejecución de cada método para evitar el primer
    # costo de importación, compilación o carga de páginas de memoria.
    n0 = TAMANOS[-1]
    A0, B0, Al0, Bl0 = generar_matrices(n0)
    medir(mimatmul.mimatmul, Al0, Bl0)
    medir(lambda a, b: a @ b, A0, B0)

    filas = []
    for n in TAMANOS:
        A, B, Al, Bl = generar_matrices(n)
        for rep in range(1, REPETICIONES + 1):
            t_mio = medir(mimatmul.mimatmul, Al, Bl)
            filas.append({"metodo": "mimatmul", "tamano": n, "repeticion": rep, "tiempo": t_mio})
            t_numpy = medir(lambda a, b: a @ b, A, B)
            filas.append({"metodo": "numpy", "tamano": n, "repeticion": rep, "tiempo": t_numpy})
        print(f"Tamanos {n}: listo")

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["metodo", "tamano", "repeticion", "tiempo"])
        writer.writeheader()
        writer.writerows(filas)
    print(f"Datos guardados en {CSV_PATH}")

    graficar(filas)
    print(f"Grafico guardado en {PNG_PATH}")


def graficar(filas):
    """Genera figures/benchmark.png a partir de las filas medidas."""
    metodos = {"mimatmul": "mimatmul (Python puro)", "numpy": "NumPy (A @ B)"}
    plt.figure(figsize=(8, 5))
    for metodo, etiqueta in metodos.items():
        puntos = [f for f in filas if f["metodo"] == metodo]
        tamanos = sorted({f["tamano"] for f in puntos})
        medianas = [
            np.median([f["tiempo"] for f in puntos if f["tamano"] == n]) for n in tamanos
        ]
        plt.plot(tamanos, medianas, marker="o", label=etiqueta)
    plt.xlabel("Tamano de la matriz (n x n)")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Benchmark: mimatmul vs NumPy")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PNG_PATH, dpi=150)


if __name__ == "__main__":
    main()
