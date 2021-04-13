from .Cell import Cell
from Model import Cell as ModelCell
from copy import deepcopy
from AI.ChatBox import ViewCell


def see_cell(grid, new_cell: ModelCell, update_chat_box):
	if new_cell is None:
		return
	cell = Cell(new_cell.x, new_cell.y)
	if grid.model_cell[cell.x][cell.y] is None:
		grid.model_cell[cell.x][cell.y] = deepcopy(new_cell)  # it should be deep copy
	else:
		is_new_info = False
		if new_cell.type is not None and new_cell.type != grid.model_cell[cell.x][cell.y].type:
			grid.model_cell[cell.x][cell.y].type = new_cell.type
			is_new_info = True
		if not is_new_info:
			return
	# ignore resource type and value for now...
	# and later cover more info...

	# are we reporting the cells that become empty?
	# todo
	# store time here and check if the new information is newer than now

	# todo
	# give nearby ants we see

	if grid.model_cell[cell.x][cell.y]:
		grid.update_vertex_in_graph(cell)
	if update_chat_box:
		grid.chat_box_writer.report(ViewCell(grid.model_cell[cell.x][cell.y]))
