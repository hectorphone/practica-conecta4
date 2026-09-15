from conecta_4.linear_board import LinearBoard
from conecta_4.settings import BOARD_LENGTH
from conecta_4.list_utils import *


class SquareBoard:
    """
    Representa el tablero completo del Conecta 4.

    El tablero está formado por varios LinearBoard, que en nuestro caso
    representan las columnas.
    """

    @classmethod
    def from_list(cls, list_of_list):
        """
        Crea un SquareBoard partiendo de una lista de listas.

        Nos viene bien cuando ya tenemos las casillas preparadas
        y queremos convertirlas otra vez en un tablero.
        """
        board = cls()

        # Convertimos cada lista en un LinearBoard.
        board._columns = map_list(
            list_of_list,
            LinearBoard.from_list
        )

        return board

    @classmethod
    def from_str_board(cls, str_board):
        """
        Reconstruye un tablero partiendo de su versión en texto.

        Hacemos el camino contrario a cuando convertimos el tablero
        en código.
        """

        # Separamos cada columna usando |.
        list_of_strings = str_board.split('|')

        # Convertimos cada texto en una lista.
        matrix = explode_list(list_of_strings)

        # Los puntos representan casillas vacías.
        # Los volvemos a convertir en None.
        matrix = replace_all(matrix, '.', None)

        # Finalmente transformamos la matriz en un SquareBoard.
        return cls.from_list(matrix)

    @classmethod
    def from_board_code(cls, board_code):
        """
        Reconstruye un tablero a partir de un BoardCode.
        """
        return cls.from_str_board(board_code.str_board)

    # Dunders. Son cosas que Python puede preguntarle al objeto.

    def __init__(self):
        """
        Creamos un tablero vacío con BOARD_LENGTH columnas.
        """
        self._columns = make_list_from_factory(
            BOARD_LENGTH,
            LinearBoard
        )

    def __repr__(self):
        """
        Nos permite ver el tablero de una forma más clara
        cuando lo imprimimos o depuramos.
        """
        return f'{self.__class__}:{self._columns}'

    def __len__(self):
        """
        Devuelve el número de columnas que tiene el tablero.
        """
        return len(self._columns)

    def __eq__(self, other):
        """
        Compara dos tableros.

        Son iguales si tienen las mismas columnas
        y las mismas fichas en cada una.
        """
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._columns == other._columns

    def __hash__(self):
        """
        Devuelve el hash del tablero.

        Convertimos las columnas a tupla porque una lista
        directamente no se puede usar para calcular un hash.
        """
        return hash(tuple(self._columns))

    # Métodos. Cosas que puede hacer el tablero.

    def is_full(self):
        """
        Comprueba si todas las columnas del tablero están llenas.
        """
        result = True

        for linear_board in self._columns:
            result = result and linear_board.is_full()

        return result

    def add(self, char, column):
        """
        Añade la ficha del jugador en la columna elegida.
        """
        result = self._columns[column].add(char)
        return result

    def as_matrix(self):
        """
        Devuelve el tablero como una lista de listas.

        Cada lista representa una de las columnas.
        """
        result = []

        for column in self._columns:
            result.append(column._columns)

        return result

        # Otra forma de hacerlo sería:
        # return map_list(self._columns, LinearBoard.get_columns)

    def as_code(self):
        """
        Convierte el tablero en un BoardCode para poder guardarlo
        o usarlo como parte de una clave.
        """
        return BoardCode(self)

    def is_victory(self, char):
        """
        Comprueba si el jugador ha ganado en alguna dirección.

        Miramos vertical, las dos diagonales y horizontal.
        """
        return (
            self._any_vertical_victory(char)
            or self._any_descending_diagonal(char)
            or self._any_ascending_diagonal(char)
            or self._any_horizontal_victory(char)
        )

    def _any_vertical_victory(self, char):
        """
        Busca una victoria vertical en cualquiera de las columnas.

        Este es el caso más sencillo y el que vamos reutilizando
        para comprobar las demás direcciones.
        """
        result = False

        for linear_board in self._columns:
            result = result or linear_board.is_victory(char)

        return result

    def _any_horizontal_victory(self, char):
        """
        Comprueba la victoria horizontal.

        Transponemos el tablero para convertir las filas en columnas.
        Así podemos reutilizar la comprobación vertical.
        """

        # Intercambiamos filas y columnas.
        transpose_matrix = transpose(self.as_matrix())

        # Creamos un tablero con esa matriz transformada.
        transpose_board = SquareBoard.from_list(transpose_matrix)

        # Lo que antes era horizontal ahora es vertical.
        return transpose_board._any_vertical_victory(char)

    def _any_descending_diagonal(self, char):
        """
        Comprueba una diagonal descendente.

        Desplazamos las columnas para conseguir que la diagonal
        quede alineada como una horizontal.
        """

        matrix = self.as_matrix()

        # Movemos cada columna una cantidad diferente.
        dm = displace_matrix(matrix)

        displace_board = SquareBoard.from_list(dm)

        # Ahora que la diagonal se ha convertido en horizontal,
        # reutilizamos la comprobación que ya tenemos.
        return displace_board._any_horizontal_victory(char)

    def _any_ascending_diagonal(self, char):
        """
        Comprueba una diagonal ascendente.

        Primero invertimos las columnas para convertirla
        en una diagonal descendente.
        """

        matrix = self.as_matrix()

        # Damos la vuelta a las columnas.
        rm = reverse_matrix(matrix)

        reverse_board = SquareBoard.from_list(rm)

        # Una vez invertida, podemos tratarla como diagonal descendente.
        return reverse_board._any_descending_diagonal(char)


class BoardCode:
    """
    Guarda una representación del tablero en forma de texto.

    El SquareBoard nos sirve para jugar, mientras que BoardCode
    nos viene mejor para guardar, comparar o identificar una posición.
    """

    def __init__(self, board):
        """
        Convertimos el tablero completo en una cadena de texto.
        """
        self._str_board = colpase_matrix(board.as_matrix())

    @property
    def str_board(self):
        """
        Devuelve el tablero guardado como texto.
        """
        return self._str_board

    def __eq__(self, other):
        """
        Dos BoardCode son iguales si contienen exactamente
        la misma representación del tablero.
        """
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._str_board == other.str_board

    def __hash__(self):
        """
        Devuelve el hash de la cadena que representa el tablero.
        """
        return hash(self._str_board)

    def __repr__(self):
        """
        Nos permite ver fácilmente el código del tablero
        cuando lo imprimimos.
        """
        return f'{self._str_board}:{self.__class__}'
