class Move:
    """
    Guarda la información de una jugada.

    Nos sirve para poder revisar después qué decisión tomó el jugador
    y cómo estaba el tablero en ese momento.
    """

    def __init__(self, position, board_code, recommendation, player):
        """
        Guardamos todos los datos necesarios de una jugada.
        """

        # Columna donde se ha jugado.
        self.position = position

        # Estado del tablero antes de realizar la jugada.
        self.board_code = board_code

        # Recomendaciones que había en ese momento.
        self.recommendation = recommendation

        # Jugador que realizó la jugada.
        self.player = player
