from AI.Movement import *
from .MovementStrategy import MovementStrategy
from Model import CellType, ResourceType, Direction
from AI.Grid import Grid, Cell
from AI.BaseAnt import BaseAnt, Config
from AI import Choosing
from AI.ChatBox import Gathering, Party
from typing import Optional
from Utils.decorators import once_per_turn

class GoCamp(MovementStrategy):
    party_cool_down = 6
    def __init__(self, base_ant):
        super(GoCamp, self).__init__(base_ant)
        self.best_cell = None
        self.stay = 0
        self.max_stay = 4
        self.meeting_cool_down = MovementStrategy.meet_default_cool_down
        self.cool_down = GoCamp.party_cool_down

    def get_direction(self):
        self.cool_down -= 1
        self.report_gathering()
        self.report_party()
        # print("We are choosing direction. we have resource: ", self.base_ant.game.ant.currentResource.value)
        # shayad bad nabashe ye vaghta tama kone bishtar biare
        return self.go_to_meeting()

    def get_scores(self):
        # what if candidates are empty todo
        current_position = self.base_ant.get_now_pos_cell()
        candidates = {}

        self.grid.rebuild_fight()
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

    def get_best_cell_resource(self, center: Cell) -> Cell:
        best_val = None
        best_cell = center
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if abs(dx) + abs(dy) == 2:
                    continue
                resource_sum = 0
                cell = center.move_to(dx, dy)
                if self.grid.known_graph.no_path(self.base_ant.get_now_pos_cell(), cell) :
                    continue

                for d2x in range(-1, 2):
                    for d2y in range(-1, 2):
                        if abs(d2x) + abs(d2y) == 2:
                            continue
                        res_cell = cell.move_to(d2x, d2y)

                        if self.grid.model_cell[res_cell.x][res_cell.y] is not None:
                            if self.grid.model_cell[res_cell.x][res_cell.y].resource_type is not None:
                                resource_sum += self.grid.model_cell[res_cell.x][res_cell.y].resource_value
                cell_value = ((resource_sum + 100) / 100) * self.grid.fight[cell.x][cell.y]
                if (best_val is None) or (best_val < cell_value):
                    best_val = cell_value
                    best_cell = cell

        return best_cell

    @once_per_turn
    def get_best_cell_camp(self):
        if (self.is_not_good()):
            return self.base_ant.get_now_pos_cell()

        if (self.best_cell is not None) and (self.stay > 0):
            self.stay -= 1
            return self.best_cell

        candidates = self.get_scores()
        # print("Candidates are :", candidates)
        ret = Choosing.max_choose(candidates)
        self.best_cell = self.get_best_cell_resource(ret)
        self.stay = self.max_stay
        # print("Fuck !", self.grid.fight[self.best_cell.x][self.best_cell.y])
        return self.best_cell

    def go_camp(self):
        cell = self.get_best_cell_camp()
        return self.go_to(cell)

    def get_meeting_address(self) -> Optional[Gathering]:
        gathering_best_new: Optional[Gathering] = None
        for news in self.grid.chat_box_reader.get_latest_news(Gathering):
            if news.turn + 1 != self.grid.chat_box_reader.get_now_turn():
                continue

            if (gathering_best_new is None) or (gathering_best_new.priority < news.get_priority()):
                gathering_best_new = news

        return gathering_best_new

    def go_to_meeting(self):
        gathering_best_new: Optional[Gathering] = self.get_meeting_address()

        party_best_new: Optional[Party] = None

        for news in self.grid.chat_box_reader.get_latest_news(Party):
            if news.turn + 2 < self.grid.chat_box_reader.get_now_turn():
                continue
            dis = self.grid.simple_graph.get_shortest_distance(self.base_ant.get_now_pos_cell(), Cell(news.cell.x, news.cell.y))
            if dis is None:
                continue
            if dis > 2:
                continue

            if (party_best_new is None) or (party_best_new.priority < news.get_priority()):
                party_best_new = news

        destination = gathering_best_new

        if party_best_new is not None:
            destination = party_best_new

        if destination is None:
            return Direction.CENTER

        # print("Finally a gathering !")
        # print("at turn", self.grid.chat_box_reader.get_now_turn())
        # print("we meet at (", gathering_best_new.get_cell().x,",", gathering_best_new.get_cell().y, ")")
        path = self.grid.known_graph.get_shortest_path(self.get_now_pos_cell(),
                                                       Cell.from_model_cell(destination.get_cell()))

        if len(path) == 1:
            return path[0].direction_to(path[0])
        return path[0].direction_to(path[1])

    def get_destination_path(self):
        cell = self.get_best_cell_camp()
        if self.grid.known_graph.no_path(self.get_now_pos_cell(), cell):
            cell = self.get_now_pos_cell()
        return self.grid.known_graph.get_shortest_path(self.get_now_pos_cell(), cell)

    def get_my_priority(self):
        return 256 * self.base_ant.age + self.base_ant.random_id

    def report_gathering(self):
        elder_exist = False
        for news in self.grid.chat_box_reader.get_latest_news(Gathering):
            if (news.turn + 1 == self.grid.chat_box_reader.get_now_turn()) and (self.get_my_priority() < news.priority):
                elder_exist = True
        if elder_exist:
            return

        dest_cell = self.get_best_cell_camp()

        self.grid.chat_box_writer.report(Gathering(dest_cell, age=self.base_ant.age, ant_id=self.base_ant.random_id))
        return

    def report_party(self) -> bool:
        meet_news = self.get_meeting_address()
        if meet_news is None:
            return False
        meet_cell = meet_news.get_cell()

        dis = self.grid.simple_graph.get_shortest_distance(self.base_ant.get_now_pos_cell(), meet_cell)
        if (dis != 4) or (self.cool_down > 0):
            return False

        us = len(self.base_ant.near_scorpions(0))

        all = 0
        for scorpion in self.base_ant.near_scorpions(2):
            dis = self.grid.simple_graph.get_shortest_distance(self.get_now_pos_cell(),
                                                              Cell(scorpion.currentX, scorpion.currentY))
            if dis is None:
                continue
            if dis > 2:
                continue
            all += 1

        if all == us:
            return False

        self.grid.chat_box_writer.report(Party(self.base_ant.get_now_pos_cell(), age=self.base_ant.age, ant_id=self.base_ant.random_id))
        self.party_cool_down = GoCamp.party_cool_down

        return True

