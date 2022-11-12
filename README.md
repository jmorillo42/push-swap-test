# push-swap-test

## Instalación

1. Clonar el repositorio
2. Editar el archivo `config.py` y modificar la línea 2. Sustituir el valor por la ruta donde se encuentra `push_swap`.
3. Lanzar en la terminal con `python3 push-swap-test.py` (o bien `./push-swap-test.py` si tiene el atributo de ejecución).

## Personalización

En el fichero `config.py` están definidas las constantes que se utilizarán para los tests:

- PUSH_SWAP: Ruta del comando `push_swap`
- CHECKER: Ruta del comando `checker`
- INPUT_TESTS: Colección de pruebas de entrada. Se verifican las salidas con el checker de 42.
- COMB_ALL_TESTS: Combinaciones de N números. Se imprimen los resultados de cada combinación.
- COMB_STAT_TESTS: Combinaciones de de N números. Se imprimen las estadísticas globales.
- SEQ_TESTS: Secuencias de N números. Se lanza una secuencia en sus formas, creciente y decreciente. Además, las combinaciones de dos secuencias crecientes y decrecientes.
- RANDOM_TESTS: Repeticiones de series aleatorias de N números.
- CHECKER_TESTS: Colección de pruebas del `checker`. Se comparan resultados con el checker de 42.

Se pueden añadir o eliminar pruebas. Cada una de las tuplas definidas en el fichero `config.py` se pueden personalizar modificando algún otro caso que se quiera verificar.
