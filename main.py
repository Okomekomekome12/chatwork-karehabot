import os
import time
import chatwork
from flask import Flask, request, jsonify

app = Flask(__name__)

API_TOKEN = "d417c4819ad4b18a4a2c6bdbd84bb365"
SECRET_TOKEN = None

@app.route("/", methods=["GET"])
def health():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-ChatWorkWebhookSignature")
    if not chatwork.webhook_verify_signature(request.data, signature, SECRET_TOKEN): # type: ignore
        return "invalid signature", 403
    data = request.json
    room_id    = chatwork.webhook_get_roomid(data) # type: ignore
    body       = chatwork.webhook_get_message(data)
    account_id = chatwork.webhook_get_account_id(data) # type: ignore
    message_id = chatwork.webhook_get_message_id(data)


    #ーーーーーーーーーーーーーーーーーーーーーーーーーーーメインコードーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    cw = chatwork.setup(room_id, API_TOKEN)
    if body == "hello world":
        cw.messagesend("hello!")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)