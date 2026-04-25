import os
import chatwork
import time
from flask import Flask, request, jsonify, render_template
from modules import add_url, math

app = Flask(__name__)
API_TOKEN = os.getenv("API_TOKEN")
SECRET_TOKEN = None
shutdown = False
user_state = {}
BOT_ACCOUNT_ID = 11156582 # ←ここに正しいBotのIDを入れる
@app.route("/", methods=["GET"])
def health():
    return render_template('index.html')


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-ChatWorkWebhookSignature")
    if not chatwork.webhook_verify_signature(request.data, signature, SECRET_TOKEN): # type: ignore
        return "invalid signature", 403

    data = request.json
    room_id    = chatwork.webhook_get_roomid(data)
    body       = chatwork.webhook_get_message(data)
    account_id = chatwork.webhook_get_account_id(data)
    message_id = chatwork.webhook_get_message_id(data)

    # デバッグログ
    print(f"\n=== Webhook受信 ===")
    print(f"account_id: {account_id}")
    print(f"body: {body}")  # 最初の50文字
    print(f"BOT_ID: {BOT_ACCOUNT_ID}")
    print(f"一致?: {int(account_id) == BOT_ACCOUNT_ID}")
    print(f"==================\n")
    global shutdown
    cw = chatwork.setup(room_id, API_TOKEN)
    cw2 = chatwork.setup(420107748,API_TOKEN)
    log_room = chatwork.setup(418992889,API_TOKEN)
    if int(account_id) == BOT_ACCOUNT_ID:
        print("→ Bot自身のメッセージなのでスキップ")
        return jsonify({"status": "ok"}), 200
    log_room.messagesend(f"[info][title][piconname:{account_id}]のメッセージ \nメッセリンク→https://www.chatwork.com/#!rid{room_id}-{message_id}[/title][code]{body}[/code][/info]")
    if body == "/start":
        cw.messagesend("起動します")
        shutdown = False
        return jsonify({"status": "ok"}), 200
    
    if shutdown == True:
        print("シャットダウン中なのでスキップ")
        return jsonify({"status": "ok"}), 200
    
    
    if body and (body.count("(quick)") >= 10 or body.count(":*") >= 10):
        cw.viewer(account_id)
        cw.messagesend("[info][title]荒らし検知[/title]荒らしを検知しました、流します[/info]")
        for i in range(70):
            cw.messagesend("a")
            time.sleep(0.7)
        message_link = cw.get_message_link()
        cw.messagesend("[info][title]荒らし対処完了[/title]寝の部屋にメッセージリンクを配布します[/info]")
        cw2.messagesend(f"[info][title]メッセリンク配布[/title]{message_link}[/info]")
    elif body == "/live?":
        cw.messagesend("[info][title]荒らし対策bot正常稼働中[/title]生きてるお[/info]")

    #コンタクト承認

    chatwork.auto_accept_contacts(API_TOKEN)
    # 自分のメッセージは無視
    if body == "/readme":
        cw.messagesend("このbotを導入したいと思ったことはありますよねぇ！？そうですよねぇ！？（圧）\n")

    chatwork.auto_accept_contacts(API_TOKEN)
    
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
        cw.delete_message(deleter_room_id,deleter_message_id)

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
    elif body == "/助けて":
        cw.messagesend(f"[rp aid={account_id} to={room_id}-{message_id}][pname:{account_id}]さん\
[info][title]これはカレハbotのコマンド一覧だよ、よく読め([/title]\
[info][info]/startmath : 簡単()な計算問題を出してきます[/info][/info]\
[hr]\
[info][info]/助けて : cwbotとコマンド重なるのでこれ()[/info][/info]\
[hr]\
[info][info]/update : アップデートしたら乗せるお[/info][/info]\
[hr]\
[info][info]/add-rammerhead /add-utopia /add-wakame /add-other : リスト一覧に追加します[/info][/info]\
[hr]\
[info][info]/delete-rammerhead /delete-utopia /delete-wakame /delete-other : リスト一覧から削除します[/info][/info]\
[hr]\
[info][info]/link: リンク一覧を表示します[/info][/info]\
[hr]\
[info][info]/live? : 荒らし対策botの稼働確認です[/info][/info]\
[hr]\
[info][info]/readme : 読　ん　で　ね[/info][/info]\
[info][info]botが送信したメッセージに対して削除と返信 : メッセージが消えます[/info][/info]\
[hr]\
[/info]"
)
    elif body == "/update":
        cw.messagesend("[info][title]アップデート情報[/title]\
shutdownコマンド、toall検知、ログ機能追加！！！！[/info]")
    elif body == "/link":
        add_url.show_list(cw)
    elif body == "/add-rammerhead":
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
    
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)