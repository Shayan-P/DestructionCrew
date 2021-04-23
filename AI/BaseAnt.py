import Model
from AI.Grid import Grid
from AI.Grid.Cell import Cell
from Model import Cell as ModelCell
from Model import AntTeam, AntType, CellType, ResourceType
from AI.ChatBox import ChatBoxWriter, ChatBoxReader, ViewCell, ViewResource, ViewScorpion, ViewOppBase, FightZone,\
    InitMessage, SafeDangerCell
from AI.Config import Config
from AI.Grid.sync_information import read_view_fight, report_view_fight


class BaseAnt:
    def __init__(self, game):
        self.game: Model.Game = game
        self.grid = Grid()
        self.start_turn = None
        self.previous_strategy = None
        self.previous_strategy_object = None
        self.previous_health = None
        self.previous_cell = None
        self.previous_resource_value = 0
        self.total_bread_picked = 0
        self.total_grass_picked = 0

    def get_message_and_priority(self):
        return self.grid.chat_box_writer.flush(), self.grid.chat_box_writer.get_priority()

    def choose_best_strategy(self):
        NotImplementedError

    def get_move(self):
        self.pre_move()
        strategy = self.choose_best_strategy()
        if strategy is self.previous_strategy:
            ret = self.previous_strategy_object.get_direction()
        else:
            self.previous_strategy = strategy
            self.previous_strategy_object = strategy(self)
            ret = self.previous_strategy_object.get_direction()
        self.after_move()
        return ret

    def pre_move(self):
        if self.previous_health is None:
            self.previous_health = self.game.ant.health
        if self.previous_cell is None:
            self.previous_cell = self.get_now_pos_cell()

        self.grid.chat_box_reader.update(self.game.chatBox)
        self.grid.chat_box_writer = ChatBoxWriter(self.grid.chat_box_reader.get_now_turn())

        self.grid.listen_to_chat_box()
        self.update_and_report_map()
        # to pre calculations after all information grabbing
        self.grid.pre_calculations(self.get_now_pos_cell())

        if self.start_turn is None:
            self.start_turn = self.grid.chat_box_reader.get_now_turn()

        self.print_statistics()

    def after_move(self):
        self.update_resource_history()
        self.previous_health = self.game.ant.health
        self.previous_cell = self.get_now_pos_cell()

    def update_resource_history(self):
        if self.game.ant.currentResource.value > self.previous_resource_value:
            if self.game.ant.currentResource.type == ResourceType.BREAD.value:
                self.total_bread_picked += self.game.ant.currentResource.value - self.previous_resource_value
            elif self.game.ant.currentResource.type == ResourceType.GRASS.value:
                self.total_grass_picked += self.game.ant.currentResource.value - self.previous_resource_value
        self.previous_resource_value = self.game.ant.currentResource.value

    def update_and_report_map(self):
        view_distance = Config.view_distance  # be nazar bugeshoon bartaraf shode
        for dx in range(-view_distance-2, view_distance+2):
            for dy in range(-view_distance-2, view_distance+2):
                model_cell: ModelCell = self.game.ant.getMapRelativeCell(dx, dy)
                if model_cell is not None:
                    self.grid.update_with_news(ViewCell(model_cell),
                                               update_chat_box=self.game.alive_turn != 0, is_from_chat_box=False)
                    self.grid.update_with_news(ViewResource(model_cell),
                                               update_chat_box=self.game.alive_turn != 0, is_from_chat_box=False)
                    for ant in model_cell.ants:
                        if ant.antTeam == AntTeam.ENEMY.value and ant.antType == AntType.SARBAAZ.value:
                            self.grid.update_with_news(ViewScorpion(model_cell),
                                                       update_chat_box=True, is_from_chat_box=False)
                        if ant.antTeam == AntTeam.ENEMY.value:
                            self.grid.update_with_news(FightZone(self.get_now_pos_cell(), model_cell),
                                                       update_chat_box=True, is_from_chat_box=False)

                    if model_cell.type == CellType.BASE.value and Cell.from_model_cell(model_cell) != self.get_base_cell():
                        self.grid.update_with_news(ViewOppBase(model_cell),
                                                   update_chat_box=True, is_from_chat_box=False)

        if self.grid.chat_box_reader.get_now_turn() == Config.chat_box_first_turn:
            self.grid.chat_box_writer.report(InitMessage())
        if self.game.ant.health < self.previous_health:
            self.grid.update_with_news(SafeDangerCell(self.previous_cell, danger=True),
                                       update_chat_box=True, is_from_chat_box=False)
        else:
            self.grid.update_with_news(SafeDangerCell(self.previous_cell, danger=False),
                                       update_chat_box=self.game.alive_turn != 0, is_from_chat_box=False)
        for attack in self.game.ant.attacks:
            if attack.is_attacker_enemy:
                a = Cell(attack.attacker_col, attack.attacker_row)
                b = Cell(attack.defender_col, attack.defender_row)
                if a.manhattan_distance(b) > Config.attacker_range:
                    self.grid.update_with_news(ViewOppBase(a), update_chat_box=True, is_from_chat_box=False)

    def print_statistics(self):
        print("expected turn is ", self.grid.chat_box_reader.get_now_turn())
        print("alived turn is ", self.game.alive_turn)
        print("prev startegy was", self.previous_strategy)
        print("now we have", self.game.ant.currentResource.type, self.game.ant.currentResource.value)
        print("we think opponent's base is in ", self.grid.expected_opponent_base())
        print("attacks: ")
        for attack in self.game.ant.attacks:
            print(attack.attacker_row)
            print(attack.attacker_col)
            print(attack.defender_row)
            print(attack.defender_col)
            print(attack.is_attacker_enemy)

        # self.grid.print_all_we_know_from_map()

    def get_now_pos_cell(self):
        return Cell(Config.now_x, Config.now_y)

    def get_base_cell(self):
        return Cell(Config.base_x, Config.base_y)
