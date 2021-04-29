import Model
from AI.Movement import *
from .MovementStrategy import MovementStrategy
from Model import CellType, ResourceType
from AI.Grid import Grid, Cell
from AI.BaseAnt import BaseAnt, Config
from AI import Choosing
from Utils.decorators import once_per_turn
from copy import deepcopy


class GrabAndReturn(MovementStrategy):
    def __init__(self, base_ant):
        super(GrabAndReturn, self).__init__(base_ant)
        self.best_cell = None
        self.prev_best_cell_value = None

    @once_per_turn
    def get_direction(self):
        # print("We are choosing direction. we have resource: ", self.base_ant.game.ant.currentResource.value)
        # shayad bad nabashe ye vaghta tama kone bishtar biare
        if Cell(self.base_ant.game.baseX, self.base_ant.game.baseY) == self.base_ant.get_now_pos_cell():
            self.best_cell = None

        # todo: shayad hamoon 0.5 kafi bashe ke bargardim!
        if self.base_ant.game.ant.currentResource.value >= Config.ant_max_rec_amount:
            return self.go_to_base()
        if self.base_ant.game.ant.currentResource.value and not self.has_close_resource():
            return self.go_to_base()
        return self.go_grab_resource()

    @once_per_turn
    def get_scores(self):
        # what if candidates are empty todo
        my_resource = self.base_ant.game.ant.currentResource
        if self.best_cell is not None:
            if self.get_base_cell() == self.get_now_pos_cell():
                self.best_cell = None
            elif self.base_ant.grid.get_cell_resource_value(self.best_cell) < self.prev_best_cell_value:
                self.best_cell = None
            elif my_resource.value > 0 and my_resource.type != self.base_ant.grid.get_cell_resource_type(self.best_cell):
                self.best_cell = None
            elif self.best_cell == self.get_now_pos_cell():
                self.best_cell = None
            elif self.grid.unknown_graph.no_path(self.get_now_pos_cell(), self.best_cell):
                self.best_cell = None
            elif self.grid.base_trap_graph.no_path(self.get_base_cell(), self.best_cell):
                self.best_cell = None

        # also forget it if someone has grabbed it beforehand. is it good? todo

        print("prev best cell is: ", self.best_cell)

        current_position = self.get_now_pos_cell()
        candidates = {}
        for cell in Grid.get_all_cells():
            if self.grid.unknown_graph.no_path(current_position, cell):
                continue
            if self.grid.base_trap_graph.no_path(self.get_base_cell(), cell):
                continue
            if self.grid.is_unknown(cell):
                continue
            if self.grid.get_cell_resource_value(cell) <= 0:
                continue
            if my_resource.value > 0 and my_resource.type != self.grid.get_cell_resource_type(cell):
                continue
            score = 0
            if (my_resource.value <= 0 or my_resource.type == ResourceType.GRASS.value) and \
                    self.grid.get_cell_resource_type(cell) == ResourceType.GRASS.value:
                score = min(self.grid.alive_worker_count() * Config.ant_max_rec_amount,
                            self.grid.get_cell_resource_value(cell)) * self.grass_importance()
            if (my_resource.value <= 0 or my_resource.type == ResourceType.BREAD.value) and \
                    self.grid.get_cell_resource_type(cell) == ResourceType.BREAD.value:
                score = min(self.grid.alive_worker_count() * Config.ant_max_rec_amount,
                            self.grid.get_cell_resource_value(cell)) * self.bread_importance()
            if self.grid.known_graph.no_path(current_position, cell):
                distance = self.grid.unknown_graph.get_shortest_distance(current_position, cell)
            else:
                distance = self.grid.known_graph.get_shortest_distance(current_position, cell)
            # change this todo
            # print("semi score is", score)
            score -= self.distance_importance() * distance
            # this should be base distance! todo

            print("importance bread/grass is: ", self.bread_importance(), self.grass_importance())
            print("CANDIDATE: ", cell, score, distance)

            if cell == self.best_cell:
                score += self.best_cell_importance()
                # change this todo
            # boro be samti ke expected score et max she todo
            # ba in taabee momken nist dore khodemoon bekharkhim?
            print("final score: ", score)
            candidates[cell] = score
        return candidates

    @once_per_turn
    def has_close_resource(self):
        my_resource = self.base_ant.game.ant.currentResource
        current_position = self.get_now_pos_cell()
        for cell in Grid.get_all_cells():
            if self.grid.unknown_graph.no_path(current_position, cell):
                continue
            if self.grid.base_trap_graph.no_path(self.get_base_cell(), cell):
                continue
            if self.grid.is_unknown(cell) or self.grid.get_cell_resource_value(cell) <= 0:
                continue
            if my_resource.value > 0 and my_resource.type != self.grid.get_cell_resource_type(cell):
                continue
            if current_position.manhattan_distance(cell) > max(3, self.grid.expected_distance(current_position, self.get_base_cell()) / 2.5):
                continue

            if (my_resource.value <= 0 or my_resource.type == ResourceType.GRASS.value) and \
                    self.grid.get_cell_resource_type(cell) == ResourceType.GRASS.value:
                return True

            if (my_resource.value <= 0 or my_resource.type == ResourceType.BREAD.value) and \
                    self.grid.get_cell_resource_type(cell) == ResourceType.BREAD.value:
                return True
        return False

    @once_per_turn
    def is_not_good(self):
        if self.base_ant.game.ant.currentResource.value > 0:
            return False
        candidates = self.get_scores()
        # print("there is not any resource near here so we are changing strategy!")
        if len(candidates) == 0:
            return True
        # other stuff todo
        return False

    @once_per_turn
    def is_really_good(self):
        # print("RUNNING IS REALLY GOOD")
        candidates = self.get_scores()
        if len(candidates) == 0:
            return False
        return True
    # change this todo

    @once_per_turn
    def get_best_cell(self):
        candidates = self.get_scores()
        # print("candids for grabbing are: ", "\n".join([f"{x}: {candidates[x]}" for x in candidates]))
        self.best_cell = Choosing.soft_max_choose(candidates)
        self.prev_best_cell_value = self.base_ant.grid.get_cell_resource_value(self.best_cell)
        # print(self.grid.base_trap_graph.no_path(self.get_base_cell(), self.best_cell))
        print("best cell is: ", self.best_cell)
        return self.best_cell

    def activate_resource(self, resource_type, graph):
        for cell in Grid.get_all_cells():
            if self.grid.get_cell_resource_type(cell) == resource_type:
                graph.get_vertex(cell).activate()

    def deactivate_resource(self, resource_type, graph):
        for cell in Grid.get_all_cells():
            if self.grid.get_cell_resource_type(cell) == resource_type:
                graph.get_vertex(cell).deactivate()

    def go_grab_resource(self):
        now_cell = self.get_now_pos_cell()
        best_cell: Cell = self.get_best_cell()
        my_resource = self.base_ant.game.ant.currentResource
        my_graph = self.grid.trap_graph if my_resource.value > 0 else self.grid.unknown_graph
        next_cell = self.go_to(best_cell, graph=my_graph)
        # if self.grid.get_cell_resource_value(best_cell) <= 0:
        #     return next_cell
        # distance = self.grid.unknown_graph.get_shortest_distance(now_cell, best_cell)
        # resource_type = self.grid.get_cell_resource_type(best_cell)
        # self.deactivate_resource(1 - resource_type)
        # self.grid.known_graph.precalculate_source(now_cell)
        # if self.grid.unknown_graph.get_shortest_distance(now_cell, best_cell) <= distance:
        #     next_cell = self.go_to(best_cell, graph=my_graph)
        # self.activate_resource(1 - resource_type)
        return next_cell
        # after this function distances are not right anymore!

    def go_to_base(self):
        # PATH = self.grid.trap_graph.get_shortest_path(self.get_now_pos_cell(), self.get_base_cell())
        # print("we want to go back to base. path is: ")
        #for cell in PATH:
        #    print(cell, self.grid.trap_graph.get_vertex(cell).get_weight())
        return self.go_to(self.get_base_cell(), graph=self.grid.trap_graph)

    def best_cell_importance(self):
        return 10

    def distance_importance(self):
        return 20

    @once_per_turn
    def bread_grass_coefficient(self):
        alive_workers = self.grid.alive_worker_count()
        alive_attackers = self.grid.alive_attacker_count()
        print("alive workers/attackers are: ", alive_workers, alive_attackers)
        grasses_per_turn = 0
        breads_per_turn = 0
        visible_grass = 0
        for cell in Grid.get_all_cells():
            if self.grid.unknown_graph.no_path(self.get_now_pos_cell(), cell):
                continue
            if self.grid.base_trap_graph.no_path(self.get_base_cell(), cell):
                continue
            dist = cell.manhattan_distance(self.get_base_cell())
            if self.grid.get_cell_resource_type(cell) == Model.ResourceType.GRASS.value:
                val = self.grid.get_cell_resource_value(cell)
                visible_grass += val
                grasses_per_turn += val / (2 * dist)
            elif self.grid.get_cell_resource_type(cell) == Model.ResourceType.BREAD.value:
                breads_per_turn += self.grid.get_cell_resource_value(cell) / (2 * dist)
        if alive_workers * Config.ant_max_rec_amount >= visible_grass:
            return 0.2, 0.8
        if alive_workers >= 15:
            return 0.2, 0.8
        if alive_attackers >= 3 * alive_workers:
            return 0.7, 0.3
        g = (alive_workers * Config.ant_max_rec_amount) / min(visible_grass, Config.get_limit_of_grass_in_turn(self.grid.chat_box_reader.get_now_turn()))
        # print("calculating ", alive_workers, Config.ant_max_rec_amount, visible_grass)
        return 1-g, g

    def grass_importance(self):
        return self.bread_grass_coefficient()[1] * 4.5

    def bread_importance(self):
        return self.bread_grass_coefficient()[0] * 4.5
    # this *3 is for compatibility with previous code

    def change_grid_coffs(self):
        self.grid.set_coffs(hate_known=3, opponent_base_fear=5)
