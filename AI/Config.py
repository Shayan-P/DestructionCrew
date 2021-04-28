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
	swamp_stay = 3
