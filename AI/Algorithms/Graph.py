from typing import List
from AI.Grid.Cell import Cell
from AI.Config import Config
import heapq


class Vertex:
    INF = 2**31

    def __init__(self, cell: Cell, w: int):
        self.cell = cell
        self.weight = w
        self.adjacent = []
        # Set distance to infinity for all nodes
        # this type of infinity can cause problem
        self.distance = Vertex.INF
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None
        self.active = True

    def __lt__(self, other):
        return self.distance < other.distance

    def prepare(self):
        # change this
        self.distance = Vertex.INF
        self.visited = False
        self.previous = None

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def add_neighbor(self, neighbor):
        if neighbor not in self.adjacent:
            self.adjacent.append(neighbor)

    def get_cell(self) -> Cell:
        return self.cell

    def get_weight(self) -> int:
        return self.weight

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_weight(self, w: int):
        self.weight = w

    def get_previous(self):
        return self.previous

    def set_previous(self, prev: Cell):
        self.previous = prev

    def set_visited(self):
        self.visited = True


class Graph:
    # weighted vertices
    # simple edges

    def __init__(self):
        self.no_of_vertices = 0
        self.curr_source = None
        self.changed = False
        self.last_precompute_order = None
        self.vertices: List[List[Vertex]] = [[None] * Config.map_height for i in range(Config.map_width)]
        self.all_vertices: List[Vertex] = []

    # maybe the edge is repeated
    def get_vertex(self, a: Cell) -> Vertex:
        if self.vertices[a.x][a.y] is not None:
            return self.vertices[a.x][a.y]
        else:
            return None

    # maybe the vertex is repeated
    def add_vertex(self, a: Cell, w: int) -> Vertex:
        self.changed = True
        if self.vertices[a.x][a.y] is None:
            self.vertices[a.x][a.y] = Vertex(a, w)
            self.all_vertices.append(self.vertices[a.x][a.y])
            self.no_of_vertices += 1

        self.get_vertex(a).activate()
        return self.vertices[a.x][a.y]

    def add_edge(self, a: Cell, b: Cell):
        self.changed = True
        # add_vertex(a)
        # add_vertex(b)
        self.get_vertex(a).add_neighbor(self.get_vertex(b))
        self.get_vertex(b).add_neighbor(self.get_vertex(a))

    # maybe the vertex is not available right now
    def delete_vertex(self, a: Cell):
        self.changed = True
        self.get_vertex(a).deactivate()

    def no_path(self, a: Cell, b: Cell) -> bool: # True if there isn't any path between a & b
        self.precalculate_source(self.last_precompute_order, is_force=True)
        reach_a = (a == self.curr_source) or (self.get_vertex(a).get_previous() is not None)
        reach_b = (b == self.curr_source) or (self.get_vertex(b).get_previous() is not None)
        if reach_a and reach_b:
            return False
        return True

    # always return None if there is no path
    def get_shortest_distance(self, start: Cell, end: Cell) -> int:
        self.precalculate_source(self.last_precompute_order, is_force=True)
        assert not self.changed
        if self.no_path(start, end):
            return None
        if end == self.curr_source:
            start, end = end, start
        return self.get_vertex(end).get_distance()

    def get_shortest_path(self, start: Cell, end: Cell) -> List[Cell]:
        self.precalculate_source(self.last_precompute_order, is_force=True)
        assert self.get_vertex(start) is not None
        assert self.get_vertex(end) is not None
        assert not self.changed

        swap = False
        if end == self.curr_source:
            start, end = end, start
            swap = True

        assert start == self.curr_source

        end_ver = self.get_vertex(end)
        # print("^^", self.curr_source, start, end_ver.get_cell())

        ans = []
        while end_ver.get_cell() != start:
            ans.append(end_ver.get_cell())
            end_ver = end_ver.get_previous()

        ans.append(start)
        
        if not swap:
            ans.reverse()
        return ans

    def change_vertex_weight(self, a: Cell, w: int):
        self.changed = True
        self.get_vertex(a).set_weight(w)

    def precalculate_source(self, source: Cell, is_force=False):
        # we are going to ask for paths that probably one side is source.
        # you have to do the pre calculations here
        # between the pre calculations and asking queries we will not change the graph

        if not is_force:
            self.last_precompute_order = source
            return

        # print("START PRE CALCULATION ", source)
        if self.changed is False and self.curr_source == source:
            return

        self.curr_source = source
        self.changed = False

        for ver in self.all_vertices:
            ver.prepare()

        start = self.get_vertex(source)

        start.set_distance(0)

        # Put tuple pair into the priority queue
        unvisited_queue = [(0, start)]
        heapq.heapify(unvisited_queue)

        while len(unvisited_queue) >= 1:
            current = heapq.heappop(unvisited_queue)[1]
            current.set_visited()
            for next in current.adjacent:
                # if visited, skip
                if next.visited:
                    continue
                # if deleted, skip
                if not next.active:
                    continue

                new_dist = current.get_distance() + next.get_weight()
                if new_dist < next.get_distance():
                    next.set_distance(new_dist)
                    next.set_previous(current)
                    heapq.heappush(unvisited_queue, (new_dist, next))

    # use shortest path algorithms implemented on the other file
