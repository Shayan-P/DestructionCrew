from AI.Movement import *
from .MovementStrategy import MovementStrategy
from Model import CellType, ResourceType
from AI.Grid import Grid, Cell
from AI.BaseAnt import BaseAnt, Config
from AI import Choosing


class GrabAndReturn(MovementStrategy):
    def __init__(self, base_ant):
        super(GrabAndReturn, self).__init__(base_ant)
        self.best_cell = None
        self.prev_best_cell_value = None

    def get_direction(self):
        # print("We are choosing direction. we have resource: ", self.base_ant.game.ant.currentResource.value)
        # shayad bad nabashe ye vaghta tama kone bishtar biare
        if Cell(self.base_ant.game.baseX, self.base_ant.game.baseY) == self.base_ant.get_now_pos_cell():
            self.best_cell = None

        if self.base_ant.game.ant.currentResource.value >= Config.ant_max_rec_amount:
            return self.go_to_base()
        if self.base_ant.game.ant.currentResource.value >= 0.5 * Config.ant_max_rec_amount and not self.is_really_good():
            return self.go_to_base()
        return self.go_grab_resource()

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

        # also forget it if someone has grabbed it beforehand. is it good? todo

        current_position = self.get_now_pos_cell()
        candidates = {}
        for cell in Grid.get_all_cells():
            if self.grid.known_graph.no_path(current_position, cell):
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
                score = min(2 * Config.ant_max_rec_amount, self.grid.get_cell_resource_value(cell)) * self.grass_importance()
            if (my_resource.value <= 0 or my_resource.type == ResourceType.BREAD.value) and \
                    self.grid.get_cell_resource_type(cell) == ResourceType.BREAD.value:
                score = min(2 * Config.ant_max_rec_amount, self.grid.get_cell_resource_value(cell)) * self.bread_importance()
            score -= self.grid.expected_distance(current_position, cell)  # need to change this
            if cell == self.best_cell:
                score += 5
                # change this todo
            # boro be samti ke expected score et max she todo
            # ba in taabee momken nist dore khodemoon bekharkhim?
            candidates[cell] = score
        return candidates

    def is_not_good(self):
        candidates = self.get_scores()
        print("there is not any resource near here so we are changing strategy!")
        if len(candidates) == 0:
            return True
        # other stuff todo
        return False

    def is_really_good(self):
        # print("RUNNING IS REALLY GOOD")
        candidates = self.get_scores()
        if len(candidates) == 0:
            return False
        # print("VAL IS ", Choosing.max_choose(candidates))
        if self.grid.expected_distance(self.base_ant.get_now_pos_cell(), Choosing.max_choose(candidates)) <= 4: # change this todo
            return True
        return False

    def get_best_cell(self):
        candidates = self.get_scores()
        print("candids for grabbing are: ", "\n".join([f"{x}: {candidates[x]}" for x in candidates]))
        self.best_cell = Choosing.soft_max_choose(candidates)
        self.prev_best_cell_value = self.base_ant.grid.get_cell_resource_value(self.best_cell)
        return self.best_cell

    def go_grab_resource(self):
        cell = self.get_best_cell()
        return self.go_to(cell)

    def go_to_base(self):
        return self.go_to(self.get_base_cell())

    def grass_importance(self):
        return 1.8 + (2 * self.grid.chat_box_reader.get_now_turn() / Config.max_turn)

    def bread_importance(self):
        return 2.2 - (2 * self.grid.chat_box_reader.get_now_turn() / Config.max_turn)
    # todo linear is not good
