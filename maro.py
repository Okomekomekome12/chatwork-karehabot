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
    global AI_flag
    global AI_room_id
    global AI_second_id
    global AI_count
    global history
    cw = chatwork.setup(room_id, API_TOKEN)
    if body == "/AI-on":
        cw.messagesend("[info][title]AI起動[/title]AI起動します...\n使用AI:glm-4.5-flash[/info]")
        AI_flag    = True
        AI_room_id = room_id
        return jsonify({"status": "ok"}), 200
    elif body == "/AI-on" and AI_flag == True:
        cw.messagesend(f"{AI_room_id}で実行されているため、そこで落としてきてください")
    elif body == "/AI-on" and room_id == AI_second_id:
        cw.messagesend("[info][title]警告[/title]前回使用したから実行できないお[/info]")
        return jsonify({"status": "ok"}),200
    elif body == "/AI-off" and AI_room_id == room_id or AI_count == 50:
        cw.messagesend("[info][title]AIシャットダウン[/title]AIシャットダウンします...[/info]")
        AI_flag      = False
        AI_second_id = room_id
        AI_room_id   = None
        AI_count     = 0
        history      = []
    elif body == "/AI-off" and AI_room_id == None:
        cw.messagesend("AIは起動してないお")
        return jsonify({"status": "ok"}), 200
    elif AI_flag == True and AI_room_id == room_id:
        history.append({"role": "user", "content": f"account_id : {account_id}\n{body}"})

        messages = [{"role": "system", "content": "あなたはチャットで人間に紛れ込もうとしているAIです、名前はカレハです。AIだと人間に必ず悟られないようにしてください。タメ口でもいいので人間とだませるしゃべり方で喋ってください。また、出来るだけ文章は短くしてください。最高でも15字で。なお、人を識別できるようにメッセージの上の行にaccount_id : 1234 という感じのを載せますが、本文の中に”必ず”account_id : 1234などと入れないでください。返信するときにAIとバレます"}] + history

        response = client.chat.completions.create(
            model="glm-4.5-flash",
            messages=messages, # type: ignore
            max_tokens=128,
            temperature=0.3,
            extra_body={
                "thinking": {
                    "type": "disabled"
                }
            }
        )

        reply = response.choices[0].message.content or ""
        answer = reply.replace("[toall]", "うおw")
        history.append({"role": "assistant", "content": answer})
        cw.messagesend(f"[rp aid={account_id} to={room_id}-{message_id}][pname:{account_id}]さん\n{answer}")
        AI_count += 1
    return jsonify({"status": "ok"}), 200
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
