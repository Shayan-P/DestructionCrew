from AI.Movement import *
from .MovementStrategy import MovementStrategy
from Model import CellType, ResourceType
from AI.Grid import Grid, Cell
from AI.BaseAnt import BaseAnt, Config
from AI import Choosing
from AI.ChatBox import Gathering

class GoCamp(MovementStrategy):
    def __init__(self, base_ant):
        super(GoCamp, self).__init__(base_ant)
        self.best_cell = None
        self.stay = 0
        self.max_stay = 8
        self.meeting_cool_down = MovementStrategy.meet_default_cool_down

    def get_direction(self):

        # print("We are choosing direction. we have resource: ", self.base_ant.game.ant.currentResource.value)
        # shayad bad nabashe ye vaghta tama kone bishtar biare
        return self.go_camp()
        #
        # if Cell(self.base_ant.game.baseX, self.base_ant.game.baseY) == self.base_ant.get_now_pos_cell():
        #     self.best_cell = None
        #
        # if self.base_ant.game.ant.currentResource.value > 0.5 * Config.ant_max_rec_amount:
        #     return self.go_to_base()
        # else:
        #     return self.go_grab_resource()

    def get_scores(self):
        # what if candidates are empty todo
        current_position = self.base_ant.get_now_pos_cell()
        candidates = {}

        self.grid.rebuild_fight()
        # print("Gooh")
        for cell in Grid.get_all_cells():
            if self.grid.known_graph.no_path(current_position, cell):
                continue
            if self.grid.is_unknown(cell):
                continue
            x = cell.x
            y = cell.y

            score = self.grid.fight[x][y]
            if(score == 0):
                continue
            # score += 0.25 * self.grid.expected_distance(current_position, cell)  # need to change  this
            # boro be samti ke expected score et max she todo
            # ba in taabee momken nist dore khodemoon bekharkhim?
            candidates[cell] = score
        return candidates

    def is_not_good(self):
        candidates = self.get_scores()
        if len(candidates) == 0:
            return True
        # other stuff todo
        return False

    # def is_really_good(self):
    #     # print("RUNNING IS REALLY GOOD")
    #     candidates = self.get_scores()
    #     if len(candidates) == 0:
    #         return False
    #     # print("VAL IS ", Choosing.max_choose(candidates))
    #     if self.grid.expected_distance(self.base_ant.get_now_pos_cell(), Choosing.max_choose(candidates)) <= 4: # change this todo
    #         return True
    #     return False

    def get_best_cell(self):
        if (self.is_not_good()):
            return self.base_ant.get_now_pos_cell()

        if (self.best_cell is not None) and (self.stay > 0):
            self.stay -= 1
            return self.best_cell

        candidates = self.get_scores()
        # print("Candidates are :", candidates)
        self.best_cell = Choosing.max_choose(candidates)
        self.stay = self.max_stay
        # print("Fuck !", self.grid.fight[self.best_cell.x][self.best_cell.y])
        return self.best_cell

    def go_camp(self):
        cell = self.get_best_cell()
        return self.go_to(cell)

    def get_destination_path(self):
        cell = self.get_best_cell()
        if self.grid.known_graph.no_path(self.get_now_pos_cell(), cell):
            cell = self.get_now_pos_cell()
        return self.grid.known_graph.get_shortest_path(self.get_now_pos_cell(), cell)
    # def go_to_base(self):
    #     # print("base cell is ", self.get_base_cell())
    #     return self.go_to(self.get_base_cell())
    #
    # def need_grass(self):
    #     return 1
    #
    # def need_bread(self):
    #     return 1


    def report_gathering(self):
        attacked = (self.base_ant.game.ant.health < self.base_ant.previous_health)
        if Config.alive_turn == 3:
            path = self.get_destination_path()
            if(len(path) > 10):
                idx = len(path) - 2
                self.grid.chat_box_writer.report(
                    Gathering(path[idx], life_time=idx + 2, priority=Config.alive_turn))
                self.meeting_cool_down = MovementStrategy.meet_default_cool_down
                return
        self.meeting_cool_down -= 1
        if (not attacked) and (self.meeting_cool_down > 0):
            return
        # handle case when we are invited somewhere else todo

        us = len(self.base_ant.near_scorpions(0))

        all = 0
        print("Count of US is", us)

        max_dis = 0
        for scorpion in self.base_ant.near_scorpions(Config.ants_view):
            dis = self.grid.known_graph.get_shortest_distance( self.get_now_pos_cell(), Cell(scorpion.currentX, scorpion.currentY) )

            if dis is None:
                continue
            if dis > 4:
                continue

            max_dis = max(max_dis, dis)
            all += 1
        print("Count of ALL is", all)
        if all == us:
            return

        best = max_dis
        best_cell = self.get_now_pos_cell()
        # for cell in self.grid.get_all_cells():
        #     dis = self.grid.known_graph.get_shortest_distance(self.get_now_pos_cell(), cell)
        #     if (dis is None) or (dis > 4):
        #         continue
        #     max_dis = dis
        #     for scorpion in self.near_scorpions(Config.ants_view):
        #         dis = self.grid.known_graph.get_shortest_distance(self.get_now_pos_cell(),
        #                                                           Cell(scorpion.currentX, scorpion.currentY))
        #
        #         if dis is None:
        #             continue
        #         if dis > 4:
        #             continue
        #
        #         dis = cell.manhattan_distance( Cell(scorpion.currentX, scorpion.currentY) )
        #         max_dis = max( max_dis, dis)
        #     if max_dis < best:
        #         best = max_dis
        #         best_cell = cell
        self.grid.chat_box_writer.report(Gathering(best_cell, life_time=best + 2, priority=Config.alive_turn))

