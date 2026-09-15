from enum import Enum
from conecta_4.square_board import *
from conecta_4.settings import BOARD_LENGTH
from copy import deepcopy


class ColumnClassification(Enum):
    """
    Posibles clasificaciones que puede tener una columna.

    Los números nos sirven para dar prioridad a unas jugadas sobre otras.
    Cuanto mayor sea el valor, mejor será la recomendación.
    """
    FULL = -1
    MAYBE = 10
    WIN = 100
    LOSE = 1
    BAD = 5


class ColumnRecommendations:
    """
    Guarda la posición de una columna y la clasificación que le da el oráculo.
    """

    def __init__(self, index, classification):
        """
        Creamos una recomendación para una columna concreta.
        """
        self.index = index
        self.classification = classification

    def __eq__(self, other):
        """
        Dos recomendaciones son iguales si tienen la misma clasificación.

        Aquí no nos importa que sean columnas distintas, sino que tengan
        la misma puntuación a la hora de elegir dónde jugar.
        """
        if not isinstance(other, self.__class__):
            return False
        else:
            return self.classification == other.classification

    def __hash__(self):
        """
        Devuelve el hash de la recomendación.
        """
        return hash((self.index, self.classification))

    def __repr__(self):
        """
        Nos sirve para poder ver por pantalla la clasificación
        que está dando el oráculo.
        """
        return f'{self.__class__}: {self.classification}'


class BaseOracle:
    """
    Es el oráculo más sencillo.

    Solo sabe distinguir entre una columna llena y una columna
    donde todavía se podría jugar.
    """

    def _get_recommendation(self, board, player):
        """
        Recorremos todas las columnas y guardamos una recomendación
        para cada una de ellas.
        """
        result = []

        # Ejemplo:
        # [(0, FULL), (1, MAYBE), (2, FULL), (3, MAYBE)]
        for i in range(len(board)):
            result.append(
                self._get_columns_recommendations(board, i, player)
            )

        return result

    def _get_columns_recommendations(self, board, i, player):
        """
        Por defecto una columna es MAYBE.

        Si está llena, ya sabemos que ahí no podemos jugar.
        """
        classification = ColumnClassification.MAYBE

        if board._columns[i].is_full():
            classification = ColumnClassification.FULL

        return ColumnRecommendations(i, classification)

    def full_or_win(self, board, player):
        """
        Comprueba si todavía queda alguna jugada WIN o MAYBE.

        Lo usa el LearningOracle cuando repasa hacia atrás una partida
        que ha terminado en derrota.
        """

        # Generamos las recomendaciones de esta posición.
        recomendaciones = self._get_recommendation(board, player)

        result = True

        # Si todavía encontramos una opción WIN o MAYBE,
        # significa que aún quedaba alguna jugada válida.
        for recomendacion in recomendaciones:
            if (
                recomendacion.classification == ColumnClassification.WIN
                or recomendacion.classification == ColumnClassification.MAYBE
            ):
                result = False
                break

        return result

    # Hooks.
    # Aquí no hacen nada, pero los oráculos que heredan de esta clase
    # pueden rellenarlos con su propia lógica.
    def back_track(self, list_of_moves):
        """
        Método preparado para que otro oráculo pueda repasar jugadas.
        """
        pass

    def to_bad(self, move):
        """
        Método preparado para que otro oráculo pueda marcar
        una jugada como mala.
        """
        pass


class SmartOracle(BaseOracle):
    """
    Además de saber si una columna está llena, intenta averiguar
    si una jugada hace ganar o puede hacer perder al jugador.
    """

    def _get_columns_recommendations(self, board, i, player):
        """
        Empezamos con la clasificación del oráculo base.

        Solo analizamos más la columna cuando todavía es MAYBE.
        """
        recommendations = super()._get_columns_recommendations(
            board, i, player
        )

        if recommendations.classification == ColumnClassification.MAYBE:

            # Primero miramos si jugando aquí ganamos directamente.
            if self._is_winning_bet(board, i, player):
                recommendations.classification = ColumnClassification.WIN

            # Si no ganamos, comprobamos si dejamos al rival
            # una victoria directa en su siguiente turno.
            elif self._is_losing_bet(board, i, player):
                recommendations.classification = ColumnClassification.LOSE

        return recommendations

    def _play_on_temporal_board(self, board, index, player):
        """
        Creamos una copia del tablero y hacemos la jugada sobre ella.

        Así podemos probar qué pasaría sin tocar el tablero real.
        """
        temporal_board = deepcopy(board)
        temporal_board.add(player.char, index)

        return temporal_board

    def _is_winning_bet(self, board, index, player):
        """
        Comprueba si al jugar en esa columna el jugador gana.
        """

        # Probamos la jugada en un tablero temporal.
        temporal_bet = self._play_on_temporal_board(
            board, index, player
        )

        return temporal_bet.is_victory(player.char)

    def _is_losing_bet(self, board, index, player):
        """
        Comprueba si nuestra jugada deja al rival una victoria inmediata.
        """

        # Primero hacemos nuestra jugada en una copia.
        temporal_bet = self._play_on_temporal_board(
            board, index, player
        )

        losing_bet = False

        # Ahora probamos todas las posibles respuestas del rival.
        for i in range(0, BOARD_LENGTH):

            # Si el rival puede ganar en alguna columna,
            # nuestra jugada no era buena.
            if self._is_winning_bet(
                temporal_bet, i, player.opponent
            ):
                losing_bet = True
                break

        return losing_bet


class MemoizationOracle(SmartOracle):
    """
    Este oráculo hace lo mismo que SmartOracle, pero además
    guarda las recomendaciones que ya ha calculado.

    Si vuelve a encontrar la misma situación, no tiene que
    calcularlo todo otra vez.
    """

    def __init__(self):
        """
        Creamos el diccionario donde vamos a guardar las recomendaciones.
        """
        super().__init__()

        # Aquí tendremos:
        # clave -> lista de recomendaciones
        self.memo_recommendations = {}

    def _make_key(self, board_code, player):
        """
        Creamos una clave usando el tablero y el jugador al que le toca.

        El mismo tablero puede tener recomendaciones distintas
        dependiendo de si juega x o juega o.
        """

        # Ejemplo:
        # x..o|xx.o|....|....@o
        return f'{board_code.str_board}@{player.char}'

    def _get_recommendation(self, board, player):
        """
        Busca las recomendaciones en la caché.

        Si todavía no las tenemos, las calculamos y las guardamos.
        """
        key = self._make_key(board.as_code(), player)

        # Primero miramos si ya conocemos esta situación.
        if key not in self.memo_recommendations:

            # Si no está guardada, la calculamos una sola vez.
            self.memo_recommendations[key] = (
                super()._get_recommendation(board, player)
            )

        # Si ya estaba, simplemente la recuperamos.
        return self.memo_recommendations[key]


class LearningOracle(MemoizationOracle):
    """
    Además de memorizar posiciones, este oráculo puede aprender
    de las partidas perdidas.

    Cuando detecta una jugada mala, cambia su clasificación a BAD
    para intentar no repetirla la próxima vez.
    """

    def to_bad(self, move):
        """
        Marca como BAD la columna que se jugó en una situación concreta.

        No decide qué columna es mala: esa información ya viene
        guardada dentro del Move.
        """

        # Reconstruimos la misma clave con la que guardamos
        # esta posición en la caché.
        key = self._make_key(move.board_code, move.player)

        # Recuperamos todas las recomendaciones de ese tablero.
        recomendaciones = self._get_recommendation(
            SquareBoard.from_board_code(move.board_code),
            move.player
        )

        # Cambiamos solamente la columna que se jugó.
        recomendaciones[move.position] = ColumnRecommendations(
            move.position,
            ColumnClassification.BAD
        )

        # Volvemos a guardar las recomendaciones ya corregidas.
        self.memo_recommendations[key] = recomendaciones

    def back_track(self, list_of_moves):
        """
        Repasa las jugadas después de una derrota.

        Empezamos por la jugada más reciente y vamos hacia atrás
        hasta encontrar una posición donde todavía había otra opción buena.
        """

        for move in list_of_moves:

            # Primero marcamos como mala la jugada que hicimos.
            self.to_bad(move)

            # Reconstruimos cómo estaba el tablero antes de esa jugada.
            board = SquareBoard.from_board_code(move.board_code)

            # Si todavía había alguna opción WIN o MAYBE,
            # ya hemos encontrado el punto donde se pudo jugar mejor.
            if not self.full_or_win(board, move.player):
                break
