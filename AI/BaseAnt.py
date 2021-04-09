from .Grid import Grid
from .Cell import Cell
from .ChatBox import ChatBoxWriter, ChatBoxReader


class BaseAnt:
    def __init__(self, game):
        self.game = game
        self.grid = Grid(game)
        self.has_resource = False  # in tooye api khodeshoon bug dasht!
        self.chat_box = ChatBoxWriter

    def get_message(self):
        # implement in child
        pass

    def get_move(self):
        self.grid.visit_cell(self.get_now_pos_cell())
        # self.chat_box.listen()
        self.update_map()
        self.grid.pre_calculations(self.get_now_pos_cell())
        # this is tof
        if self.get_now_pos_cell() == self.get_base_cell():
            self.has_resource = False
        self.print_statistics()
        # implement in child
        pass

    def update_map(self):
        view_distance = self.game.viewDistance
        print("VIEW IS ", view_distance)
        if view_distance == 0:  # ina bug zadan ino 0 midan!
            view_distance = 8
        for dx in range(-view_distance-2, view_distance+2):
            for dy in range(-view_distance-2, view_distance+2):
                cell = self.game.ant.getMapRelativeCell(dx, dy)
                if cell is not None:
                    self.grid.see_cell(cell)

    def print_statistics(self):
        print("I'm in", self.get_now_pos_cell())
        print(f"I have yummy of type {self.game.ant.currentResource.type} with value {self.game.ant.currentResource.value}", self.game.ant.currentResource)
        self.grid.print_all_we_know_from_map()

    def get_now_pos_cell(self):
        return Cell(self.game.ant.currentX, self.game.ant.currentY)

    def get_base_cell(self):
        return Cell(self.game.baseX, self.game.baseY)
