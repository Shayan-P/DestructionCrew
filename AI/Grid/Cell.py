import random

from Model import Direction
from AI.Config import Config


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, obj):
        return isinstance(obj, Cell) and obj.x == self.x and obj.y == self.y

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return hash((self.x, self.y))

    # handled mirror effect

    @staticmethod
    def normalize_mod_n(x: int, y: int):
        return (x + Config.map_width) % Config.map_width, (y + Config.map_height) % Config.map_height

    @staticmethod
    def normalize_direction(x: int, y: int):
        x, y = Cell.normalize_mod_n(x, y)
        if x == Config.map_width - 1:
            x = -1
        if y == Config.map_height - 1:
            y = -1
        return x, y

    @staticmethod
    def from_model_cell(model_cell):
        return Cell(model_cell.x, model_cell.y)

    def go_to(self, direction: Direction):
        delta_x, delta_y = get_direction_delta(direction)
        ret = (self.x + delta_x, self.y + delta_y)
        return Cell(*Cell.normalize_mod_n(*ret))

    def delta_to(self, cell):
        return Cell.normalize_direction(cell.x - self.x, cell.y - self.y)

    def move_to(self, x, y):
        return Cell(*Cell.normalize_mod_n(self.x + x, self.y + y))

    def direction_to(self, cell):
        return get_direction_by_delta(self.delta_to(cell))

    def manhattan_distance(self, cell):
        return min(abs(cell.x - self.x), Config.map_width) + min(abs(cell.y - self.y), Config.map_height)


DIRECTIONS = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.CENTER]


def get_random_directions():
    my_directions = DIRECTIONS.copy()
    random.shuffle(my_directions)
    return my_directions


def get_direction_delta(direction: Direction):
    if direction == Direction.UP:
        return 0, -1
    if direction == Direction.DOWN:
        return 0, 1
    if direction == Direction.RIGHT:
        return 1, 0
    if direction == Direction.LEFT:
        return -1, 0
    if direction == Direction.CENTER:
        return 0, 0


def get_direction_by_delta(delta: (int, int)):
    if delta == (0, -1):
        return Direction.UP
    if delta == (0, +1):
        return Direction.DOWN
    if delta == (+1, 0):
        return Direction.RIGHT
    if delta == (-1, 0):
        return Direction.LEFT
    if delta == (0, 0):
        return Direction.CENTER
