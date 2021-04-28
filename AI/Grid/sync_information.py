from .Cell import Cell
from Model import Cell as ModelCell
from AI.ChatBox import ViewCell, ViewOppBase, ViewScorpion, ViewResource, SafeDangerCell, FightZone
from AI.Config import Config


def see_cell(grid, news: ViewCell, is_from_chat_box, update_chat_box):
	new_cell = news.get_cell()
	if new_cell is None:
		return
	x, y = new_cell.x, new_cell.y
	if grid.model_cell[x][y] is None:
		grid.model_cell[x][y] = ModelCell(x, y, new_cell.type, 0, 2)
		grid.update_vertex_in_graph(Cell(x, y))
	else:
		update_chat_box = False
	if not is_from_chat_box:
		grid.model_cell[x][y].ants = new_cell.ants
	if update_chat_box:
		grid.chat_box_writer.report(ViewCell(grid.model_cell[x][y]))


def see_resource(grid, news: ViewResource, is_from_chat_box, update_chat_box):
	new_cell = news.get_cell()
	if new_cell is None:
		return
	x, y = new_cell.x, new_cell.y
	assert grid.model_cell[x][y] is not None
	if grid.model_cell[x][y].resource_type != new_cell.resource_type or grid.model_cell[x][y].resource_value != new_cell.resource_value:
		grid.model_cell[x][y].resource_type = new_cell.resource_type
		grid.model_cell[x][y].resource_value = new_cell.resource_value
	else:
		update_chat_box = False
	if update_chat_box:
		grid.chat_box_writer.report(ViewResource(grid.model_cell[x][y]))


def view_opp_base(grid, news: ViewOppBase, is_from_chat_box, update_chat_box):
	grid.report_opponent_base(Cell.from_model_cell(news.get_cell()))
	if update_chat_box:
		grid.chat_box_writer.report(news)


def view_safe_danger_cell(grid, news: SafeDangerCell, is_from_chat_box, update_chat_box):
	# not handled danger == True case. todo
	# in chize agar ye edde ziadi yek ja hatta zir attack sangin bashan kharab mishe
	grid.report_crowded(news.get_cell())

	if not news.danger:
		grid.divide_scorpion_danger(
			start_cell=news.get_cell(),
			steps=Config.view_distance // 2,
			division=2
		)
	if update_chat_box:
		grid.chat_box_writer.report(news)


def view_scorpion(grid, news: ViewScorpion, is_from_chat_box, update_chat_box):
	grid.add_scorpion_danger(
		start_cell=Cell.from_model_cell(news.get_cell()),
		starting_danger=Config.attacker_range * 5 + 5,
		reduction_ratio=5,
		steps=Config.attacker_range
	)
	if update_chat_box:
		grid.chat_box_writer.report(news)


def view_fight(grid, news: FightZone, is_from_chat_box, update_chat_box):
	grid.add_fight(Cell.from_model_cell(news.get_cell()), 2, 1, 1)
	if update_chat_box:
		grid.chat_box_writer.report(news)


def read_view_fight(grid, news):
	grid.add_fight(Cell.from_model_cell(news.get_cell()), 2, 1, 1) # todo


def report_view_fight(grid, news):
	grid.chat_box_writer.report(news)


def see_alive_ant(grid, news, is_from_chat_box, update_chat_box):
	if news.is_worker:
		grid.report_worker_alive(ant_id=news.ant_id, turn=news.turn)
	else:
		grid.report_attacker_alive(ant_id=news.ant_id, turn=news.turn)
	if update_chat_box:
		grid.chat_box_writer.report(news)
