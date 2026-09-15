from conecta_4.settings import BOARD_LENGTH, VICTORY_STRIKE
from conecta_4.list_utils import find_strike, make_list, index_first_element


class LinearBoard:
    """
    Representa una sola columna del tablero.

    Las fichas pueden ser:
    - x para un jugador
    - o para el otro jugador
    - None cuando la casilla está vacía
    """

    @classmethod
    def from_list(cls, data):
        """
        Crea un LinearBoard a partir de una lista que ya tiene datos.
        """
        board = cls()

        # Creamos primero la columna y después sustituimos
        # su contenido por la lista que nos han pasado.
        board._columns = data

        return board

    # Dunders. Cosas que Python puede preguntarle al objeto.

    def __init__(self):
        """
        Crea una columna vacía con el tamaño del tablero.
        """
        self._columns = make_list(BOARD_LENGTH, None)

        # Otra forma de hacerlo sería:
        # [None for i in range(BOARD_LENGTH)]

    def __eq__(self, other):
        """
        Permite comparar dos LinearBoard usando ==.

        Son iguales si tienen las mismas fichas
        en las mismas posiciones.
        """
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._columns == other._columns

    def __hash__(self):
        """
        Devuelve el hash de la columna.

        Convertimos la lista a tupla porque las listas
        no se pueden hashear directamente.
        """
        return hash(tuple(self._columns))

    # Cosas que puede hacer la columna.

    def get_columns(self):
        """
        Devuelve la lista que representa la columna.
        """
        return self._columns

    def is_full(self):
        """
        Comprueba si la columna está llena.

        Como las fichas se van apilando sin dejar huecos,
        basta con mirar la última posición.
        """
        return self._columns[-1] is not None

    def add(self, char):
        """
        Añade una ficha en la primera posición vacía.

        Si la columna ya está llena, no hacemos nada.
        """
        if not self.is_full():

            # Buscamos el primer hueco disponible.
            i = index_first_element(self._columns, None)

            # Colocamos aquí la ficha del jugador.
            self._columns[i] = char

    def is_victory(self, char):
        """
        Comprueba si el jugador tiene una racha suficiente
        para ganar dentro de esta columna.
        """
        return find_strike(
            self._columns,
            char,
            VICTORY_STRIKE
        )

    def is_tie(self, char_1, char_2):
        """
        Comprueba que ninguno de los dos jugadores haya ganado.
        """
        return (
            self.is_victory(char_1) == False
            and self.is_victory(char_2) == False
        )
