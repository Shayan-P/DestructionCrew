import random

from Model import *
from Model import Cell as ModelCell
from AI.Algorithms import Graph
from copy import deepcopy


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
        return (x + Grid.width) % Grid.width, (y + Grid.height) % Grid.height

    @staticmethod
    def normalize_direction(x: int, y: int):
        x, y = Cell.normalize_mod_n(x, y)
        if x == Grid.width - 1:
            x = -1
        if y == Grid.height - 1:
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
        self.known_graph = Graph()
        self.unknown_graph = Graph()
        self.initialize_graphs()

    def is_visited(self, cell):
        return self.visited[cell.x][cell.y]

    def pre_calculations(self, now: Cell):
        self.unknown_graph.precalculate_source(now)
        self.known_graph.precalculate_source(now)

    def update_vertex_in_graph(self, cell):
        if self.is_wall(cell):
            self.known_graph.delete_vertex(cell)
            self.unknown_graph.delete_vertex(cell)
            return
        for direction in DIRECTIONS:
            self.update_edge_in_graph(cell, cell.go_to(direction))

    def update_edge_in_graph(self, cell1, cell2):
        if self.is_wall(cell1) or self.is_wall(cell2):
            return
        self.known_graph.add_edge(cell1, cell2)

    def initialize_graphs(self):
        for i in range(Grid.width):
            for j in range(Grid.height):
                cell = Cell(i, j)
                self.known_graph.add_vertex(cell, 1)  # 1 or 0?
                self.unknown_graph.add_vertex(cell, 1)
        for i in range(Grid.width):
            for j in range(Grid.height):
                cell = Cell(i, j)
                for direction in DIRECTIONS:
                    self.unknown_graph.add_edge(cell, cell.go_to(direction))

    def see_cell(self, new_cell: ModelCell):
        if new_cell is not None:
            cell = Cell(new_cell.x, new_cell.y)
            self.model_cell[cell.x][cell.y] = deepcopy(new_cell)  # it should be deep copy
            self.update_vertex_in_graph(cell)

    def visit_cell(self, cell: Cell):
        self.visited[cell.x][cell.y] = True

    def is_wall(self, cell: Cell):
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            return remembered.type == CellType.WALL.value

    def get_cell_resource_value(self, cell: Cell):
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            return remembered.resource_type # inja ro khodeshoon bug zadan. bejaye resource type, value gozashtan

    def get_cell_resource_type(self, cell: Cell):
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            return remembered.resource_value  # momkene inam jabeja bashe?

    def is_unknown(self, cell: Cell):
        return self.model_cell[cell.x][cell.y] is None

    def expected_distance(self, cell_start: Cell, cell_end: Cell):
        if not self.known_graph.no_path(cell_start, cell_end):
            return self.known_graph.get_shortest_distance(cell_start, cell_end)
        if not self.unknown_graph.no_path(cell_start, cell_end):
            return int(self.unknown_graph.get_shortest_distance(cell_start, cell_end) * 1.5) + 5  # what the hell?!
        return 1000  # inf

    def get_best_path(self, cell_start: Cell, cell_end: Cell):
        if not self.known_graph.no_path(cell_start, cell_end):
            return self.known_graph.get_shortest_path(cell_start, cell_end)
        if not self.unknown_graph.no_path(cell_start, cell_end):
            return self.unknown_graph.get_shortest_path(cell_start, cell_end)
        return None

    def print_all_we_know_from_map(self):
        for i in range(Grid.width):
            arr = []
            for j in range(Grid.height):
                arr.append(self.is_wall(Cell(i, j)))
            print(*arr)

    def get_best_cell_score_with_resource(self, current_position: Cell):
        # score must be expected value
        best_cell = None
        best_score = -1

        for x in range(Grid.width):
            for y in range(Grid.height):
                cell = Cell(x, y)
                score = 0
                # dar yek khoone momkene do no manbaa bashan?
                if self.is_unknown(cell):
                    score = 0
                elif self.get_cell_resource_type(cell) == ResourceType.GRASS.value:
                    score = min(20, self.get_cell_resource_value(cell))  # in 20 avaz she
                elif self.get_cell_resource_type(cell) == ResourceType.BREAD.value:
                    score = min(20, self.get_cell_resource_value(cell))  # in 20 avaz she
                if not self.is_unknown(cell) and self.get_cell_resource_value(cell) <= 0:  #  don't try to go to seen cells. also change this.
                    score = -1000  # inf
                # age manabe tamoom beshan va hame chiz ro dide bashim ina miterekan

                score -= 0.5 * self.expected_distance(current_position, cell)  # need to change  this
                # ba in taabee momken nist dore khodemoon bekharkhim?
                if best_cell is None or best_score < score:
                    best_cell = cell
                    best_score = score
                    print("HEY BETTER SCORE! ", best_cell, best_score, self.is_unknown(cell), self.get_cell_resource_value(cell))
        return best_cell, best_score


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
