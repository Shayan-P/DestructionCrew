from .Grid import Grid
from .Cell import get_random_directions, Cell


class Worker:
    def __init__(self, game):
        self.game = game
        self.grid = Grid(game)
        self.dfs_generator = self.dfs(self.get_now_pos_cell())
        self.has_resource = False  # in tooye api khodeshoon bug dasht!

    def get_message(self):
        return f"worker: I have yummy of type {self.game.ant.currentResource.type} with value {self.game.ant.currentResource.value}", 10

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

    def listen_to_chat_box(self):
        pass

    def grid_pre_calculates(self):
        self.grid.pre_calculations(self.get_now_pos_cell())

    def do_pre_tasks(self):
        self.update_map()
        self.grid_pre_calculates()
        # this is tof
        if self.get_now_pos_cell() == self.get_base_cell():
            self.has_resource = False
        self.listen_to_chat_box()

    def get_move(self):
        self.do_pre_tasks()
        self.print_statistics()
        return self.find_best_and_grab_resource().value
#        return next(self.dfs_generator).value

    def get_now_pos_cell(self):
        return Cell(self.game.ant.currentX, self.game.ant.currentY)

    def get_base_cell(self):
        return Cell(self.game.baseX, self.game.baseY)

    def dfs(self, now):
        self.grid.visit_cell(now)
        for direction in get_random_directions():
            nxt = now.go_to(direction)
            if not self.grid.is_visited(nxt) and not self.grid.is_wall(nxt):
                yield direction
                yield from self.dfs(nxt)
                yield nxt.direction_to(now)

    def find_best_and_grab_resource(self):
        # if you have grabbed it go back to base
        # mage har bar az arzeshesh yeki kam nemishod?
        # if self.game.ant.currentResource.value - self.grid.expected_distance(self.get_now_pos_cell(), self.get_base_cell()) <= 0:
        # change this
        if self.has_resource:
            return self.go_to_base()
        else:
            return self.go_grab_resource()

    def go_grab_resource(self):
        cell, score = self.grid.get_best_cell_score_with_resource(self.get_now_pos_cell())
        path = self.grid.get_best_path(self.get_now_pos_cell(), cell)
        # what if path is None?
        print("want to grab resource from", cell, "path is ", *path)
        return self.get_first_step_direction(path)

    def go_to_base(self):
        path = self.grid.get_best_path(self.get_now_pos_cell(), self.get_base_cell())
        print("want to go back to base. path is ", *path)
        return self.get_first_step_direction(path)

    def get_first_step_direction(self, path):
        assert path[0] == self.get_now_pos_cell()
        assert len(path) > 1

        # this is tof
        if self.grid.get_cell_resource_value(path[1]) > 0:
            self.has_resource = True

        return path[0].direction_to(path[1])
