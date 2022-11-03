# push-swap-test

## Instalación

1. Clonar el repositorio
2. Editar el archivo `push-swap-test.py` y modificar la línea 44. Sustituir el valor por la ruta donde se encuentra `push_swap`.
3. Lanzar en la terminal con `./push-swap-test.py` o bien `python3 push-swap-test.py`.

## Personalización

- En la línea 63 se define la batería de pruebas. Se puede editar añadiendo o eliminando líneas. El formato es:
    `[NÚMERO_O_TEXTO, NÚMERO_O_TEXTO, ... ],`
- En la línea 107 se define el procedimiento principal `main`. Se puede editar añadiendo o eliminando casos. Por ejemplo, para añadir una pila de 20 números aleatorios que se lance 10 veces se añadiría una línea con:
    `print_random_numbers(20, 10)`