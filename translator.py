import json
from builtins import print
from AI.ChatBox import message_text_translator


PLAYER_DATA = [[], []]
ok = [True, True]

with open('../AIC21-Game/server/log.json') as f:
	mp = json.loads(f.read())

	turn_count = 0
	ret = ""

	for turn in mp['turns']:
		turn_count += 1
		ret += f"\nTurn {turn_count}\n\n"

		for player, chat in [(0, turn['trivial_chat_box_0']), (1, turn['trivial_chat_box_1'])]:
			ret += f"team {player}:\n"
			arr = []
			for mes in chat:
				mmm = ""
				try:
					mmm += message_text_translator(mes['text']) + "\n"
					ret += message_text_translator(mes['text']) + "\n"
				except Exception as e:
					mmm += mes['text']
					ok[player] = False
				arr.append(mmm)
			PLAYER_DATA[player].append(arr)

	with open('../AIC21-Game/server/chat_box.log', 'w') as f:
		f.write(ret)

	if not ok[0]:
		print("error in parsing player 0")
	if not ok[1]:
		print("error in parsing player 1")

	p = int(input("give me player (0 or 1): "))
	assert p == 0 or p == 1
	while True:
		turn = int(input("give me turn: "))
		if 1 <= turn <= len(PLAYER_DATA[p]):
			print(PLAYER_DATA[p][turn-1])
		else:
			print("invalid")
