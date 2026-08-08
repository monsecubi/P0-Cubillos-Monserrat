# P0-Cubillos-Monserrat

## Propósito general

Implementar en Python puro una función de multiplicación de matrices
(`mimatmul`), recolectar información del computador y, en una etapa posterior
(P0E2), medir el rendimiento de `mimatmul` frente a `numpy` usando matrices de
distintos tamaños, generando datos, gráficos y un análisis de uso de CPU y RAM.

## Sistema operativo

Windows. La versión exacta y el resto de los datos se guardan en
`data/system_info.json`.

## Versión de Python

3.12.10

## Ambiente virtual

Crear el ambiente virtual:

```
python -m venv .venv
```

Activarlo (Windows):

```
.venv\Scripts\activate
```

Desactivarlo:

```
deactivate
```

## Instalar dependencias

```
pip install -r requirements.txt
```

## Obtener la información del computador

```
python src/system_info.py
```

## Ejecutar las pruebas

```
python -m unittest discover -s tests -v
```

## Estado actual

- [x] Ambiente de desarrollo configurado (Python, Git, GitHub, OpenCode, editor, venv).
- [x] Información del computador (`src/system_info.py` -> `data/system_info.json`).
- [x] Primera versión de `mimatmul` con una prueba inicial.
- [ ] Benchmark definitivo, gráficos y análisis completo (P0E2).
