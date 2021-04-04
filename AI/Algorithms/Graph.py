from AI.Cell import Cell
import heapq, sys


class Vertex:
    def __init__(self, cell: Cell, w: int):
        self.cell = cell
        self.weight = w
        self.adjacent = []
        # Set distance to infinity for all nodes
        self.distance = -1
        # Mark all nodes unvisited        
        self.visited = False
        # Predecessor
        self.previous = None
        self.active = True

    def __lt__(self, other):
        return self.distance < other.distance

    def prepare(self):
        self.distance = -1
        self.visited = False
        self.previous = None

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def add_neighbor(self, neighbor):
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
        self.no_of_vertices = 0;
        self.vert_dict = {}
        self.curr_source = None

    # maybe the edge is repeated
    def get_vertex(self, a: Cell) -> Vertex:
        if a in self.vert_dict:
            return self.vert_dict[a]
        else:
            return None

    # maybe the vertex is repeated
    def add_vertex(self, a: Cell, w: int) -> Vertex:
        if(a not in self.vert_dict):
            self.vert_dict[a] = Vertex(a, w)
            self.no_of_vertices += 1

        self.get_vertex(a).activate()
        return self.vert_dict[a]

    def add_edge(self, a: Cell, b: Cell):
        # add_vertex(a)
        # add_vertex(b)
        self.get_vertex(a).add_neighbor(self.get_vertex(b));
        self.get_vertex(b).add_neighbor(self.get_vertex(a));

    # maybe the vertex is not available right now
    def delete_vertex(self, a: Cell):
        self.get_vertex(a).deactivate();    

    def no_path(self, a: Cell, b: Cell) -> bool:
        if(self.get_vertex(a).get_previous() == None and self.get_vertex(b).get_previous() == None):
            return True
        return False

    # always return None if there is no path
    def get_shortest_distance(self, start: Cell, end: Cell) -> int:
        if(self.no_path(start, end)):
            return None
        if(end == self.curr_source):
            start, end = end, start
        return self.get_vertex(end).get_distance();

    def get_shortest_path(self, start: Cell, end: Cell) -> [Cell]:
        assert self.get_vertex(start) != None
        assert self.get_vertex(end) != None

        swap = False
        if(end == self.curr_source):
            start, end = end, start
            swap = True

        assert start == self.curr_source

        end_ver = self.get_vertex(end)
        print ("^^", self.curr_source, start, end_ver.get_cell())

        ans = []
        while end_ver.get_cell() != start:
            print("Fuck Shayan !")
            ans.append(end_ver.get_cell())
            print(type(ans[0]), ans[0], ",$$$$$$")
            end_ver = end_ver.get_previous()
            print(type(end_ver))

        ans.append(start)
        
        if(not swap):
            ans.reverse()
        return ans

    def change_vertex_weight(self, a: Cell, w: int):
        self.get_vertex(a).set_weight(w)

    def precalculate_source(self, source: Cell):
        # we are going to ask for paths that probably one side is source.
        # you have to do the pre calculations here
        # between the pre calculations and asking queries we will not change the graph
        
        if(self.curr_source == source):
            return 

        self.curr_source = source

        for ver in self.vert_dict.values():
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
                next.set_distance(new_dist)
                next.set_previous(current)
                heapq.heappush(unvisited_queue, (new_dist, next) )

    # use shortest path algorithms implemented on the other file