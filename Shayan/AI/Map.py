from Model import *
from Model import Cell as ModelCell


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, obj):
        return isinstance(obj, Cell) and obj.x == self.x and obj.y == self.y

    def __ne__(self, obj):
        return not self.__eq__(obj)

    # handled mirror effect

    @staticmethod
    def normalize_mod_n(x: int, y: int):
        return (x + Grid.width) % Grid.width, (y + Grid.height) % Grid.height

    @staticmethod
    def normalize_direction(x: int, y: int):
        x, y = Cell.normalize_mod_n(x, y)
        if x == Grid.width-1:
            x = -1
        if y == Grid.height-1:
            y = -1
        return x, y

    def go_to(self, direction: Direction):
        delta_x, delta_y = get_direction_delta(direction)
        ret = (self.x + delta_x, self.y + delta_y)
        return Cell(*Cell.normalize_mod_n(*ret))

    def delta_to(self, cell):
        return Cell.normalize_direction(cell.x - self.x, cell.y - self.y)

    def direction_to(self, cell):
        return get_direction_by_delta(self.delta_to(cell))


class Grid:
    width = None
    height = None

    def __init__(self, game):
        Grid.width = game.mapWidth
        Grid.height = game.mapHeight
        self.model_cell = [[None] * Grid.height for i in range(Grid.width)]
        self.visited = [[False] * Grid.height for i in range(Grid.width)]

    def is_visited(self, cell):
        return self.visited[cell.x][cell.y]

    def see_cell(self, cell: ModelCell):
        if cell is not None:
            if self.model_cell[cell.x][cell.y] is None:
                print("see this cell for first time", cell.x, cell.y, cell.type, cell.resource_type, cell.resource_value)
            self.model_cell[cell.x][cell.y] = cell
            if self.is_wall(Cell(cell.x, cell.y)):
                print("it was wall!")

    def visit_cell(self, cell: Cell):
        self.visited[cell.x][cell.y] = True

    def is_wall(self, cell: Cell):
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            return remembered.type == CellType.WALL.value

    def print_all_we_know_from_map(self):
        for i in range(Grid.width):
            arr = []
            for j in range(Grid.height):
                arr.append(self.is_wall(Cell(i, j)))
            print(*arr)


DIRECTIONS = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.CENTER]


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
