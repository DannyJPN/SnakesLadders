import random

# Constants for the game
GRID_SIZE = 10
CELL_SIZE = 60
NUM_SNAKES_MIN = 4
NUM_SNAKES_MAX = 10
NUM_LADDERS_MIN = 4
NUM_LADDERS_MAX = 10

# Colors
COMMON_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (0, 255, 255),  # Cyan
    (255, 192, 203),# Pink
    (128, 128, 128),# Gray
    (0, 128, 0),    # Dark Green
    (0, 0, 128),    # Navy
    (128, 128, 0),  # Olive
    (128, 0, 0),    # Maroon
    (0, 128, 128),  # Teal
    (192, 192, 192),# Silver
    (255, 20, 147)  # Deep Pink
]

def get_random_color():
    rand_choice = random.choice(COMMON_COLORS)
    COMMON_COLORS.remove(rand_choice)
    return rand_choice