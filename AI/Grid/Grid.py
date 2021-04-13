import Model
from typing import List
from Model import CellType, ResourceType, Cell as ModelCell
from .Cell import DIRECTIONS, Cell
from AI.Algorithms import Graph
from AI.ChatBox import BaseNews, ViewCell
from .sync_information import see_cell


class Grid:
    width = None
    height = None

    @staticmethod
    def get_all_cells():
        res = []
        for x in range(Grid.width):
            for y in range(Grid.height):
                res.append(Cell(x, y))
        return res

    def __init__(self, game):
        Grid.width = game.mapWidth
        Grid.height = game.mapHeight
        Cell.width = game.mapWidth # tof
        Cell.height = game.mapHeight # tof
        self.model_cell = [[None] * Grid.height for i in range(Grid.width)]
        self.known_graph = Graph()
        # self.unknown_graph = Graph()
        self.initialize_graphs()
        self.chat_box_writer = None
        self.chat_box_reader = None

    def update_with_news(self, base_news: BaseNews, update_chat_box=True):
        if type(base_news) == ViewCell:
            if update_chat_box is False:
                print("WE SEE CELL In ChatBox", base_news.get_cell().x, base_news.get_cell().y)
            see_cell(self, base_news.get_cell(), update_chat_box=update_chat_box)
        pass
        # todo add other news

    def pre_calculations(self, now: Cell):
        for news in self.chat_box_reader.get_all_news():
            self.update_with_news(news, update_chat_box=False)
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
        for cell in Grid.get_all_cells():
            self.known_graph.add_vertex(cell, 1)  # 1 or 0?
            # self.unknown_graph.add_vertex(cell, 1)
        """
        for cell in Grid.get_all_cells():
            cell = Cell(i, j)
            for direction in DIRECTIONS:
                self.unknown_graph.add_edge(cell, cell.go_to(direction))
        """

    # todo
    # behold that this functions may return None in case there is nothing in memory
    def is_wall(self, cell: Cell):
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            return remembered.type == CellType.WALL.value

    def is_unknown(self, cell: Cell):
        return self.model_cell[cell.x][cell.y] is None

    def get_cell_resource_value(self, cell: Cell):
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            if remembered.resource_value is None:
                return 0 # todo remove this
            return remembered.resource_value

    def get_cell_resource_type(self, cell: Cell):
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            if remembered.resource_type is None:
                return -1 # todo remove this
            return remembered.resource_type

    def get_cell_ants(self, cell: Cell) -> List[Model.Ant]:
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            return remembered.ants

    def expected_distance(self, cell_start: Cell, cell_end: Cell):
        if not self.known_graph.no_path(cell_start, cell_end):
            return self.known_graph.get_shortest_distance(cell_start, cell_end)
        # if not self.unknown_graph.no_path(cell_start, cell_end):
        #    return int(self.unknown_graph.get_shortest_distance(cell_start, cell_end) * 1.5) + 5  # what the hell?!
        return 1000  # inf

    def print_all_we_know_from_map(self):
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'

        def colorful_print(txt, clr):
            return str(clr) + str(txt) + ENDC

        def colorful_cell(cell):
            if self.is_wall(cell):
                return colorful_print("W", WARNING)
            if self.is_unknown(cell):
                return "?"
            if self.get_cell_resource_value(cell) > 0:
                if self.get_cell_resource_type(cell) == ResourceType.GRASS.value:
                    return colorful_print("G", OKGREEN)
                if self.get_cell_resource_type(cell) == ResourceType.BREAD.value:
                    return colorful_print("B", OKGREEN)
                print(colorful_print(FAIL, "SHIT SHIT SHIT SHIT ANOTHER TYPE"), self.get_cell_resource_value(cell), self.get_cell_resource_type(cell), ResourceType.GRASS, ResourceType.BREAD)
                assert False
            return colorful_print("E", OKCYAN)

        for i in range(Grid.width):
            arr = [colorful_cell(Cell(i, j)) for j in range(Grid.height)]
            print(*arr)
