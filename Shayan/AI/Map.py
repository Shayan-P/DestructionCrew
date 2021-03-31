from Model import *


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, obj):
        return isinstance(obj, Cell) and obj.x == self.x and obj.y == self.y

    def __ne__(self, obj):
        return not self.__eq__(obj)

    # not handled rotation
    def adjacent(self, direction):
        if direction == Direction.UP:
            return Cell(self.x, self.y-1)
        if direction == Direction.DOWN:
            return Cell(self.x, self.y+1)
        if direction == Direction.RIGHT:
            return Cell(self.x+1, self.y)
        if direction == Direction.LEFT:
            return Cell(self.x-1, self.y)
        if direction == Direction.CENTER:
            return Cell(self.x, self.y)

    def direction_to(self, cell):
        if self.x == cell.x and self.y-1 == cell.y:
            return Direction.UP
        if self.x == cell.x and self.y+1 == cell.y:
            return Direction.DOWN
        if self.x+1 == cell.x and self.y == cell.y:
            return Direction.RIGHT
        if self.x-1 == cell.x and self.y == cell.y:
            return Direction.LEFT
        return Direction.CENTER


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.val = [[-1] * height for i in range(width)]

    def is_unknown(self, cell):
        return self.val[cell.x][cell.y] == -1

    def put_cell(self, cell, new_value):
        self.val[cell.x][cell.y] = new_value
