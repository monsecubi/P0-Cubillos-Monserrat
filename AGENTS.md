# AGENTS.md

Instrucciones básicas para OpenCode en este repositorio.

## Propósito del proyecto

Implementar la función `mimatmul` (multiplicación de matrices en Python puro),
compararla con `numpy` y documentar los resultados (benchmark, gráficos y
análisis de CPU y RAM).

## Reglas básicas

- Mantener el código sencillo y legible.
- No inventar mediciones ni resultados: todo dato debe provenir de ejecuciones
  reales en este computador.
- No ejecutar comandos destructivos de Git (por ejemplo, `git reset --hard`,
  `git rebase`, `git push --force`).
- No subir credenciales ni claves al repositorio; revisar antes de commitear.
- Ejecutar las pruebas después de modificar código:

```
python -m unittest discover -s tests -v
```

- Hacer commits pequeños y descriptivos directamente en `main`.
