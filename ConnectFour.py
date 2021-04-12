"""Holds the Connect Four Game"""
from __future__ import annotations
from typing import Optional, Tuple, Type, List

from Game import Game, GameState
import pygame
import copy


class ConnectFourGameState(GameState):
    """Stores the game state of a TicTacToe game

    Instance Attributes:
        - n: The dimension of the board. Must be even.
        - board: A 2D nxn list storing the object in each position in the game.
            A 1 is placed if player 1's piece is in the location, 0 if it is player 2's piece and -1 if it is empty.
        - turn: Stores the turn of the player. This is true if it is X's turn and False otherwise.
        - game_type: Holds the type of game.
        - previous_move: Stores the previous move made. This is None if no move has been made yet.
    """
    n: int
    board: list[list[int]]
    turn: bool
    game_type: Type[Game]
    previous_move: Optional[int]

    def __init__(self, n: int = 6, game_state: Optional[ConnectFourGameState] = None) -> None:
        self.game_type = ConnectFour
        self.previous_move = None
        if game_state is None:
            self.board = [[-1] * n for _ in range(n)]
            self.turn = True
        else:
            self.board = copy.deepcopy(game_state.board)
            self.turn = game_state.turn

        self.n = n

    def vector_representation(self) -> List[float]:
        """Return the flattened board"""
        vector = []
        for row in self.board:
            vector.extend(row)
        return vector

    def is_legal(self, move: int) -> bool:
        """Return whether the next move is legal from the game state in self

        Preconditions:
            - 0 <= move[0] <= 3
            - 0 <= move[1] <= 3
        """
        return self.board[0][move] == -1

    def make_move(self, move: int, check_legal: bool = True) -> bool:
        """Play move. Returns False if move is not legal and True otherwise.

        Preconditions:
            - 0 <= move <= self.n
        """
        if not check_legal and self.is_legal(move):
            self.previous_move = move
            if self.turn:
                piece = 1
            else:
                piece = 0

            placed_piece = False
            row = 0
            while not placed_piece and row < self.n:
                row += 1
                if self.board[row][move] != -1:
                    self.board[row - 1][move] = piece
                    placed_piece = True

            if row == self.n:
                self.board[-1][move] = piece

            self.turn = not self.turn
            return True
        else:
            return False

    def evaluate_position(self, heuristic_type: int = 0) -> float:
        """Return an evaluation of the current position.
        There is only the default heuristic for Connect 4:
        1 is returned if X wins and -1 is returned if O wins. 0 is returned otherwise.
        """
        winner = self.winner()
        if winner == (True, True):
            return 1
        elif winner == (True, False):
            return -1
        return 0

    def legal_moves(self) -> list[GameState]:
        """Return all legal moves from this position"""

        # Checks if the game is over
        if self.winner() is not None:
            return []

        possible_moves = []
        for i in range(self.n):
            if self.is_legal(i):
                new_game = ConnectFourGameState(self.n, self)
                new_game.make_move(i, False)
                possible_moves.append(new_game)
        return possible_moves

    def winner(self) -> Optional[Tuple[bool, bool]]:
        """Return (True, True) if Red won, (True, False) if Yellow won,
        (False, False) if there is a tie, and None if the game is not over."""
        # TODO: Finish

        is_over = all(
            self.board[i][j] != -1
            for i in range(self.n)
            for j in range(self.n)
        )

        if is_over:
            return (False, False)
        else:
            return None

    def board_object(self, x, y) -> str:
        """Return a string representing the piece
        at the location (x, y) on the board
        """
        piece = self.board[x][y]
        if piece == 1:
            return 'R'
        elif piece == 0:
            return 'Y'
        else:
            return ''

    def equal(self, game_state: ConnectFourGameState) -> bool:
        """Return whether self is equal to game_state"""
        return self.board == game_state.board

    def __str__(self) -> str:
        """A unique string representation of the board for memoization and debugging."""
        state_string = ""
        for row in self.board:
            for piece in row:
                if piece == -1:
                    state_string += " - "
                elif piece == 0:
                    state_string += " Y "
                else:
                    state_string += " R "
            state_string += "\n"
        return state_string

    def display(self, screen: pygame.display) -> None:
        """Display the current TicTacToe Board on screen"""
        w, h = screen.get_size()

        # TODO: fix

        # Draw the lines on the board
        pygame.draw.line(screen, (0, 0, 0), (0, h // 3), (w, h // 3))
        pygame.draw.line(screen, (0, 0, 0), (0, 2 * h // 3), (w, 2 * h // 3))
        pygame.draw.line(screen, (0, 0, 0), (w // 3, 0), (w // 3, h))
        pygame.draw.line(screen, (0, 0, 0), (2 * w // 3, 0), (2 * w // 3, h))

        # Draw the markers
        font = pygame.font.SysFont('Calibri', 100)
        for x in range(3):
            for y in range(3):
                piece = font.render(
                    self.board_object(x, y),
                    True,
                    (0, 0, 0)
                )
                screen.blit(
                    piece,
                    (
                        (y + 0.5) * (w // 3) - 30,
                        (x + 0.5) * (h // 3) - 30
                    )
                )
        pygame.display.update()

    def copy(self) -> ConnectFourGameState:
        """Return a copy of self"""
        return ConnectFourGameState(self.n, self)


class ConnectFour(Game):
    """A subclass of Game implementing Connect Four.

    Instance Attributes:
        - player1: Stores the Player object representing the player playing as 'X'.
        - player2: Stores the Player object representing the player playing as 'O'.
    """
    # Private Instance Attributes
    #   - game_state: Stores the current game state
    _game_state: ConnectFourGameState

    def copy(self) -> ConnectFour:
        """Return a copy of self"""
        return ConnectFour(self.player1.copy(), self.player2.copy(), self._game_state.copy())