from AI.Grid import Grid
from AI.Grid.Cell import Cell
from AI.ChatBox import ChatBoxWriter, ChatBoxReader, ViewCell, ViewResource
from AI.Config import Config


class BaseAnt:
    def __init__(self, game):
        self.game = game
        self.grid = Grid()
        self.has_resource = False  # in tooye api khodeshoon bug dasht!

    def get_message_and_priority(self):
        return self.grid.chat_box_writer.flush(), self.grid.chat_box_writer.get_priority()

    def pre_move(self):
        self.grid.chat_box_writer = ChatBoxWriter()
        self.grid.chat_box_reader = ChatBoxReader(self.game.chatBox)

        self.grid.pre_calculations(self.get_now_pos_cell())
        self.update_and_report_map()
        # aval chatBox ro Bebin baad map ro bebin ta etelaat override she. todo fix this

        if self.get_now_pos_cell() == self.get_base_cell():
            self.has_resource = False
        if self.grid.get_cell_resource_value(self.get_now_pos_cell()) > 0:
            self.has_resource = True # todo ask this
        self.print_statistics()

    def update_and_report_map(self):  # reporting here is not optimal
        view_distance = self.game.viewDistance
        print("VIEW IS ", view_distance)
        if view_distance == 0:  # ina bug zadan ino 0 midan!
            view_distance = 8
        for dx in range(-view_distance-2, view_distance+2):
            for dy in range(-view_distance-2, view_distance+2):
                model_cell = self.game.ant.getMapRelativeCell(dx, dy)
                if model_cell is not None:
                    self.grid.update_with_news(ViewCell(model_cell), update_chat_box=True, force_update_grid=True)
                    self.grid.update_with_news(ViewResource(model_cell), update_chat_box=True, force_update_grid=True)
                    # todo remove this ViewResource

    def print_statistics(self):
        print("I'm in", self.get_now_pos_cell())
        print(f"I have yummy of type {self.game.ant.currentResource.type} with value {self.game.ant.currentResource.value}", self.game.ant.currentResource)
        self.grid.print_all_we_know_from_map()

    def get_now_pos_cell(self):
        return Cell(Config.now_x, Config.now_y)

    def get_base_cell(self):
        return Cell(Config.base_x, Config.base_y)
