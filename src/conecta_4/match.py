class Match:
    """
    Controla los jugadores de una partida.

    Se encarga de asignar las fichas, saber de quién es cada una
    y alternar los turnos.
    """

    def __init__(self, player1, player2):
        """
        Preparamos los dos jugadores para empezar la partida.
        """

        # Asignamos las fichas a mano.
        # Más adelante se podrían elegir al azar.
        player1.char = 'o'
        player2.char = 'x'

        # Dejamos enlazados los dos jugadores como oponentes.
        player1.opponent = player2

        # El diccionario nos permite encontrar rápido
        # qué jugador corresponde a cada ficha.
        self._players = {
            'o': player1,
            'x': player2
        }

        # Esta lista nos sirve para ir alternando los turnos.
        self._round = [player1, player2]

    @property
    def get_next_player(self):
        """
        Devuelve el jugador al que le toca.

        Después damos la vuelta al orden para que en la siguiente
        llamada juegue el otro.
        """
        next_player = self._round[0]

        # Invertimos el orden de los jugadores.
        self._round.reverse()

        return next_player

    def get_player(self, char):
        """
        Devuelve el jugador que tiene esa ficha.
        """
        return self._players[char]

    def get_winner(self, board):
        """
        Comprueba si hay un ganador y devuelve el jugador correspondiente.
        """

        if board.is_victory('x'):
            return self.get_player('x')

        if board.is_victory('o'):
            return self.get_player('o')

        return None

    def get_loser(self, board):
        """
        Si hay un ganador, devuelve el jugador que ha perdido.
        """

        if board.is_victory('x'):
            return self.get_player('o')

        if board.is_victory('o'):
            return self.get_player('x')

        return None

    def play_more(self):
        """
        Pregunta al usuario si quiere jugar otra partida.
        """

        while True:
            answer = input(
                '¿Le apetece una partida más? S/N '
            )

            if answer.lower() == 's':
                return True

            elif answer.lower() == 'n':
                return False
