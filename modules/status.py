def status(cw, account_id, body, BOT_ACCOUNT_ID, AI_flag, AI_room_id, AI_second_id, AI_count, role, less_flag, less_room_id, glm_less_flag, glm_less_room_id, gemini_flag, gemini_room_id, gemini_account_id):
    cw.messagesend(f"""[info][title]状態確認[/title][code]account_id: {account_id}
body: {body}
BOT_ID: {BOT_ACCOUNT_ID}
一致?: {int(account_id) == BOT_ACCOUNT_ID}
AI_flag: {AI_flag}
AI_room_id: {AI_room_id}
AI_second_id: {AI_second_id}
AI_count: {AI_count}
role : {role}
less-battle : {less_flag}
less-room_id : {less_room_id}
glm_less_flag : {glm_less_flag}
glm_less_room_id : {glm_less_room_id}
gemini_flag : {gemini_flag}
gemini_room_id : {gemini_room_id}
gemini_account_id : {gemini_account_id}[/code][/info]""")