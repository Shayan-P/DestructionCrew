from AI.Map import Cell


class Graph:
    # weighted vertices
    # simple edges

    def __init__(self):
        pass

    def add_edge(self, a: Cell, b: Cell):
        pass

    def add_vertex(self, a: Cell, w: int):
        pass

    def no_path(self, a: Cell, b: Cell) -> bool:
        pass

    # always return None if there is no path
    def get_shortest_distance(self, start: Cell, end: Cell) -> int:
        pass

    def get_shortest_path(self, start: Cell, end: Cell) -> [Cell]:
        pass

    def change_vertex_weight(self, a: Cell, w: int):
        pass

    def precalculate_source(self, source: Cell):
        # we are going to ask for paths that probably one side is source.
        # you have to do the pre calculations here
        # between the pre calculations and asking queries we will not change the graph
        pass

    # use shortest path algorithms implemented on the other file
