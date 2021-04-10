from Model import CellType, ResourceType, Cell as ModelCell
from .Cell import Cell, DIRECTIONS
from AI.Algorithms import Graph
from copy import deepcopy


# hell!
# time consuming?
def soft_max_choose(candidates):
    from math import exp
    from random import random
    total = 0
    for x in candidates:
        total += exp(candidates[x])
    rnd = random() * total
    for x in candidates:
        rnd -= exp(candidates[x])
        if rnd < 0:
            return x


class Grid:
    width = None
    height = None

    def __init__(self, game):
        Grid.width = game.mapWidth
        Grid.height = game.mapHeight
        Cell.width = game.mapWidth # tof
        Cell.height = game.mapHeight # tof
        self.model_cell = [[None] * Grid.height for i in range(Grid.width)]
        self.visited = [[False] * Grid.height for i in range(Grid.width)]
        self.known_graph = Graph()
        # self.unknown_graph = Graph()
        self.initialize_graphs()

    def is_visited(self, cell):
        return self.visited[cell.x][cell.y]

    def pre_calculations(self, now: Cell):
        # self.unknown_graph.precalculate_source(now)
        self.known_graph.precalculate_source(now)

    def update_vertex_in_graph(self, cell):
        if self.is_wall(cell):
            self.known_graph.delete_vertex(cell)
            # self.unknown_graph.delete_vertex(cell)
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
                # self.unknown_graph.add_vertex(cell, 1)
                """
        for i in range(Grid.width):
            for j in range(Grid.height):
                cell = Cell(i, j)
                for direction in DIRECTIONS:
                    self.unknown_graph.add_edge(cell, cell.go_to(direction))
                """

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
            return remembered.resource_value

    def get_cell_resource_type(self, cell: Cell):
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            return remembered.resource_type

    def is_unknown(self, cell: Cell):
        return self.model_cell[cell.x][cell.y] is None

    def expected_distance(self, cell_start: Cell, cell_end: Cell):
        if not self.known_graph.no_path(cell_start, cell_end):
            return self.known_graph.get_shortest_distance(cell_start, cell_end)
        # if not self.unknown_graph.no_path(cell_start, cell_end):
        #    return int(self.unknown_graph.get_shortest_distance(cell_start, cell_end) * 1.5) + 5  # what the hell?!
        return 1000  # inf

    def get_best_path(self, cell_start: Cell, cell_end: Cell):
        # nabayad chizaii ke midim be graph mutable bashe? age avazesh kone chi?
        if not self.known_graph.no_path(cell_start, cell_end):
            return self.known_graph.get_shortest_path(cell_start, cell_end)
        # if not self.unknown_graph.no_path(cell_start, cell_end):
        #    return self.unknown_graph.get_shortest_path(cell_start, cell_end)
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
                if not self.is_unknown(cell) and self.get_cell_resource_value(cell) <= 0: #  don't try to go to seen cells. also change this.
                    score = -1000  # inf
                # age manabe tamoom beshan va hame chiz ro dide bashim ina miterekan

                score -= 0.5 * self.expected_distance(current_position, cell)  # need to change  this
                # ba in taabee momken nist dore khodemoon bekharkhim?
                if best_cell is None or best_score < score:
                    best_cell = cell
                    best_score = score
                    print("HEY BETTER SCORE! ", best_cell, best_score, self.is_unknown(cell), self.get_cell_resource_value(cell))
        return best_cell, best_score

    def get_one_of_near_unknowns(self, current_position: Cell):
        candidates = {}
        for x in range(Grid.width):
            for y in range(Grid.height):
                cell = Cell(x, y)
                if self.is_unknown(cell):
                    distance = self.expected_distance(current_position, cell)
                    candidates[cell] = -distance
                    # age yeki az 1000 ha bardashte beshe badbakht mishim
                    if distance != 1000:
                        print("can go to ", cell, "distance is ", distance)
        return soft_max_choose(candidates)
