import json
from AI.ChatBox import message_text_translator


PLAYER_DATA = [[], []]

with open('../AIC21-Game/server/log.json') as f:
	mp = json.loads(f.read())

	ok = True
	turn_count = 0
	ret = ""

	for turn in mp['turns']:
		turn_count += 1
		ret += f"\nTurn {turn_count}\n\n"

		for sss, chat in [("important0", turn['important_chat_box_0']), ("important1", turn['important_chat_box_1']), ("trivial0", turn['trivial_chat_box_0']), ("trivial1", turn['trivial_chat_box_1'])]:
			ret += f"chat box {sss}:\n"
			for mes in chat:
				try:
					ret += message_text_translator(mes['text']) + "\n"
				except Exception as e:
					ok_team = False

		for player, chat in [(0, turn['trivial_chat_box_0']), (1, turn['trivial_chat_box_1'])]:
			arr = []
			for mes in chat:
				mmm = ""
				try:
					mmm += message_text_translator(mes['text']) + "\n"
				except Exception as e:
					mmm += mes['text']
				arr.append(mmm)
			PLAYER_DATA[player].append(arr)

	with open('../AIC21-Game/server/chat_box.log', 'w') as f:
		f.write(ret)

	if not ok:
		print("error")

	p = int(input("give me player (0 or 1): "))
	assert p == 0 or p == 1
	while True:
		turn = int(input("give me turn: "))
		if 1 <= turn <= len(PLAYER_DATA[p]):
			print(PLAYER_DATA[p][turn-1])
		else:
			print("invalid")
