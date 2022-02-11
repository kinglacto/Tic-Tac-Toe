import pygame
import random
import sys
from engine import Engine

pygame.font.init()
engine = Engine()

class TicTacToe:
    def __init__(self) -> None:
        self.size = 300
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Tic-Tac-Toe")

        self.square_centers_list = [[(self.size//6 + (x * self.size//3), self.size//6 + (y * self.size//3)) for x in range(3)] for y in range(3)]
        self.squares_list = [[pygame.Rect(x * (self.size//3), y * (self.size//3), self.size//3, self.size//3) for x in range(3)] for y in range(3)]
        self.occupied_list = []

        self.font = pygame.font.SysFont("Arial", self.size//10)

        self.radius = self.size//6 - 20
        self.line_thickness = 3

        self.to_move = random.choice(("player", "computer"))

    def reset_screen(self) -> None:
        self.screen.fill("white")
        pygame.draw.line(self.screen, "black", (self.size//3, 0), (self.size//3, self.size), width=self.line_thickness)
        pygame.draw.line(self.screen, "black", (2 * (self.size//3), 0), (2 * (self.size//3), self.size), width=self.line_thickness)
        pygame.draw.line(self.screen, "black", (0, self.size//3), (self.size, self.size//3), width=self.line_thickness)
        pygame.draw.line(self.screen, "black", (0, 2 * (self.size//3)), (self.size, 2 * (self.size//self.line_thickness)), width=self.line_thickness)

    def draw_mark(self, center, cord) -> None:
        if engine.turn == 1:
            pygame.draw.circle(self.screen, "black", center, self.radius, width=self.line_thickness)
        else:
            pygame.draw.line(self.screen, "black", (center[0] - self.radius, center[1] - self.radius), (center[0] + self.radius, center[1] + self.radius), width=self.line_thickness)
            pygame.draw.line(self.screen, "black", (center[0] + self.radius, center[1] - self.radius), (center[0] - self.radius, center[1] + self.radius), width=self.line_thickness)
        self.occupied_list.append(cord)

    def should_end_game(self) -> None:
        is_draw = engine.is_draw()
        if (engine.check_for_winner() in (1, -1)) or is_draw:
            if is_draw:
                end_message = "Draw!"
            elif self.to_move == "player":
                end_message = "Computer Wins!"
            elif self.to_move == "computer":
                end_message = "Player Wins!"
                
            self.screen.blit(self.font.render(end_message, False, (0, 0, 0)), (10, 10))
            pygame.display.update()
            pygame.time.wait(1500)
            return True
        return False

    def clean_up(self) -> None:
        engine.reset() 
        self.reset_screen()
        self.to_move = random.choice(("player", "computer"))
        self.occupied_list = []
        pygame.display.update()

    def run(self) -> bool:
        self.reset_screen()
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.to_move == "player" and event.type == pygame.MOUSEBUTTONUP:
                    for i in range(3):
                        for j in range(3):
                            if self.squares_list[i][j].collidepoint(event.pos) and ((i, j) not in self.occupied_list):

                                if engine.make_move((i, j)):
                                    self.draw_mark(self.square_centers_list[i][j], (i, j))
                                    self.to_move = "computer"

                                    if self.should_end_game():
                                        self.clean_up()
                                        return True

                                    pygame.display.update()
                                    break
                
                if self.to_move == "computer":
                    i, j = engine.get_best_move()

                    engine.make_move((i, j))
                    self.draw_mark(self.square_centers_list[i][j], (i, j))
                    self.to_move = "player"

                    if self.should_end_game():
                        self.clean_up()
                        return True

                    pygame.display.update()

            pygame.time.wait(30)

if __name__ == "__main__":
    tictactoe = TicTacToe()
    while True:
        tictactoe.run()