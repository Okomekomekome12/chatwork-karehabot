from openai import OpenAI
import chatwork
import os
from flask import Flask, request, jsonify
app = Flask(__name__)
client = OpenAI(
    api_key  = "3bf001939eb04293964b26f9824bb80c.UDYDegcWn87NNWLh",
    base_url = "https://api.z.ai/api/paas/v4/"
)
API_TOKEN    =  "API入れて"
AI_flag      = False
AI_room_id   = None
AI_second_id = None
AI_count     = 0
history      = []
@app.route("/webhook", methods=["POST"])
def webhook():
    data       = request.json
    room_id    = chatwork.webhook_get_roomid(data)
    body       = chatwork.webhook_get_message(data)
    account_id = chatwork.webhook_get_account_id(data)
    message_id = chatwork.webhook_get_message_id(data)

    return jsonify({"status": "ok"}), 200
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
