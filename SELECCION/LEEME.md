# Selección de imágenes para el entrenamiento

La carpeta original `ILUSTRACION_ESTILO/` no se ha tocado. Aquí hay copias de las elegidas.
El número delante de cada archivo es su posición en orden alfabético dentro de la carpeta original.

## Estilo elegido

Dibujo suelto de **lápiz, lápiz de color y algo de acuarela/aguada sobre papel blanco**, figura aislada sin fondo.
Es el que encaja con el objetivo: personajes con fondo transparente y animación de temblor de trazo.

- `NUCLEO/` (48): escaneos o imágenes limpias sobre blanco. Base del entrenamiento.
- `FOTOGRAFIADAS/` (11): buen trazo, pero son fotos del papel con sombras y fondo gris.
  Se usarán después de limpiarles el fondo (lo hace el script de preparación).

## Descartadas (68) y motivo

| Motivo | Números |
|---|---|
| Duplicado exacto | 10 (= 11) |
| Cómic / páginas con viñetas y color plano digital | 7, 11, 16, 17, 25, 26, 28, 29, 32, 33, 39, 42, 44, 46, 50, 57, 60, 65, 67, 71, 78, 82, 84, 92, 95, 97, 100, 104, 106, 109, 113, 118, 119 |
| Tinta negra a pincel muy contrastada (otra técnica) | 12, 43, 48, 52, 55, 68, 70, 73, 74, 77, 79, 88, 99, 105, 110 |
| Personajes con copyright (el modelo los aprendería) | 9, 31, 72, 96, 122 |
| Fondos de color planos / composiciones digitales | 0, 18, 19, 34, 66, 75, 80, 81, 90, 114, 116, 124 |
| Mockup de revista | 69 |
| Resolución demasiado baja | 8 |

`resumen_seleccion.jpg` muestra todas las elegidas de un vistazo.
