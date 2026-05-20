import os
import chatwork
from openai import OpenAI
import time
from flask import Flask, request, jsonify, render_template
from modules import add_url, math , help, ytdlp_check , blacklist

client = OpenAI(
    api_key  = "3bf001939eb04293964b26f9824bb80c.UDYDegcWn87NNWLh",
    base_url = "https://api.z.ai/api/paas/v4/"
)

app = Flask(__name__)

API_TOKEN    = os.getenv("API_TOKEN")
SECRET_TOKEN = None
shutdown     = False
AI_flag      = False
AI_room_id   = None
AI_second_id = None
AI_count     = 0
history      = []
user_state   = {}
BOT_ACCOUNT_ID = 11156582
@app.route("/", methods=["GET"])
def health():
    return render_template('index.html')


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-ChatWorkWebhookSignature")
    if not chatwork.webhook_verify_signature(request.data, signature, SECRET_TOKEN): # type: ignore
        return "invalid signature", 403

    data       = request.json
    room_id    = chatwork.webhook_get_roomid(data)
    body       = chatwork.webhook_get_message(data)
    account_id = chatwork.webhook_get_account_id(data)
    message_id = chatwork.webhook_get_message_id(data)



    global shutdown
    global AI_flag
    global AI_room_id
    global AI_second_id
    global AI_count
    global history

    # デバッグログ
    print(f"\n=== Webhook受信 ===")
    print(f"account_id: {account_id}")
    print(f"body: {body}")
    print(f"BOT_ID: {BOT_ACCOUNT_ID}")
    print(f"一致?: {int(account_id) == BOT_ACCOUNT_ID}")
    print(f"AI_flag: {AI_flag}")
    print(f"AI_room_id: {AI_room_id}")
    print(f"AI_second_id: {AI_second_id}")
    print(f"AI_count: {AI_count}")
    print(body[43:51])
    print(body.find("[dtext:chatroom_added]"))
    print(f"==================\n")
    cw = chatwork.setup(room_id, API_TOKEN)
    cw2 = chatwork.setup(420107748,API_TOKEN)
    log_room = chatwork.setup(418992889,API_TOKEN)
    try:
        if int(account_id) == BOT_ACCOUNT_ID:
            print("→ Bot自身のメッセージなのでスキップ")
            return jsonify({"status": "ok"}), 200

        logs = body.replace("[/code]","")
        log_room.messagesend(f"[info][title][piconname:{account_id}]のメッセージ \nメッセリンク→https://www.chatwork.com/#!rid{room_id}-{message_id}[/title][code]{logs}[/code][/info]")

        if body == "/start":
            cw.messagesend("起動します")
            shutdown = False
            return jsonify({"status": "ok"}), 200
        
        if shutdown == True:
            print("シャットダウン中なのでスキップ")
            return jsonify({"status": "ok"}), 200
        
        if body.find("[dtext:chatroom_added]") == 95:
            target_account_id = body[86:93]
            print("===メンバー参加確認===")
            print(target_account_id)
            blacklist.check(cw,target_account_id)
            

        if body and (body.count("(quick)") >= 10 or body.count(":*") >= 10):
            cw.viewer(account_id)
            cw.messagesend("[info][title]荒らし検知[/title]荒らしを検知しました、流します[/info]")

            for i in range(70):
                cw.messagesend("a")
                time.sleep(0.7)

            message_link = cw.get_message_link()
            cw.messagesend("[info][title]荒らし対処完了[/title]寝の部屋にメッセージリンクを配布します[/info]")
            cw2.messagesend(f"[info][title]メッセリンク配布[/title]{message_link}[/info]")

            description = log_room.get_description()
            room_name   = log_room.get_room_name()
            log_room.edit_room_description(f"[info][title]メッセリンク配布[/title]{message_link}[/info]" + str(description),room_name)
            
            blacklist.add(account_id)

        chatwork.auto_accept_contacts(API_TOKEN)

        if body and body.count("[toall]") >= 1:
            cw.viewer(account_id)
            cw.messagesend("[info][title]toall検知[/title]何してんねんハゲぇぇぇぇぇぇぇぇ（（（[/info]")
            blacklist.add(account_id)
            
        if body == "/live?":
            cw.messagesend("[info][title]荒らし対策bot正常稼働中[/title]生きてるお[/info]")

        if body == "/AI-on":
            cw.messagesend("[info][title]AI起動[/title]AI起動します...\n使用AI:glm-4.5-flash[/info]")
            AI_flag    = True
            AI_room_id = room_id
            return jsonify({"status": "ok"}), 200
        
        if body == "/AI-on" and AI_room_id == room_id:
            cw.messagesend("[info][title]AI実行中[/title]既に実行されてます[/info]")
            return jsonify({"status": "ok"})
        
        if body == "/AI-on" and room_id == AI_second_id:
            cw.messagesend("[info][title]警告[/title]前回使用したから実行できないお[/info]")
            return jsonify({"status": "ok"})
        
        if body == "/AI-off" and AI_room_id == room_id or AI_count == 50:
            cw.messagesend("[info][title]AIシャットダウン[/title]AIシャットダウンします...[/info]")
            AI_flag = False
            AI_second_id = room_id
            AI_room_id = None
            AI_count = 0
            history = []
        elif body == "/AI-off" and AI_room_id == None:
            cw.messagesend("AIは起動してないお")
            return jsonify({"status": "ok"}), 200
        elif body == "/AI-off":
            cw.messagesend(f"{AI_room_id}で実行されているため、そこで落としてきてください")

        if body == "/readme":
            cw.messagesend("このbotを導入したいと思ったことはありますよねぇ！？そうですよねぇ！？（圧）\n")


        # 計算問題の回答チェック
        if account_id in math.current_questions:
            print(f"→ 計算問題の回答チェック実行")
            math.answer(account_id, body, cw)
            return jsonify({"status": "ok"}), 200

        if body == "/shutdown" and account_id == 10870480:
            cw.messagesend("シャットダウンします、、、")
            shutdown = True

        elif body == "/shutdown":
            cw.messagesend("この操作は古米しかできないお")

        if body and body.count("削除") >= 1:
            target = body.split("to=")[1].split("]")[0]  
            delete_room_id , delete_message_id = target.split("-")
            deleter_room_id = delete_room_id
            deleter_message_id = delete_message_id
            print(deleter_room_id,deleter_message_id)
            cw.delete_message(deleter_message_id)

        # URL待ち状態の処理
        if account_id in user_state:
            state = user_state.pop(account_id)
            if state == "add-rammerhead":
                add_url.add_rammerhead(body, cw)
            elif state == "add-utopia":
                add_url.add_utopia(body, cw)
            elif state == "add-wakame":
                add_url.add_wakame(body, cw)
            elif state == "add-other":
                add_url.add_other(body, cw)
            elif state == "delete-rammerhead":
                add_url.delete_rammerhead(body, cw)
            elif state == "delete-utopia":
                add_url.delete_utopia(body, cw)
            elif state == "delete-wakame":
                add_url.delete_wakame(body, cw)
            elif state == "delete-other":
                add_url.delete_other(body, cw)
            return jsonify({"status": "ok"}), 200
        

        if body == "/startmath":
            print(f"→ /startmath 実行")
            math.start(account_id, cw)
        
        if body == "/助けて":
            help.help(cw,account_id,room_id,message_id)

        if body == "/update":
            cw.messagesend("[info][title]アップデート情報[/title]\
    ytdlpコマンド追加！仙人さんコード提供ありがとうございます！[/info]")
            
        if body == "/link":
            add_url.show_list(cw)
        
        if body == "/ytdlp":
            ytdlp_check.check_status(cw)

        if body == "/blacklist":
            blacklist.accont_list(cw)
        
        if body.find("/delete-blacklist") == 0:
            account_id = body.split()[1]
            blacklist.delete(cw,account_id)


        if body == "/add-rammerhead":
            cw.messagesend("ランマーヘッドをリスト一覧に追加します\nこのメッセージの次に\"必ず\"リンクを載せてください")
            user_state[account_id] = "add-rammerhead"
        
        elif body == "/add-utopia":
            cw.messagesend("utopiaをリスト一覧に追加します\nこのメッセージの次に\"必ず\"リンクを載せてください")
            user_state[account_id] = "add-utopia"
        
        elif body == "/add-wakame":
            cw.messagesend("わかめtubeをリスト一覧に追加します\nこのメッセージの次に\"必ず\"リンクを載せてください")
            user_state[account_id] = "add-wakame"
        
        elif body == "/add-other":
            cw.messagesend("その他をリスト一覧に追加します\nこのメッセージの次に\"必ず\"リンクを載せてください")
            user_state[account_id] = "add-other"
        
        elif body == "/delete-rammerhead":
            cw.messagesend("ランマーヘッドをリスト一覧から削除します\nこのメッセージの次に\"必ず\"リンクを載せてください")
            user_state[account_id] = "delete-rammerhead"
        
        elif body == "/delete-utopia":
            cw.messagesend("utopiaをリスト一覧から削除します\nこのメッセージの次に\"必ず\"リンクを載せてください")
            user_state[account_id] = "delete-utopia"
        
        elif body == "/delete-wakame":
            cw.messagesend("わかめtubeをリスト一覧から削除します\nこのメッセージの次に\"必ず\"リンクを載せてください")
            user_state[account_id] = "delete-wakame"
        
        elif body == "/delete-other":
            cw.messagesend("その他をリスト一覧から削除します\nこのメッセージの次に\"必ず\"リンクを載せてください")
            user_state[account_id] = "delete-other"
        
        if AI_flag == True and AI_room_id == room_id:
            history.append({"role": "user", "content": f"account_id : {account_id}\n{body}"})

            messages = [{"role": "system", "content": "あなたはチャットで人間に紛れ込もうとしているAIです、名前はカレハです。AIだと人間に必ず悟られないようにしてください。タメ口でもいいので人間とだませるしゃべり方で喋ってください。また、出来るだけ文章は短くしてください。最高でも15字で。なお、人を識別できるようにメッセージの上の行にaccount_id : 1234 という感じのを載せます。それで識別して下さい。"}] + history

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

            reply = response.choices[0].message.content
            history.append({"role": "assistant", "content": reply})
            cw.messagesend(f"[rp aid={account_id} to={room_id}-{message_id}][pname:{account_id}]さん\n{reply}")
            AI_count += 1
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return jsonify({"status": "ok"}), 200
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
