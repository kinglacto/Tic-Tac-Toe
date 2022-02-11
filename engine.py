import random

class Engine:
    def __init__(self, board=None, turn=None) -> None:
        self.board = [[0 for _ in range(3)] for __ in range(3)] if board is None else board
        self.turn = 1 if turn is None else turn
        self.num_of_moves = 0

    def reset(self) -> None:
        self.board = [[0 for _ in range(3)] for __ in range(3)]
        self.turn = 1
        self.num_of_moves = 0

    def is_draw(self) -> bool:
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return False
        return True

    def check_for_winner(self) -> int:
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                return self.board[i][0]
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
                return self.board[0][i]
            elif self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
                return self.board[0][0]
            elif self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
                return self.board[0][2]
        return 0

    def make_move(self, cord) -> bool:
        if self.board[cord[0]][cord[1]] == 0:
            self.board[cord[0]][cord[1]] = self.turn
            self.turn *= -1
            self.num_of_moves += 1
            return True
        return False

    def get_best_move(self) -> tuple:
        self.opponent = self.turn * -1
        if self.num_of_moves == 0:
            return random.choice([(0, 0), (0, 2), (2, 0), (2, 0)])
        if self.num_of_moves == 1:
            if self.board[1][1] == self.opponent:
                return random.choice([(0, 0), (0, 2), (2, 0), (2, 0)])
            elif self.opponent in (self.board[0][0], self.board[0][2], self.board[2][0], self.board[2][0]):
                return (1, 1)

        return self.minimax(True)[1]

    def minimax(self, is_maximising) -> tuple:
        if self.check_for_winner() == self.turn:
            return 10, None
        elif self.check_for_winner() == self.opponent:
            return -10, None
        elif self.is_draw():
            return 0, None

        if is_maximising:
            best_score = -1
            best_move = None
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == 0:
                        self.board[i][j] = self.turn
                        score = self.minimax(False)[0]
                        self.board[i][j] = 0
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
            return best_score, best_move

        else:
            best_score = 1
            best_move = None
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == 0:
                        self.board[i][j] = self.opponent
                        score = self.minimax(True)[0]
                        self.board[i][j] = 0
                        if score < best_score:
                            best_score = score
                            best_move = (i, j)
            return best_score, best_move