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
            if self.grid.unknown_graph.no_path(current_position, cell):
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
                score = min(self.expected_workers() * Config.ant_max_rec_amount,
                            self.grid.get_cell_resource_value(cell)) * self.grass_importance()
            if (my_resource.value <= 0 or my_resource.type == ResourceType.BREAD.value) and \
                    self.grid.get_cell_resource_type(cell) == ResourceType.BREAD.value:
                score = min(self.expected_workers() * Config.ant_max_rec_amount,
                            self.grid.get_cell_resource_value(cell)) * self.bread_importance()
            if self.grid.known_graph.no_path(current_position, cell):
                distance = self.grid.unknown_graph.get_shortest_distance(current_position, cell)
            else:
                distance = self.grid.known_graph.get_shortest_distance(current_position, cell)
            # change this todo
            score -= self.distance_importance() * distance
            # this should be base distance! todo

            if cell == self.best_cell:
                score += self.best_cell_importance()
                # change this todo
            # boro be samti ke expected score et max she todo
            # ba in taabee momken nist dore khodemoon bekharkhim?
            candidates[cell] = score
        return candidates

    def has_close_resource(self):
        my_resource = self.base_ant.game.ant.currentResource
        current_position = self.get_now_pos_cell()
        for cell in Grid.get_all_cells():
            if self.grid.unknown_graph.no_path(current_position, cell):
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

    def is_not_good(self):
        if self.base_ant.game.ant.currentResource.value > 0:
            return False
        candidates = self.get_scores()
        # print("there is not any resource near here so we are changing strategy!")
        if len(candidates) == 0:
            return True
        # other stuff todo
        return False

    def is_really_good(self):
        # print("RUNNING IS REALLY GOOD")
        if self.base_ant.game.ant.currentResource.value > 0:
            return True
        candidates = self.get_scores()
        if len(candidates) == 0:
            return False
        return True
    # change this todo

    def get_best_cell(self):
        candidates = self.get_scores()
        print("candids for grabbing are: \n", "\n".join([f"{x}: {candidates[x]}" for x in candidates]))
        self.best_cell = Choosing.soft_max_choose(candidates)
        self.prev_best_cell_value = self.base_ant.grid.get_cell_resource_value(self.best_cell)
        return self.best_cell

    def go_grab_resource(self):
        now_cell = self.get_now_pos_cell()
        best_cell: Cell = self.get_best_cell()
        next_cell = self.go_to(best_cell)
        if self.grid.get_cell_resource_value(best_cell) <= 0:
            return next_cell
        distance = self.grid.expected_distance(now_cell, best_cell)
        resource_type = self.grid.get_cell_resource_type(best_cell)
        self.grid.deactivate(1 - resource_type)
        self.grid.known_graph.precalculate_source(now_cell)
        if self.grid.expected_distance(now_cell, best_cell) <= distance:
            next_cell = self.go_to(best_cell)
        self.grid.activate(1 - resource_type)
        return next_cell
        # after this function distances are not right anymore!

    def go_to_base(self):
        return self.go_to(self.get_base_cell())

    def expected_workers(self):
        # increasing this untill it's not too much will help. I set this for small maps so work positive in others\
        # todo: but it can be more optimized

        x = self.grid.chat_box_reader.get_now_turn()
        if x <= 10:
            return max(1, Config.start_worker / 2)
        elif x <= 20:
            return max(1, Config.start_worker * (1 + (x - 10) / 10) / 2)
        elif x <= 50:
            return max(1, Config.start_worker * (2 + (x - 20) / 30) / 2)
        else:
            return max(1, Config.start_worker * 3 / 2)

    def best_cell_importance(self):
        return 10

    def distance_importance(self):
        return 20

    @once_per_turn
    def bread_grass_coefficient(self):
        alive_workers = self.grid.alive_worker_count()
        grasses = []
        breads = []
        for cell in Grid.get_all_cells():
            if self.grid.unknown_graph.no_path(self.get_now_pos_cell(), cell):
                continue
            dist = cell.manhattan_distance(self.get_base_cell())
            if self.grid.get_cell_resource_type(cell) == Model.ResourceType.GRASS.value:
                val = self.grid.get_cell_resource_value(cell)
                print("val is : ", val, dist, (val / Config.ant_max_rec_amount) * 2 * dist)
                grasses.append([Config.ant_max_rec_amount / dist, (val / Config.ant_max_rec_amount) * 2 * dist])
            elif self.grid.get_cell_resource_type(cell) == Model.ResourceType.BREAD.value:
                val = self.grid.get_cell_resource_value(cell)
                print("val is : ", val, dist, (val / Config.ant_max_rec_amount) * 2 * dist)
                breads.append([Config.ant_max_rec_amount / dist, (val / Config.ant_max_rec_amount) * 2 * dist])
        grasses.sort()
        breads.sort()

        def calculate(bread_worker_ratio):
            score = 0
            copy_grasses = deepcopy(grasses)
            copy_breads = deepcopy(breads)
            now_workers = alive_workers
            turn_now = self.grid.chat_box_reader.get_now_turn()
            turn_end = min(Config.max_turn, turn_now + 50)
            for turn in range(turn_now, turn_end):
                bread_workers = bread_worker_ratio * now_workers
                grass_workers = (1-bread_worker_ratio) * now_workers
                new_workers = 0
                new_grass = 0
                while bread_workers >= 0.1 and len(copy_breads):
                    carry_boxes = min(bread_workers, copy_breads[-1][1])
                    copy_breads[-1][1] -= carry_boxes
                    bread_workers -= carry_boxes
                    value = carry_boxes * copy_breads[-1][0]
                    new_workers += value / Config.generate_kargar
                    if copy_breads[-1][1] < 0.1:
                        copy_breads.pop()
                while grass_workers >= 0.1 and len(copy_grasses):
                    carry_boxes = min(grass_workers, copy_grasses[-1][1])
                    copy_grasses[-1][1] -= carry_boxes
                    bread_workers -= carry_boxes
                    value = carry_boxes * copy_grasses[-1][0]
                    new_grass += value
                    if copy_grasses[-1][1] < 0.1:
                        copy_grasses.pop()
                now_workers += new_workers
                score_cof = (Config.max_turn - turn)  # changed
                score += score_cof * new_grass
            print("answer for query ", bread_worker_ratio, grasses, breads, alive_workers, score)
            return score
        # add unknowns resources?

        def best_interval(l, r, k):
            arr = []
            now = l
            for i in range(k+1):
                arr.append(calculate(now))
                now += (r-l) / k
            mx_ind = 0
            for i in range(k+1):
                if arr[mx_ind] < arr[i]:
                    mx_ind = i
            arr2 = []
            if mx_ind != 0:
                arr2.append(mx_ind-1)
            if mx_ind != len(arr)-1:
                arr2.append(mx_ind+1)
            if len(arr2) == 2 and arr[arr2[0]] < arr[arr2[1]]:
                arr2 = [arr2[1], arr2[0]]
            side1 = l + mx_ind * (r-l) / k
            side2 = l + arr2[0] * (r-l) / k
            if side1 > side2:
                side1, side2 = (side2, side1)
            return side1, side2

        l = 0
        r = 1
        l, r = best_interval(l, r, 6)
        l, r = best_interval(l, r, 6)
        ret = (l+r) / 2

        print("best ratio is", Config.alive_turn, "bread-grass", ret, 1-ret)

        return ret, 1-ret

    def grass_importance(self):
        return self.bread_grass_coefficient()[1] * 4.5

    def bread_importance(self):
        return self.bread_grass_coefficient()[0] * 4.5
    # this *3 is for compatibility with previous code

    def change_grid_coffs(self):
        self.grid.set_coffs(hate_known=3, opponent_base_fear=5)

    def get_best_path(self, cell_start: Cell, cell_end: Cell):
        # maybe this is bad. change this. when we grabbed something we need to reach base fast! todo
        if not self.grid.unknown_graph.no_path(cell_start, cell_end):
            return self.grid.unknown_graph.get_shortest_path(cell_start, cell_end)
        return None
