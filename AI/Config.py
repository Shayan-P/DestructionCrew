class Config:
	ant_type = -1
	map_width = -1
	map_height = -1
	base_x = -1
	base_y = -1
	health_kargar = -1
	health_sarbaaz = -1
	attack_distance = -1
	view_distance = -1
	generate_kargar = -1
	generate_sarbaaz = -1
	rate_death_resource = -1
	now_x = -1
	now_y = -1

	chat_box_first_turn = 1
	# this is static one
	# update this one
	ants_view = 4
	ants_reg_rate = 0.8
	base_range = 6
	base_damage = 3
	base_health = 10
	max_com_per_turn = 5
	max_com_length = 32
	max_turn = 200
	worker_health = 3
	attacker_health = 5
	attacker_range = 4
	attacker_damage = 1
	worker_price = 10
	attacker_price = 15
	ant_max_rec_amount = 10
	start_worker = 4
	start_attacker = 0
	max_turn_time = 0.1
	map_size = 35
	map_wall_perc = 0.2
	min_base_dist = 10
	work_rec_amount = 800
	attack_rec_amount = 800
	mirror_effect = True

	# todo check konam mellat faghat az ina estefade konan
	# todo delete get_now_pos from BaseAnt
	# todo update Client Repository

	# this is our constants
	PingRate = 35
	alive_turn = -1
	swamp_stay = 3 + 1

	@staticmethod
	def linear(start, finish, count):
		if count == 1:
			return [start]
		d = (finish - start) / (count - 1)
		return [start + d * i for i in range(count)]

	limit_grass_arr = linear(80, 90, 10) + linear(90, 120, 10) + linear(120, 160, 10) + linear(160, 210, 10) + linear(
		210, 270, 10) + linear(270, 340, 10) + linear(340, 500, 50) + linear(500, 800, 120) + linear(800, 1000, 100)

	@staticmethod
	def get_limit_of_grass_in_turn(turn):
		return Config.limit_grass_arr[turn]
