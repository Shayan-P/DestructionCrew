from .Cell import Cell
from Model import Cell as ModelCell
from AI.ChatBox import ViewCell, ViewOppBase, ViewScorpion, ViewResource, AttackCell
from AI.Config import Config


def see_cell(grid, news: ViewCell, is_from_chat_box, update_chat_box):
	new_cell = news.get_cell()
	if new_cell is None:
		return
	x, y = new_cell.x, new_cell.y
	if grid.model_cell[x][y] is None:
		grid.model_cell[x][y] = ModelCell(x, y, new_cell.type, None, None)
		grid.model_cell[x][y].ants = new_cell.ants
	else:
		if not is_from_chat_box:
			grid.model_cell[x][y].ants = new_cell.ants
			# it is not new info because we dont report it to chat_box
		is_new_info = False
		if new_cell.type is not None and new_cell.type != grid.model_cell[x][y].type:
			grid.model_cell[x][y].type = new_cell.type
			is_new_info = True
		if not is_new_info:
			return
	grid.update_vertex_in_graph(Cell(x, y))  # it is not model cell
	if update_chat_box:
		grid.chat_box_writer.report(ViewCell(grid.model_cell[x][y]))  # or only pass new information we saw?


def see_resource(grid, news: ViewResource, is_from_chat_box, update_chat_box):
	news_turn = min(news.turn, grid.chat_box_reader.get_now_turn())
	new_cell = news.get_cell()
	if new_cell is None:
		return
	x, y = new_cell.x, new_cell.y
	if grid.model_cell[x][y] is None:
		grid.model_cell[x][y] = ModelCell(x, y, None, new_cell.resource_value, new_cell.resource_type)
		grid.model_cell[x][y].ants = new_cell.ants
	else:
		if not is_from_chat_box:
			grid.model_cell[x][y].ants = new_cell.ants
		is_new_info = False
		if new_cell.resource_type is not None and grid.last_update[x][y] <= news_turn and new_cell.resource_type != grid.model_cell[x][y].resource_type:
			if grid.model_cell[x][y].resource_type is not None and new_cell.resource_type != grid.model_cell[x][y].resource_type:
				is_new_info = True
			grid.model_cell[x][y].resource_type = new_cell.resource_type
		if new_cell.resource_value is not None and grid.last_update[x][y] <= news_turn and new_cell.resource_value != grid.model_cell[x][y].resource_value:
			if grid.model_cell[x][y].resource_value is not None:
				is_new_info = True
			if new_cell.resource_value > 0:
				is_new_info = True
			grid.model_cell[x][y].resource_value = new_cell.resource_value
		if not is_new_info:
			return
	grid.last_update[x][y] = news_turn
	if update_chat_box:
		grid.chat_box_writer.report(ViewResource(grid.model_cell[x][y]))


def view_opp_base(grid, news: ViewOppBase, is_from_chat_box, update_chat_box):
	grid.opponent_base = Cell.from_model_cell(news.get_cell())
	grid.add_danger(
		start_cell=Cell.from_model_cell(news.get_cell()),
		starting_danger=Config.base_range * 10 + 10,
		reduction_ratio=10,
		steps=Config.base_range
	)
	if update_chat_box:
		grid.chat_box_writer.report(news)


def view_scorpion(grid, news: ViewScorpion, is_from_chat_box, update_chat_box):
	# todo handle delete scorpion
	# when a scorpion dies we should go and gather resource!
	grid.add_danger(
		start_cell=Cell.from_model_cell(news.get_cell()),
		starting_danger=Config.base_range * 5 + 5,
		reduction_ratio=5,
		steps=Config.attacker_range
	)
	if update_chat_box:
		grid.chat_box_writer.report(news)


# todo add attack cell
