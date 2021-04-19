import Model
from typing import List
from Model import CellType, ResourceType, Cell as ModelCell
from .Cell import DIRECTIONS, Cell
from AI.Algorithms import Graph
from AI.ChatBox import BaseNews, ViewCell, ViewOppBase, ViewScorpion, ViewResource, FightZone, SafeDangerCell
from .sync_information import see_cell, view_opp_base, view_scorpion, see_resource, view_fight, view_safe_danger_cell
from AI.Config import Config
from AI.ChatBox import ChatBoxWriter, ChatBoxReader


class Grid:
    initial_vertex_weight = 1

    @staticmethod
    def get_all_cells():
        res = []
        for x in range(Config.map_width):
            for y in range(Config.map_height):
                res.append(Cell(x, y))
        return res

    @staticmethod
    def new_2d_array_of(val):
        return [[val] * Config.map_height for i in range(Config.map_width)]

    def __init__(self):
        self.model_cell = Grid.new_2d_array_of(None)
        self.last_update = Grid.new_2d_array_of(-1)
        # this probably has some bugs. when there are plenty of things with different update time

        self.danger = Grid.new_2d_array_of(0)
        self.fight = Grid.new_2d_array_of(0)

        self.known_graph = Graph()
        # self.unknown_graph = Graph()
        self.initialize_graphs()
        self.chat_box_writer: ChatBoxWriter = ChatBoxWriter()
        self.chat_box_reader: ChatBoxReader = ChatBoxReader()

        self.saved_expected_opponent_base = None
        self.opponent_base_reports = []  # there is no function to return this. and it's type is ModelCell

    def update_with_news(self, base_news: BaseNews, is_from_chat_box=True, update_chat_box=False):
        # print(type(base_news))
        if type(base_news) == ViewCell:
            # if update_chat_box is False:
            # print("WE SEE CELL In ChatBox", base_news.get_cell().x, base_news.get_cell().y)
            see_cell(self, base_news, is_from_chat_box=is_from_chat_box, update_chat_box=update_chat_box)
        if type(base_news) == ViewOppBase:
            view_opp_base(self, base_news, is_from_chat_box=is_from_chat_box, update_chat_box=update_chat_box)
        if type(base_news) == ViewScorpion:
            view_scorpion(self, base_news, is_from_chat_box=is_from_chat_box, update_chat_box=update_chat_box)
        if type(base_news) == ViewResource:
            see_resource(self, base_news, is_from_chat_box=is_from_chat_box, update_chat_box=update_chat_box)
        if type(base_news) is FightZone:
            view_fight(self, base_news, is_from_chat_box=is_from_chat_box, update_chat_box=update_chat_box)
        if type(base_news) is SafeDangerCell:
            view_safe_danger_cell(self, base_news, is_from_chat_box=is_from_chat_box, update_chat_box=update_chat_box)
        # add other types of messages todo

    def listen_to_chat_box(self):
        for _news_type in BaseNews.__subclasses__():
            for news in self.chat_box_reader.get_all_news(ViewCell):
                self.update_with_news(news, update_chat_box=False, is_from_chat_box=True)

    def pre_calculations(self, now: Cell):
        self.saved_expected_opponent_base = self.calculate_expected_opponent_base()

        expected_base = self.expected_opponent_base()
        print("We think their base is at: ", expected_base)
        for cell in Grid.get_all_cells():
            my_danger = Grid.initial_vertex_weight + self.danger[cell.x][cell.y]
            dis = expected_base.manhattan_distance(cell)
            if dis <= Config.base_range + 2:
                my_danger += 120 - dis * 8
                # change this todo
            elif dis <= Config.base_range + 5:
                my_danger += 88 - dis * 8
            self.known_graph.change_vertex_weight(cell, my_danger)
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
            self.known_graph.add_vertex(cell, Grid.initial_vertex_weight)
            # self.unknown_graph.add_vertex(cell, Grid.initial_vertex_weight)
        """
        for cell in Grid.get_all_cells():
            cell = Cell(i, j)
            for direction in DIRECTIONS:
                self.unknown_graph.add_edge(cell, cell.go_to(direction))
        """

    # todo is there a case were cell is not None but .type is None?
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
                return 0
            return max(0, remembered.resource_value)
        return 0

    def get_cell_resource_type(self, cell: Cell):
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            if remembered.resource_type is None \
                    or remembered.resource_value is None or remembered.resource_value <= 0:
                return -1
            return remembered.resource_type
        return -1

    def get_cell_ants(self, cell: Cell) -> List[Model.Ant]:
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            return remembered.ants

    def get_near_cell_ants(self, cell: Cell, distance: int) -> List[Model.Ant]:
        ants = []
        for dx in range(-distance, distance+1):
            for dy in range(-distance, distance+1):
                if abs(dx) + abs(dy) <= distance:
                    ants += self.get_cell_ants(cell.move_to(dx, dy))
        return ants

    def get_empty_adjacents(self, cell: Cell):
        result = []
        for direction in DIRECTIONS:
            if not self.is_wall(cell.go_to(direction)):
                result.append(cell.go_to(direction))
        return result

    def activate(self, resource_type):
        for cell in self.get_all_cells():
            if self.get_cell_resource_type(cell) == resource_type:
                self.known_graph.get_vertex(cell).activate()

    def deactivate(self, resource_type):
        for cell in self.get_all_cells():
            if self.get_cell_resource_type(cell) == resource_type:
                self.known_graph.get_vertex(cell).deactivate()

    # probably we want to change this function so that it does not include danger!
    def expected_distance(self, cell_start: Cell, cell_end: Cell):
        if not self.known_graph.no_path(cell_start, cell_end):
            return self.known_graph.get_shortest_distance(cell_start, cell_end)
        # if not self.unknown_graph.no_path(cell_start, cell_end):
        #    return int(self.unknown_graph.get_shortest_distance(cell_start, cell_end) * 1.5) + 5  # what the hell?!
        return 1000  # inf # is this enough?

    def expected_opponent_base(self):
        return self.saved_expected_opponent_base

    def calculate_expected_opponent_base(self):
        if len(self.opponent_base_reports) > 0:
            assert len(self.opponent_base_reports) == 1
            return self.opponent_base_reports[0]
        dp = Grid.new_2d_array_of(False)
        all_cells = Grid.get_all_cells()
        for cell in all_cells:
            dp[cell.x][cell.y] = self.is_unknown(cell)
        while True:
            store = dp
            dp = Grid.new_2d_array_of(False)
            candid = None
            for cell in all_cells:
                dp[cell.x][cell.y] = True
                for direction in DIRECTIONS:
                    new_cell = cell.go_to(direction)
                    dp[cell.x][cell.y] = dp[cell.x][cell.y] and store[new_cell.x][new_cell.y]
                if dp[cell.x][cell.y]:
                    candid = cell
            if candid is None:
                dp = store
                break
        best_candid = None

        def our_base_distance(_cell: Cell):
            return _cell.manhattan_distance(Cell(Config.base_x, Config.base_y))

        for cell in all_cells:
            if dp[cell.x][cell.y]:
                if best_candid is None or our_base_distance(cell) > our_base_distance(best_candid):
                    best_candid = cell

        return best_candid
        # this is stupid now. we don't consider base reports and also we may have several candidates.
        # taking average doesnt work here. fix this todo

    def report_opponent_base(self, cell: Cell):
        if cell in self.opponent_base_reports:
            return
        assert len(self.opponent_base_reports) == 1
        self.opponent_base_reports.append(cell)

    def add_danger(self, start_cell: Cell, starting_danger, reduction_ratio, steps): # it is linear
        for dx in range(-steps, steps+1):
            for dy in range(-steps, steps+1):
                dis = abs(dx) + abs(dy)
                if dis <= steps:
                    new_cell = start_cell.move_to(dx, dy)
                    self.danger[new_cell.x][new_cell.y] += int(starting_danger - dis * reduction_ratio)

    def divide_danger(self, start_cell: Cell, division, steps):
        for dx in range(-steps, steps+1):
            for dy in range(-steps, steps+1):
                dis = abs(dx) + abs(dy)
                if dis <= steps:
                    new_cell = start_cell.move_to(dx, dy)
                    self.danger[new_cell.x][new_cell.y] //= division

    def rebuild_fight(self):
        self.fight = [[0] * Config.map_height for i in range(Config.map_width)]
        avg_dis = (Config.map_width + Config.map_height) // 2
        for new in self.chat_box_reader.get_all_news(FightZone):
            turn_dif = self.chat_box_reader.get_now_turn() - new.turn
            if(avg_dis <= turn_dif): # it was long time ago
                continue

            self.add_fight(new.cell, 20 * ((avg_dis - turn_dif) / avg_dis), 10 * ((avg_dis - turn_dif) / avg_dis), 1)

    def add_fight(self, start_cell: Cell, starting_fight, reduction_ratio, steps): # it is linear
        for dx in range(-steps, steps+1):
            for dy in range(-steps, steps+1):
                dis = abs(dx) + abs(dy)
                if dis <= steps:
                    new_cell = start_cell.move_to(dx, dy)
                    self.fight[new_cell.x][new_cell.y] += int(starting_fight - dis * reduction_ratio)

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
            if Config.now_x == cell.x and Config.now_y == cell.y:
                return colorful_print("X", OKBLUE)
            if self.is_wall(cell):
                return colorful_print("W", WARNING)
            if self.is_unknown(cell):
                return "?"
            if self.get_cell_resource_value(cell) > 0:
                if self.get_cell_resource_type(cell) == ResourceType.GRASS.value:
                    return colorful_print("G", OKGREEN)
                if self.get_cell_resource_type(cell) == ResourceType.BREAD.value:
                    return colorful_print("B", OKGREEN)
                # print(colorful_print(FAIL, "SHIT SHIT SHIT SHIT ANOTHER TYPE"), self.get_cell_resource_value(cell), self.get_cell_resource_type(cell), ResourceType.GRASS, ResourceType.BREAD)
                assert False
            return colorful_print("E", OKCYAN)

        # you should rotate and then print
        print("map: ")
        for j in range(Config.map_height):
            arr = [colorful_cell(Cell(i, j)) for i in range(Config.map_width)]
            print(*arr)
        print("danger: ")
        for j in range(Config.map_height):
            arr = [self.danger[i][j] for i in range(Config.map_width)]
            print(*arr)
        print("fight zone: ")
        for j in range(Config.map_height):
            arr = [self.fight[i][j] for i in range(Config.map_width)]
            print(*arr)
