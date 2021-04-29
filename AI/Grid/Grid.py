import Model
from typing import List
from math import log2
from Model import CellType, ResourceType, Cell as ModelCell
from .Cell import DIRECTIONS, Cell
from AI.Algorithms import Graph
from AI.ChatBox import BaseNews, ViewCell, ViewOppBase, ViewScorpion, ViewResource, FightZone, SafeDangerCell, ImAlive
from .sync_information import see_cell, view_opp_base, view_scorpion, see_resource, view_fight, view_safe_danger_cell, see_alive_ant
from AI.Config import Config
from AI.ChatBox import ChatBoxWriter, ChatBoxReader


class Grid:
    initial_vertex_weight = 1
    infinity_danger = 100000

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
        # this probably has some bugs. when there are plenty of things with different update time

        self.scorpion_danger = Grid.new_2d_array_of(0)
        self.fight = Grid.new_2d_array_of(0)
        self.crowded = Grid.new_2d_array_of(0)
        self.total_danger = Grid.new_2d_array_of(0)

        self.known_graph = Graph()
        self.unknown_graph = Graph()
        self.simple_graph = Graph()
        self.trap_graph = Graph()
        self.base_trap_graph = Graph()

        self.initialize_graphs()
        self.chat_box_writer: ChatBoxWriter = ChatBoxWriter()
        self.chat_box_reader: ChatBoxReader = ChatBoxReader()

        self.saved_expected_opponent_base = None
        self.opponent_base_reports = []  # there is no function to return this. and it's type is ModelCell

        self.alive_worker_reports = {}
        self.alive_attacker_reports = {}

        self.hate_known = 0  # this will only change known graph
        self.opponent_base_fear = 1
        self.fight_fear = 0
        self.scorpion_fear = 0

        # self.scorpion_fear = 1
        # self.scorpion_fear_forgetting_rate = 0.8
        #
        # self.damaged_cell_fear = 1
        # self.damaged_cell_fear_forgetting_rate = 0.6
        # use this later on

        # change this before!!! every round

    def set_coffs(self, hate_known=0, opponent_base_fear=1, fight_fear=0, scorpion_fear=0):
        self.hate_known = hate_known
        self.opponent_base_fear = opponent_base_fear
        self.fight_fear = fight_fear
        self.scorpion_fear = scorpion_fear

    def update_with_news(self, base_news: BaseNews, is_from_chat_box=True, update_chat_box=False):
        base_news.turn = self.chat_box_reader.get_now_turn()
        # print(type(base_news))
        if type(base_news) == ImAlive:
            see_alive_ant(self, base_news, is_from_chat_box=is_from_chat_box, update_chat_box=update_chat_box)
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
        for news in self.chat_box_reader.get_latest_news(ViewCell):
            self.update_with_news(news, update_chat_box=False, is_from_chat_box=True)
        for _news_type in BaseNews.__subclasses__():
            for news in self.chat_box_reader.get_latest_news(_news_type):
                self.update_with_news(news, update_chat_box=False, is_from_chat_box=True)

    def prepare_graph_vertex(self, graph, cell, extra_add=0, danger_cof=1):
        swamp_cof = Config.swamp_stay if self.is_swamp(cell) else 1
        graph.change_vertex_weight(cell, (Grid.initial_vertex_weight + danger_cof * self.total_danger[cell.x][cell.y] + extra_add) * swamp_cof)

    def pre_calculations(self, now: Cell):
        self.saved_expected_opponent_base = self.calculate_expected_opponent_base()

        expected_base = self.expected_opponent_base()
        for cell in Grid.get_all_cells():
            base_danger = 0
            dis = expected_base.manhattan_distance(cell)
            if self.sure_opponent_base():
                if dis <= Config.base_range:
                    base_danger = Grid.infinity_danger
            else:
                if dis <= Config.base_range + 2:
                    base_danger += 120 - dis * 8
                elif dis <= Config.base_range + 5:
                    base_danger += 88 - dis * 8
            self.total_danger[cell.x][cell.y] = (self.opponent_base_fear * base_danger +
                                                 self.scorpion_fear * self.scorpion_danger[cell.x][cell.y] +
                                                 self.fight_fear * self.fight[cell.x][cell.y])
            self.prepare_graph_vertex(self.known_graph, cell)
            hate_cof = 0 if self.is_unknown(cell) else self.hate_known
            self.prepare_graph_vertex(self.unknown_graph, cell, extra_add=hate_cof)
            self.prepare_graph_vertex(self.simple_graph, cell, danger_cof=0)
            if self.is_trap(cell):
                self.prepare_graph_vertex(self.trap_graph, cell, extra_add=Config.map_width + Config.map_height)
            else:
                self.prepare_graph_vertex(self.trap_graph, cell, extra_add=0)
            self.prepare_graph_vertex(self.base_trap_graph, cell, extra_add=0)
            # bias this dangers todo
        self.unknown_graph.precalculate_source(now)
        self.known_graph.precalculate_source(now)
        self.simple_graph.precalculate_source(now)
        self.trap_graph.precalculate_source(now)
        self.base_trap_graph.precalculate_source(Cell(Config.base_x, Config.base_y))

    def update_vertex_in_graph(self, cell):
        if self.is_wall(cell):
            self.known_graph.delete_vertex(cell)
            self.unknown_graph.delete_vertex(cell)
            self.simple_graph.delete_vertex(cell)
            self.trap_graph.delete_vertex(cell)
            self.base_trap_graph.delete_vertex(cell)
            return
        if self.is_trap(cell):
            self.base_trap_graph.delete_vertex(cell)
        for direction in DIRECTIONS:
            self.update_edge_in_graph(cell, cell.go_to(direction))

    def update_edge_in_graph(self, cell1, cell2):
        if self.is_wall(cell1) or self.is_wall(cell2):
            return
        self.known_graph.add_edge(cell1, cell2)

    def initialize_graphs(self):
        for cell in Grid.get_all_cells():
            self.known_graph.add_vertex(cell, Grid.initial_vertex_weight)
            self.unknown_graph.add_vertex(cell, Grid.initial_vertex_weight)
            self.trap_graph.add_vertex(cell, Grid.initial_vertex_weight)
            self.simple_graph.add_vertex(cell, Grid.initial_vertex_weight)
            self.base_trap_graph.add_vertex(cell, Grid.initial_vertex_weight)
        for cell in Grid.get_all_cells():
            for direction in DIRECTIONS:
                self.unknown_graph.add_edge(cell, cell.go_to(direction))
                self.trap_graph.add_edge(cell, cell.go_to(direction))
                self.simple_graph.add_edge(cell, cell.go_to(direction))
                self.base_trap_graph.add_edge(cell, cell.go_to(direction))

    def is_wall(self, cell: Cell):
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            return remembered.type == CellType.WALL.value

    def is_swamp(self, cell: Cell):
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            return remembered.type == CellType.SWAMP.value

    def is_trap(self, cell: Cell):
        remembered: ModelCell = self.model_cell[cell.x][cell.y]
        if remembered is not None:
            return remembered.type == CellType.TRAP.value

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
                return 2
            return remembered.resource_type
        return 2

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

    def get_total_danger(self, cell: Cell):
        return self.total_danger[cell.x][cell.y]

    # probably we want to change this function so that it does not include danger!
    def expected_distance(self, cell_start: Cell, cell_end: Cell):
        if not self.known_graph.no_path(cell_start, cell_end):
            return self.known_graph.get_shortest_distance(cell_start, cell_end)
        return 1000

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

        def distance_to_mirror(_cell: Cell):
            X = abs(mirror_of_our_base.x - _cell.x)
            Y = abs(mirror_of_our_base.y - _cell.y)
            return X + Y

        mirror_of_our_base = Cell(Config.map_width - 1 - Config.base_x, Config.map_height - 1 - Config.base_y)

        for cell in all_cells:
            if dp[cell.x][cell.y]:
                # I changed this
                if best_candid is None or distance_to_mirror(cell) < distance_to_mirror(best_candid):
                    best_candid = cell

        return best_candid
        # this is stupid now. we don't consider base reports and also we may have several candidates.
        # taking average doesnt work here. fix this todo

    def report_opponent_base(self, cell: Cell):
        if cell in self.opponent_base_reports:
            return
        assert len(self.opponent_base_reports) == 0
        self.opponent_base_reports.append(cell)

    def report_worker_alive(self, ant_id, turn):
        assert ant_id is not None
        assert turn is not None
        self.alive_worker_reports[ant_id] = turn

    def report_attacker_alive(self, ant_id, turn):
        assert ant_id is not None
        assert turn is not None
        self.alive_attacker_reports[ant_id] = turn

    def alive_worker_count(self):
        ret = 0
        for ant_id in self.alive_worker_reports:
            if self.chat_box_reader.get_now_turn() - self.alive_worker_reports[ant_id] <= Config.PingRate + 4:
                ret += 1
        return ret

    def alive_attacker_count(self):
        ret = 0
        for ant_id in self.alive_attacker_reports:
            if self.chat_box_reader.get_now_turn() - self.alive_attacker_reports[ant_id] <= Config.PingRate + 4:
                ret += 1
        return ret

    def sure_opponent_base(self):
        return len(self.opponent_base_reports) == 1

    def add_scorpion_danger(self, start_cell: Cell, starting_danger, reduction_ratio, steps): # it is linear
        for dx in range(-steps, steps+1):
            for dy in range(-steps, steps+1):
                dis = abs(dx) + abs(dy)
                if dis <= steps:
                    new_cell = start_cell.move_to(dx, dy)
                    self.scorpion_danger[new_cell.x][new_cell.y] += int(starting_danger - dis * reduction_ratio)

    def divide_scorpion_danger(self, start_cell: Cell, division, steps):
        for dx in range(-steps, steps+1):
            for dy in range(-steps, steps+1):
                dis = abs(dx) + abs(dy)
                if dis <= steps:
                    new_cell = start_cell.move_to(dx, dy)
                    self.scorpion_danger[new_cell.x][new_cell.y] //= division

    def rebuild_fight(self):
        self.fight = Grid.new_2d_array_of(0)
        avg_dis = (Config.map_width + Config.map_height) // 3
        for new in self.chat_box_reader.get_all_news(FightZone):
            turn_dif = self.chat_box_reader.get_now_turn() - new.turn
            if(avg_dis <= turn_dif): # it was long time ago
                continue
            self.add_fight(new.cell, log2(avg_dis - turn_dif), log2(avg_dis - turn_dif) / 4, 2)
            # self.add_fight(new.cell, 20 * ((avg_dis - turn_dif) / avg_dis), 10 * ((avg_dis - turn_dif) / avg_dis), 1)

    def report_crowded(self, cell: Cell):
        self.crowded[cell.x][cell.y] += 1

    def get_crowded(self, cell: Cell):
        return self.crowded[cell.x][cell.y]

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
                assert False
            return colorful_print("E", OKCYAN)

        # you should rotate and then print
        print("map: ")
        for j in range(Config.map_height):
            arr = [colorful_cell(Cell(i, j)) for i in range(Config.map_width)]
            print(*arr)
        print("danger: ")
        for j in range(Config.map_height):
            arr = [self.total_danger[i][j] for i in range(Config.map_width)]
            print(*arr)
        print("fight zone: ")
        for j in range(Config.map_height):
            arr = [self.fight[i][j] for i in range(Config.map_width)]
            print(*arr)
        print("crowded: ")
        for j in range(Config.map_height):
            arr = [self.crowded[i][j] for i in range(Config.map_width)]
            print(*arr)
