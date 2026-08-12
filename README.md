# P0-Cubillos-Monserrat

Proyecto 0: implementación de la multiplicación de matrices en Python puro
(`mimatmul`), comparación con NumPy mediante un benchmark y documentación de
los resultados.

## Propósito

- Implementar `mimatmul`, una multiplicación de matrices con ciclos explícitos
  de Python (sin NumPy).
- Recolectar información del computador.
- Medir el rendimiento de `mimatmul` frente a `numpy` (`A @ B`) para matrices
  de distintos tamaños.
- Generar datos (CSV), un gráfico (PNG) y un análisis de uso de CPU y RAM.

## Estructura del repositorio

```
P0-Cubillos-Monserrat/
├── README.md
├── AGENTS.md
├── requirements.txt
├── src/
│   ├── system_info.py
│   ├── mimatmul.py
│   └── benchmark.py
├── tests/
│   └── test_mimatmul.py
├── data/
│   ├── system_info.json
│   └── benchmark_results.csv
└── figures/
    └── benchmark.png
```

## 1. Ambiente reproducible

Comandos exactos (Windows):

```
git clone https://github.com/monsecubi/P0-Cubillos-Monserrat.git
cd P0-Cubillos-Monserrat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Ejecutar las pruebas:

```
pytest
```

Ejecutar el benchmark (mide tiempos, genera `data/benchmark_results.csv`
y `figures/benchmark.png`):

```
python src/benchmark.py
```

Obtener la información del computador (genera `data/system_info.json`):

```
python src/system_info.py
```

Dependencias (en `requirements.txt`):

- `numpy` (para el benchmark y la comparación en las pruebas)
- `matplotlib` (para el gráfico)
- `pytest` (para las pruebas)

## 2. Información del computador

Tabla con las características principales (detalle completo en
`data/system_info.json`):

| Característica              | Valor                                  |
| --------------------------- | -------------------------------------- |
| Sistema operativo           | Windows 11 (10.0.26200)                |
| Procesador                  | AMD Ryzen 5 5600U with Radeon Graphics |
| Núcleos físicos             | 6                                      |
| Procesadores lógicos        | 12                                     |
| RAM total                   | 7.35 GiB (7890833408 bytes)          |
| RAM libre al medir          | 0.63 GiB (674459648 bytes)           |
| GPU                         | AMD Radeon Graphics (integrada)        |
| Versión de Python           | 3.12.10                                |
| Versión de NumPy            | 2.5.2                                  |
| Versión de matplotlib       | 3.11.1                                 |

## 3. Implementación de mimatmul

`src/mimatmul.py` implementa `mimatmul(A, B)` con tres ciclos `for` anidados
siguiendo la definición clásica: el elemento `(i, j)` del resultado es la suma
de los productos de la fila `i` de A con la columna `j` de B.

- Funciona con matrices cuadradas y rectangulares.
- Comprueba que las matrices no estén vacías, que todas las filas tengan el
  mismo largo (matrices "rectas") y que el ancho de A sea igual al alto de B.
- Levanta `ValueError` con mensajes comprensibles para dimensiones incompatibles.
- No usa internamente `A @ B`, `np.matmul`, `np.dot` ni `np.einsum`.

## 4. Pruebas automáticas

`tests/test_mimatmul.py` incluye:

- un caso conocido (multiplicación 2x2 con resultado calculado a mano);
- matrices cuadradas;
- matrices rectangulares;
- comparación de resultados con NumPy (cuadradas y rectangulares);
- dimensiones incompatibles (levanta `ValueError`);
- matrices vacías y no rectangulares.

Se ejecutan todas con:

```
pytest
```

Resultado: 10 pruebas, todas pasan.

## 5. Benchmark

`src/benchmark.py` compara:

- `mimatmul` (Python puro);
- NumPy con `A @ B`.

Características:

- matrices `float64`;
- tamaños `n = 32, 64, 128, 256, 384`;
- 5 repeticiones por tamaño y método;
- ejecución de calentamiento para cada método;
- reloj `time.perf_counter()` (reloj de alta resolución);
- cada repetición se guarda por separado en `data/benchmark_results.csv`
  (columnas: `metodo`, `tamano`, `repeticion`, `tiempo`).

Los tamaños se eligieron para que el benchmark sea seguro para este computador:
`mimatmul` escala como O(n³) y a n = 384 tarda unos 4 segundos por ejecución,
por lo que el benchmark completo tarda menos de un minuto y usa poca RAM.

## 6. Datos finales

`data/benchmark_results.csv` contiene 50 mediciones reales realizadas en este
computador (5 tamaños × 2 métodos × 5 repeticiones). No se editaron los tiempos.

## 7. Gráfico final

`figures/benchmark.png` muestra:

- tamaño de la matriz en el eje horizontal;
- tiempo de ejecución (segundos) en el eje vertical;
- los resultados de `mimatmul` y de NumPy, identificados con etiquetas y
  leyenda;
- escala logarítmica en el eje vertical para poder ver ambos métodos (NumPy es
  miles de veces más rápido).

## 8. Observaciones de rendimiento

1. **¿`mimatmul` parece utilizar uno o varios núcleos?**
   Uno. Medí el tiempo de pared y el tiempo de CPU del proceso con
   `time.perf_counter()` y `time.process_time()`. Para `mimatmul` la razón
   CPU/pared fue de 1.00 (p. ej. 4.22 s de pared y 4.20 s de CPU), es decir,
   consume el equivalente a un solo núcleo. Además, Python tiene el GIL, que
   impide usar varios núcleos desde un solo hilo de Python.

2. **¿NumPy parece utilizar uno o varios núcleos?**
   Varios. Con la misma medición, la razón CPU/pared de `A @ B` fue mayor que 1:
   unas 4 veces a n = 384 y casi 9 veces a n = 2048 (11.05 s de CPU en 1.23 s de
   pared). NumPy llama a BLAS (OpenBLAS), que lanza varios hilos y reparte el
   trabajo entre los 12 procesadores lógicos.

3. **¿Por qué NumPy es más rápido?**
   Varias razones combinadas:
   - NumPy ejecuta operaciones escritas en C/Fortran optimizadas (BLAS) en vez
     de interpretar un ciclo Python por cada elemento.
   - Usa varios núcleos en paralelo, mientras que `mimatmul` usa uno solo.
   - Aprovecha el cache de memoria (bloques) y extensiones SIMD del CPU, algo
     que un ciclo `for` de Python no hace.
   En las mediciones la diferencia fue de ~60x a n = 32 y de ~2500x a n = 384
   (comparando las medianas de cada método).

4. **¿Por qué las repeticiones no entregan exactamente el mismo tiempo?**
   Porque el tiempo depende del estado del sistema: otros procesos (navegador,
   OneDrive, Windows) compiten por el CPU, la frecuencia del procesador varía
   (turbo/ahorro de energía), y las matrices dejan de caber en el cache a medida
   que crecen. Por eso se miden varias repeticiones y se usa la mediana.

5. **¿Cuál es aproximadamente la matriz cuadrada de mayor tamaño que cabría en
   la RAM libre del computador?**
   En el momento de medir había 0.63 GB libres (674459648 bytes). Una matriz
   `float64` de n×n ocupa 8·n² bytes. Para guardar una sola matriz,
   n ≈ sqrt(674459648 / 8) ≈ 9200, es decir, unas 9000×9000. Para multiplicar
   dos matrices con `A @ B` se necesitan A, B y el resultado en memoria
   (3 matrices), por lo que n ≈ sqrt(674459648 / 24) ≈ 5300, unas 5000×5000.
   La RAM libre varía según los programas abiertos, así que estos valores son
   aproximados.

## 9. Uso de OpenCode

1. **¿Qué parte realizó correctamente el agente?**
   Implementó `mimatmul` con la validación de dimensiones, escribió el benchmark
   (`src/benchmark.py`), generó el CSV con las mediciones y el gráfico PNG,
   actualizó `requirements.txt`, `system_info.py` y las instrucciones del README,
   y ejecutó `pytest` y el benchmark para verificar que todo funcionara.

2. **¿Qué parte tuvo que corregir o modificar?**
   Reescribí las pruebas de `unittest` a `pytest` (con `pytest.raises` y
   `np.testing.assert_allclose`) y agregué las pruebas de comparación con NumPy.
   También ajusté el benchmark para guardar cada repetición en el CSV y para
   hacer el calentamiento antes de medir, y modifiqué `system_info.py` para
   incluir la RAM libre.

3. **¿Qué archivo comprende mejor después del proyecto?**
   `src/mimatmul.py`: es la implementación más corta y la que más veces revisé.
   Después de escribir el benchmark y las pruebas, entiendo cada línea: la
   validación de dimensiones, los tres ciclos anidados y cómo el elemento
   (i, j) se calcula sumando productos de la fila i con la columna j.

4. **¿Qué parte del código todavía le resulta menos clara?**
   Lo que menos claro me queda es la generación de datos del benchmark con
   `np.random.default_rng(n)` y cómo el tamaño se usa como semilla; funciona,
   pero todavía no domino bien la generación de números aleatorios de NumPy ni
   cómo configurar exactamente cuántos hilos usa OpenBLAS.

## Verificación antes de entregar

```
pytest
python src/benchmark.py
git status
```

`git status` no debería mostrar cambios pendientes. El commit final se sube con
`git push`.
