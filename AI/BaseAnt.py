import Model
from AI.Grid import Grid
from AI.Grid.Cell import Cell
from Model import Cell as ModelCell
from Model import AntTeam, AntType, CellType
from AI.ChatBox import ChatBoxWriter, ChatBoxReader, ViewCell, ViewResource, ViewScorpion, ViewOppBase, FightZone, InitMessage
from AI.Config import Config


class BaseAnt:
    def __init__(self, game):
        self.game: Model.Game = game
        self.grid = Grid()
        self.start_turn = None
        self.previous_strategy = None
        self.previous_strategy_object = None

    def get_message_and_priority(self):
        return self.grid.chat_box_writer.flush(), self.grid.chat_box_writer.get_priority()

    def choose_best_strategy(self):
        NotImplementedError

    def get_move(self):
        self.pre_move()
        strategy = self.choose_best_strategy()
        # print("now startegy is", strategy, "previouse strategy was", self.previous_strategy)
        if strategy is self.previous_strategy:
            return self.previous_strategy_object.get_direction()
        else:
            self.previous_strategy = strategy
            self.previous_strategy_object = strategy(self)
            return self.previous_strategy_object.get_direction()

    def pre_move(self):
        self.grid.chat_box_reader.update(self.game.chatBox)
        self.grid.chat_box_writer = ChatBoxWriter(self.grid.chat_box_reader.get_now_turn())

        self.grid.listen_to_chat_box()
        self.update_and_report_map()
        self.grid.pre_calculations(self.get_now_pos_cell())

        if self.start_turn is None:
            self.start_turn = self.grid.chat_box_reader.get_now_turn()

        # self.print_statistics()

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
        self.grid.chat_box_writer.report(InitMessage())

    def print_statistics(self):
        # print("I'm in", self.get_now_pos_cell())
        # print(f"I have yummy of type {self.game.ant.currentResource.type} with value {self.game.ant.currentResource.value}", self.game.ant.currentResource)
        self.grid.print_all_we_know_from_map()

    def get_now_pos_cell(self):
        return Cell(Config.now_x, Config.now_y)

    def get_base_cell(self):
        return Cell(Config.base_x, Config.base_y)
