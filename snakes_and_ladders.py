#!E:\ProgramFiles\Programy\Python\Python311\python.exe

import random
import logging
import pygame
from constants import GRID_SIZE, NUM_SNAKES_MIN, NUM_SNAKES_MAX, NUM_LADDERS_MIN, NUM_LADDERS_MAX, get_random_color, COMMON_COLORS, RIGHT, LEFT

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("game.log"),
    logging.StreamHandler()
])

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.snakes = []
        self.ladders = []
        self.initialize_board()

    def initialize_board(self):
        num_snakes = random.randint(NUM_SNAKES_MIN, NUM_SNAKES_MAX)
        num_ladders = random.randint(NUM_LADDERS_MIN, NUM_LADDERS_MAX)

        for _ in range(num_snakes):
            self.add_snake()
            print(f"Adding snake {self.snakes[-1]}")

        for _ in range(num_ladders):
            self.add_ladder()
            print(f"Adding ladder {self.ladders[-1]}")

    def add_snake(self):
        while True:
            start_row = random.randint(1, GRID_SIZE - 2)
            start_col = random.randint(1, GRID_SIZE - 2)
            end_row = start_row + random.randint(1, 2)
            end_col = start_col + random.randint(-2, 3)
            if self.is_valid_snake_or_ladder(start_row, start_col, end_row, end_col):
                self.snakes.append(((start_row, start_col), (end_row, end_col)))
                break

    def add_ladder(self):
        while True:
            start_row = random.randint(1, GRID_SIZE - 2)
            start_col = random.randint(1, GRID_SIZE - 2)
            end_row = start_row - random.randint(1, 2)
            end_col = start_col + random.randint(-2, 3)
            if self.is_valid_snake_or_ladder(start_row, start_col, end_row, end_col):
                self.ladders.append(((start_row, start_col), (end_row, end_col)))
                break

    def is_valid_snake_or_ladder(self, start_row, start_col, end_row, end_col):
        if (not (0 < start_row < GRID_SIZE)) or (not (0 < start_col < GRID_SIZE)) or (not (0 < end_row < GRID_SIZE)) or (not (0 < end_col < GRID_SIZE)):
            return False
        if (start_row, start_col) == (end_row, end_col):
            return False
        for snake in self.snakes:
            if (start_row, start_col) == snake[0] or (end_row, end_col) == snake[1]:
                return False
        for ladder in self.ladders:
            if (start_row, start_col) == ladder[0] or (end_row, end_col) == ladder[1]:
                return False
        return True

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = (GRID_SIZE - 1, 0)
        self.direction = RIGHT
        self.logger = logging.getLogger(self.name)
        self.logger.info(f"{self.name} initialized at position {self.position}")

    def throw_dice(self):
        total_roll = 0
        while True:
            input(f"{self.name}, press Enter to roll the dice...")
            roll = random.randint(1, 6)
            self.logger.info(f"{self.name} rolled a {roll}")
            total_roll += roll
            if roll != 6:
                if total_roll >= 6:
                    self.logger.info(f"{self.name} total roll is {total_roll}")
                break
            else:
                self.logger.info(f"{self.name} ROLLS AGAIN")
        return total_roll

    def move(self, steps):
        if steps == 0:
            return

        if steps < 0:
            self.move_backward(abs(steps))
            return

        row, col = self.position
        old_position = self.position

        # Move one step in the current direction
        col += self.direction

        # Check if we need to move to the next row
        if col >= GRID_SIZE:
            col = GRID_SIZE - 1
            row -= 1
            self.swap_direction()
        elif col < 0:
            col = 0
            row -= 1
            self.swap_direction()

        self.position = (row, col)
        self.logger.info(f"{self.name} moved from {old_position} to {self.position}")

        # Recursive call with one less step
        self.move(steps - 1)

    def move_backward(self):
    

        row, col = self.position
        old_position = self.position

        # Move one step in the opposite direction
        col -= self.direction

        # Check if we need to move to the previous row
        if col >= GRID_SIZE:
            col = GRID_SIZE - 1
            row += 1
            self.swap_direction()
        elif col < 0:
            col = 0
            row += 1
            self.swap_direction()

        self.position = (row, col)
        self.logger.info(f"{self.name} moved backward from {old_position} to {self.position}")



    def swap_direction(self):
        if self.direction == RIGHT:
            self.direction = LEFT
        else:
            self.direction = RIGHT

    def check_snake_or_ladder(self, board):
        for start, end in board.snakes:
            if self.position == start:
                self.position = end
                self.logger.info(f"{self.name} hit a snake and moved to {self.position}")
                return
        for start, end in board.ladders:
            if self.position == start:
                self.position = end
                self.logger.info(f"{self.name} climbed a ladder and moved to {self.position}")

    def has_won(self):
        return self.position == (0, GRID_SIZE - 1)

class Game:
    def __init__(self, num_players):
        self.board = Board()
        self.players = [Player(f"Player {i+1}", get_random_color()) for i in range(num_players)]
        self.current_player_index = 0

    def start(self):
        logging.info("Game started")
        while True:
            player = self.players[self.current_player_index]
            roll = player.throw_dice()
            player.move(roll)
            player.check_snake_or_ladder(self.board)
            self.check_player_collision(player)
            if player.has_won():
                logging.info(f"{player.name} has won the game!")
                print(f"{player.name} has won the game!")
                break
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def check_player_collision(self, current_player):
        for player in self.players:
            if player != current_player and player.position == current_player.position:
                logging.info(f"Collision detected: {current_player.name} landed on {player.name}'s position. {player.name} moves back one step.")
                player.move_backward()
                player.check_snake_or_ladder(self.board)

def main():
    print("Welcome to Snakes and Ladders!")
    while True:
        try:
            num_players = int(input(f"Enter the number of players (2-{len(COMMON_COLORS)}): "))
            if 2 <= num_players <= len(COMMON_COLORS):
                break
            else:
                print(f"Please enter a number between 2 and {len(COMMON_COLORS)}.")
        except ValueError:
            print(f"Invalid input. Please enter a number between 2 and {len(COMMON_COLORS)}.")

    game = Game(num_players)
    game.start()

if __name__ == "__main__":
    main()