from .Cell import Cell
from Model import Cell as ModelCell
from copy import deepcopy
from AI.ChatBox import ViewCell


def see_cell(grid, news: ViewCell, update_chat_box, force_update_grid):
	# choon turn feeli ro nadarim nemishe last_update negah darim. todo fix this
	turn = news.get_turn()
	new_cell = news.get_cell()
	if new_cell is None:
		return
	x, y = new_cell.x, new_cell.y
	if grid.model_cell[x][y] is None:
		grid.model_cell[x][y] = deepcopy(new_cell)
	else:
		is_new_info = False
		if new_cell.type is not None and new_cell.type != grid.model_cell[x][y].type:
			grid.model_cell[x][y].type = new_cell.type
			is_new_info = True
		if new_cell.resource_type is not None and new_cell.resource_type != grid.model_cell[x][y].resource_type:
			grid.model_cell[x][y].resource_type = new_cell.resource_type
			is_new_info = True
		if new_cell.resource_value is not None and new_cell.resource_value != grid.model_cell[x][y].resource_value:
			grid.model_cell[x][y].resource_value = new_cell.resource_value
			is_new_info = True
		if new_cell.ants is not None: # special case!
			grid.model_cell[x][y].ants = new_cell.ants
			# is_new_info = True
			# it is not new info because we dont report it to chat_box

		if not is_new_info:
			return
	if grid.model_cell[x][y]:
		grid.update_vertex_in_graph(Cell(x, y))  # it is not model cell
	if update_chat_box:
		grid.chat_box_writer.report(ViewCell(grid.model_cell[x][y]))  # or only pass new information we saw?
