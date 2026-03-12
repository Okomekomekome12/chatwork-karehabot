import os
import time
import chatwork
from flask import Flask, request, jsonify
from modules import math
app = Flask(__name__)
API_TOKEN = "d417c4819ad4b18a4a2c6bdbd84bb365"
SECRET_TOKEN = None

@app.route("/", methods=["GET"])
def health():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-ChatWorkWebhookSignature")
    if not chatwork.webhook_verify_signature(request.data, signature, SECRET_TOKEN):  # type: ignore
        return "invalid signature", 403
    data = request.json
    room_id    = chatwork.webhook_get_roomid(data) 
    body       = chatwork.webhook_get_message(data)
    account_id = chatwork.webhook_get_account_id(data) 
    message_id = chatwork.webhook_get_message_id(data)


    #ーーーーーーーーーーーーーーーーーーーーーーーーーーーメインコードーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    cw = chatwork.setup(room_id, API_TOKEN)

    if body == "/startmath":
        answer = math.start(cw)
        cw.messagesend(f"{answer}")
    elif body == "/助けて":
        cw.messagesend("[info][title]これはカレハbotのコマンド一覧だよ、よく読め([/title]\
[info]/startmath : 簡単()な計算問題を出してきます、\n15秒待って最後に取得したメッセージが数字ではないとエラーを吐いて止まる親切設計です()[/info]\
[hr]\
[info]/助けて : cwbotとコマンド重なるのでこれ()[/info]\
[hr]\
[info]/update : アップデートしたら乗せるお[/info]\
[/info]")
    elif body == "/update":
        cw.messagesend("[info][title]アップデート情報[/title]\
まだアップデートは来ていません[/info]")
    

    


    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)