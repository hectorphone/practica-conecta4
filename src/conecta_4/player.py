from random import choice

from conecta_4.oracle import *
from conecta_4.square_board import *
from conecta_4.move import *
from conecta_4.settings import BOARD_LENGTH


class Player:
    """
    Representa a un jugador del Conecta 4.

    El jugador tiene un nombre, una ficha, un oráculo que le recomienda
    dónde jugar y, si lo tiene, un oponente.
    """

    def __init__(self, name, char=None, oracle=BaseOracle(), opponent=None):
        """
        Inicializamos los datos necesarios del jugador.
        """
        self.name = name
        self.char = char
        self._oracle = oracle
        self.opponent = opponent

        # Aquí vamos guardando las jugadas realizadas.
        # La jugada más reciente siempre queda al principio.
        self.last_moves = []

    @property
    def opponent(self):
        """
        Devuelve el oponente de este jugador.
        """
        return self._opponent

    @opponent.setter
    def opponent(self, other):
        """
        Asigna el oponente en los dos sentidos.

        Si A tiene como oponente a B, también dejamos a A
        como oponente de B.
        """
        self._opponent = other

        if other is not None:
            # Usamos _opponent directamente para no volver a entrar
            # en el setter y crear un bucle entre los dos jugadores.
            other._opponent = self

    def play(self, board):
        """
        Pregunta al oráculo cuál es la mejor jugada y la realiza.
        """
        best, recommendations = self._ask_oracle(board)
        self._play_on(board, best.index, recommendations)

    def _play_on(self, board, position, recommendations):
        """
        Guarda la jugada elegida y después coloca la ficha en el tablero.

        Guardamos primero el estado anterior porque es el que necesita
        el oráculo si más adelante tiene que aprender de una derrota.
        """

        # Primero guardamos cómo estaba el tablero antes de jugar.
        self.last_moves.insert(
            0,
            Move(position, board.as_code(), recommendations, self)
        )

        # Ahora sí hacemos la jugada real.
        board.add(self.char, position)

    def _ask_oracle(self, board):
        """
        Pregunta al oráculo las posibles jugadas y elige una de ellas.
        """
        recommendations = self._oracle._get_recommendation(board, self)
        best = self._choose_a_recommendation(recommendations)

        return best, recommendations

    def _choose_a_recommendation(self, recommendations):
        """
        Elige la mejor opción entre las recomendaciones del oráculo.
        """

        # Quitamos las columnas llenas porque ahí no podemos jugar.
        valid_recommendations = list(
            filter(
                lambda x: x.classification != ColumnClassification.FULL,
                recommendations
            )
        )

        # Ordenamos de mayor a menor para dejar primero
        # la recomendación con mejor puntuación.
        valid_recommendations = sorted(
            valid_recommendations,
            key=lambda x: x.classification.value,
            reverse=True
        )

        # Si todas tienen la misma puntuación elegimos una al azar.
        if all_the_same_score(valid_recommendations):
            return choice(valid_recommendations)

        # Si no, nos quedamos con la mejor.
        return valid_recommendations[0]

    # Hook. La clase base no hace nada.
    # Las clases que lo necesiten pueden rellenarlo.
    def _on_lose(self):
        """
        Se ejecuta cuando el jugador pierde.

        Aquí no hacemos nada, pero otras clases pueden sobrescribir
        este método para reaccionar a una derrota.
        """
        pass


class HumanPlayer(Player):
    """
    Representa al jugador humano.

    En vez de preguntar a un oráculo automático, le preguntamos
    directamente al usuario qué columna quiere jugar.
    """

    def __init__(self, name, char=None):
        """
        Inicializamos al jugador humano usando lo que ya tiene Player.
        """
        super().__init__(name, char)

    def _ask_oracle(self, board):
        """
        En este caso el "oráculo" es el propio jugador.

        Pedimos una columna por pantalla y comprobamos que sea válida.
        """
        while True:
            position = input("Tu turno! Selecciona una columna: ")

            # Comprobamos que sea un número, que esté dentro del tablero
            # y que la columna todavía tenga hueco.
            if (
                HumanEntryVerifications._is_int(position)
                and HumanEntryVerifications._is_in_range(board, int(position))
                and HumanEntryVerifications._is_not_full(board, int(position))
            ):
                position = int(position)

                # El jugador humano no necesita una clasificación del oráculo.
                return ColumnRecommendations(position, None), None


class HumanEntryVerifications:
    """
    Agrupa las comprobaciones de los datos que introduce el usuario.
    """

    @staticmethod
    def _is_int(cadena):
        """
        Comprueba si el valor introducido se puede convertir a entero.
        """
        try:
            int(cadena)
            return True
        except:
            return False

    @staticmethod
    def _is_not_full(board, col):
        """
        Comprueba que todavía se pueda jugar en esa columna.
        """
        return not board._columns[col].is_full()

    @staticmethod
    def _is_in_range(board, col):
        """
        Comprueba que la columna esté dentro del tablero.
        """
        return 0 <= col < len(board)


class ReportingPlayer(Player):
    """
    Jugador que informa al oráculo cuando pierde para que pueda aprender.
    """

    def _on_lose(self):
        """
        Cuando pierde, le pasa sus últimas jugadas al oráculo
        para que las revise hacia atrás.
        """
        self._oracle.back_track(self.last_moves)
