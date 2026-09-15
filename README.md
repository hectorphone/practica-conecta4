# Conecta 4

Este proyecto forma parte de la práctica de Conecta 4 del bootcamp.

La idea principal de la práctica ha sido entender cómo está montado el juego, cómo se relacionan las distintas clases y qué decisiones de diseño se han tomado. El juego ya venía desarrollado y durante la práctica he ido revisando el código, entendiendo cada parte, comentándolo y ejecutando los tests.

## Cómo funciona

El juego permite jugar de dos formas:

- Humano contra ordenador.
- Ordenador contra ordenador.

Si jugamos contra el ordenador podemos elegir tres niveles de dificultad:

- Fácil.
- Intermedio.
- Difícil.

Cada nivel usa un tipo de oráculo distinto para decidir la jugada.

El tablero que usamos es de 4x4 y para ganar hay que conseguir 3 fichas seguidas.

## Archivos principales

El proyecto está dividido en varios archivos para que cada uno tenga una responsabilidad concreta.

- `game.py`: controla el juego en general.
- `match.py`: controla los jugadores y los turnos.
- `player.py`: contiene los distintos tipos de jugador.
- `oracle.py`: decide qué jugada es mejor.
- `square_board.py`: representa el tablero completo.
- `linear_board.py`: representa una columna.
- `list_utils.py`: tiene funciones auxiliares para trabajar con listas y matrices.
- `move.py`: guarda la información de cada jugada.
- `settings.py`: contiene la configuración del tablero.

## Cómo ejecutar el juego

Desde la carpeta principal del proyecto:

```bash
uv run python src/conecta_4/conecta4.py
```

También se puede ejecutar desde PyCharm usando el entorno virtual del proyecto.

## Tests

Para ejecutar todos los tests:

```bash
uv run pytest
```

Actualmente el proyecto tiene 27 tests y todos pasan correctamente.

## Algunas decisiones de diseño

Una de las cosas que más me ha ayudado a entender el proyecto es ver cómo se reutiliza código.

Por ejemplo, para comprobar victorias horizontales y diagonales no se hace un algoritmo completamente distinto cada vez. Se transforma el tablero y se reutiliza la comprobación vertical.

También se separa la lógica del jugador de la lógica del oráculo. El jugador se encarga de jugar y el oráculo se encarga de decidir qué jugada puede ser mejor.

En las jugadas que se quieren probar sin modificar el tablero real se usa una copia temporal del tablero.

También se guarda una representación del tablero como texto. Esto permite identificar una posición de forma sencilla y utilizarla en la caché del oráculo.

## LearningOracle

El `LearningOracle` guarda recomendaciones de situaciones que ya ha visto.

Cuando pierde una partida puede revisar jugadas anteriores y marcar alguna como `BAD`.

La idea es que, si vuelve a encontrarse en la misma situación, tenga guardada esa información y pueda evitar repetir una jugada que ya salió mal.

## Autor

Héctor Pérez Álvarez
