import time

from Model import *
from .Attacker import Attacker
from .Worker import Worker
from AI.Config import Config
from Utils import logger
from settings import DEBUG, HAS_SLEEP
from AI.BaseAnt import BaseAnt

# just remove this and everything will be printed in console


class AI:
	def __init__(self):
		# Current Game State
		self.game: Game = None

		# Answer
		self.message: str = None
		self.direction: int = None
		self.value: int = None

	"""
	Return a tuple with this form:
		(message: str, message_value: int, message_direction: int)
	check example
	"""

	def turn(self) -> (str, int, int):
		global turn_count

		Config.start_time = time.time()

		update_config(self.game)
		Config.alive_turn = turn_count
		if turn_count == 0:
			init(self.game)
		turn_count += 1  # store the turns
		ant: BaseAnt = get_ant(self.game.antType)
		ant.game = self.game
		self.direction = ant.get_move()
		self.message, self.value = ant.get_message_and_priority()
		# print("turn ", self.message, self.value, self.direction)


		# this is for server failiure in fast games!
		if HAS_SLEEP:
			time.sleep(0.01)

		ant.use_extra_time()
		print("turn: ", turn_count, f"took us {Config.how_much_time()} seconds")
		return self.message, self.value, self.direction.value


turn_count = 0
worker = None
attacker = None


def init(game):
	global worker, attacker
	worker = Worker(game)
	attacker = Attacker(game)


def get_ant(ant_type):
	if ant_type == AntType.SARBAAZ.value:
		return attacker
	else:
		return worker


def update_config(game: Game):
	Config.ant_type = game.antType
	Config.map_width = game.mapWidth
	Config.map_height = game.mapHeight
	Config.base_x = game.baseX
	Config.base_y = game.baseY
	Config.health_kargar = game.healthKargar
	Config.health_sarbaaz = game.healthSarbaaz
	Config.attack_distance = game.attackDistance
	Config.view_distance = game.viewDistance
	Config.generate_kargar = game.generateKargar
	Config.generate_sarbaaz = game.generateSarbaaz
	Config.rate_death_resource = game.rateDeathResource
	Config.now_x = game.ant.currentX
	Config.now_y = game.ant.currentY
