from AI.Config import Config

func_names_to_turn = {}
func_names_to_answer = {}
names_alert = set()


def once_per_turn(func):
	assert func.__name__ not in names_alert
	names_alert.add(func.__name__)

	def outer_func(*args, **kwargs):
		if func.__name__ not in func_names_to_turn:
			func_names_to_turn[func.__name__] = -1
		if func_names_to_turn[func.__name__] != Config.alive_turn:
			func_names_to_answer[func.__name__] = func(*args, **kwargs)
			func_names_to_turn[func.__name__] = Config.alive_turn
		return func_names_to_answer[func.__name__]
	return outer_func
