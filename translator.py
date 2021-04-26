import json
from AI.ChatBox import message_text_translator


with open('../AIC21-Game/server/log.json') as f:
	mp = json.loads(f.read())

ok = True
turn_count = 0
ret = ""

for turn in mp['turns']:
	turn_count += 1
	ret += f"\nTurn {turn_count}\n\n"

	for chat in [("important0", turn['important_chat_box_0']), ("important1", turn['important_chat_box_1']), ("trivial0", turn['trivial_chat_box_0']), ("trivial1", turn['trivial_chat_box_1'])]:
		ret += f"chat box {chat[0]}:\n"
		for mes in chat[1]:
			try:
				ret += message_text_translator(mes['text']) + "\n"
			except Exception as e:
				ok_team = False

with open('../AIC21-Game/server/chat_box.log', 'w') as f:
	f.write(ret)

if not ok:
	print("error")
