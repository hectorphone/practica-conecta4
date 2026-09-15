import pyfiglet
from beautifultable import BeautifulTable

from enum import Enum, auto

from conecta_4.match import *
from conecta_4.player import *
from conecta_4.list_utils import *


class RoundType(Enum):
    """
    Tipos de partida que podemos elegir.
    """
    Human_vs_Computer = auto()
    Computer_vs_Computer = auto()


class Level(Enum):
    """
    Niveles de dificultad disponibles para el ordenador.
    """
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class Game:
    """
    Controla el funcionamiento general del juego.

    Aquí configuramos la partida, creamos los jugadores,
    controlamos los turnos y mostramos el resultado.
    """

    def __init__(self):
        """
        Inicializamos el juego con un tablero vacío.
        """
        self.board = SquareBoard()

    def start_game(self):
        """
        Punto de inicio del juego.

        Mostramos el logo, pedimos la configuración
        y empezamos el bucle de la partida.
        """
        self._print_logo()
        self._configuration()
        self._game_loop()

    def _print_logo(self):
        """
        Muestra el logo de Conecta 4 por pantalla.
        """
        logo = pyfiglet.Figlet(font="swamp_land")
        print(logo.renderText("Conecta 4"))

    def _configuration(self):
        """
        Pide al usuario las opciones necesarias antes de empezar.
        """

        # Primero elegimos el tipo de partida.
        self.round_type = self._get_round_type()

        # Solo necesitamos elegir dificultad si jugamos
        # contra el ordenador.
        if self.round_type == RoundType.Human_vs_Computer:
            self._difficulty_level = self._get_level()

        # Con la configuración lista creamos la partida.
        self.match = self._match()

    def _get_round_type(self):
        """
        Pregunta qué tipo de partida queremos jugar.
        """
        print("""
        Selecciona las opciones disponibles:

        1) Humano vs Computadora
        2) Computadora vs Computadora
        """)

        respuesta = ""

        # Seguimos preguntando hasta recibir una opción válida.
        while respuesta != '1' and respuesta != '2':
            respuesta = input('Selecciona 1 ó 2: ')

        if respuesta == '1':
            return RoundType.Human_vs_Computer

        return RoundType.Computer_vs_Computer

    def _get_level(self):
        """
        Pregunta el nivel de dificultad del ordenador.
        """
        print("""
        Selecciona las opciones disponibles:

        1) Fácil
        2) Intermedio
        3) Difícil
        """)

        while True:
            respuesta = input("Selecciona entre 1, 2 ó 3: ")

            if respuesta == '1':
                return Level.LOW

            elif respuesta == '2':
                return Level.MEDIUM

            elif respuesta == '3':
                return Level.HIGH

    def _match(self):
        """
        Crea los dos jugadores dependiendo del tipo de partida.

        El tipo de oráculo que usamos marca la dificultad
        del jugador controlado por el ordenador.
        """

        # Relacionamos cada nivel con el oráculo correspondiente.
        _levels = {
            Level.LOW: BaseOracle(),
            Level.MEDIUM: SmartOracle(),
            Level.HIGH: LearningOracle()
        }

        if self.round_type == RoundType.Computer_vs_Computer:

            # Los dos ordenadores utilizan LearningOracle
            # para poder aprender de las derrotas.
            player1 = ReportingPlayer(
                'Ordenador 1',
                oracle=LearningOracle()
            )

            player2 = ReportingPlayer(
                'Ordenador 2',
                oracle=LearningOracle()
            )

        else:
            # El ordenador utiliza el oráculo correspondiente
            # al nivel elegido por el usuario.
            player1 = ReportingPlayer(
                'Computer',
                oracle=_levels[self._difficulty_level]
            )

            # El segundo jugador es la persona que juega por pantalla.
            player2 = HumanPlayer(
                name=input('Ingrese su nombre: ')
            )

        return Match(player1, player2)

    def _game_loop(self):
        """
        Controla el bucle principal de la partida.

        Vamos alternando jugadores hasta que alguien gane
        o el tablero termine lleno.
        """

        while True:

            # Miramos a quién le toca jugar.
            jugador_actual = self.match.get_next_player

            # El jugador realiza su movimiento.
            jugador_actual.play(self.board)

            # Mostramos qué ha jugado.
            self._print_move(jugador_actual)

            # Mostramos cómo queda el tablero.
            self._print_board()

            # Comprobamos si la partida ha terminado.
            if self._winner_or_tie():

                self._print_result()

                # Preguntamos si queremos empezar otra partida.
                if self.match.play_more():

                    # Empezamos con un tablero nuevo.
                    self.board = SquareBoard()
                    self._print_board()

                else:
                    break

    def _print_board(self):
        """
        Muestra el tablero por pantalla.
        """

        # Le damos la vuelta a las columnas para que el tablero
        # se vea como esperamos al imprimirlo.
        board_matrix = reverse_matrix(
            self.board.as_matrix()
        )

        bt = BeautifulTable()

        for col in board_matrix:
            bt.columns.append(col)

        # Ponemos el número de cada columna arriba.
        bt.columns.header = [
            str(i) for i in range(BOARD_LENGTH)
        ]

        print(bt)

    def _print_result(self):
        """
        Muestra el ganador y el perdedor.

        Si no hay ganador significa que la partida terminó en empate.
        """
        ganador = self.match.get_winner(self.board)
        perdedor = self.match.get_loser(self.board)

        if ganador is not None:
            print(
                f'{ganador.name} ({ganador.char}) '
                f'GANA VS {perdedor.name} ({perdedor.char})'
            )

        else:
            print('EMPATE')

    def _print_move(self, player):
        """
        Muestra quién ha jugado y en qué columna.
        """
        print(
            f'{player.name} ({player.char}) '
            f'ha movido en {player.last_moves[0].position}'
        )

    def _winner_or_tie(self):
        """
        Comprueba si la partida ha terminado por victoria o empate.
        """

        ganador = self.match.get_winner(self.board)

        if ganador is not None:

            # Avisamos al jugador que ha perdido.
            # Si usa LearningOracle podrá revisar sus jugadas.
            ganador.opponent._on_lose()

            return True

        elif self.board.is_full():
            return True

        return False
