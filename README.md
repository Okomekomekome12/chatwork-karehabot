# chatwork-karehabot
Pythonのflask、requestsなどを使用してbotを作ります
## 機能一覧

/startmath : +、-、×、÷の中からランダムに出題します

/add-rammerhead /add-utopia /add-wakame /add-other : コマンドを入力した後にリンクを載せて登録してください

/link : 登録されたリンク一覧を表示します

後　は　め　ん　ど　く　さ　い　か　ら　書　き　ま　せ　ん


# no_api_cw

> ⚠️ **非公式ライブラリです。Chatworkの公式APIとは無関係です。自己責任でご利用ください。**

ChatworkのAPIキー不要で動くメッセージ送信ライブラリ。

---

## 関連リンク

- [Chatwork](https://www.chatwork.com/)
- [Chatwork 公式API](https://developer.chatwork.com/)
- [no_api_cw GitHub](https://github.com/Okomekomekome12/chatwork-karehabot)

---

## 使用エンドポイント

| 用途 | URL |
|------|-----|
| トークン取得 | `https://www.chatwork.com/` |
| メッセージ送信 | `https://www.chatwork.com/gateway/send_chat.php?myid={myid}&room_id={room_id}` |

---

## セットアップ

```bash
pip install requests
```

`no_api_cw.py` をプロジェクトに置く。

---

## 使い方

```python
import no_api_cw

cw = no_api_cw.setup(ルームID, アカウントID, "cwssid")
cw.messagesend("hello world!")
```

---

## cwssidの取得方法

1. Chatworkにブラウザでログイン
2. F12 → Applicationタブ → Cookies
3. `cwssid` の値をコピー

---

## ルームID / アカウントIDの取得方法

URLから取得できる。

```
https://www.chatwork.com/#!rid440818030
                                ^^^^^^^^^ ルームID

F12 → Console
> MYID
  10870480  ← アカウントID
```

---

## 仕組み

```
1. cwssidでChatworkにアクセス
2. ページからACCESS_TOKENを抽出
3. 5分ごとにトークンを自動更新
4. send_chat.phpにPOSTしてメッセージ送信
```

---

## 出力例

```
[token] 更新: abcdefghij12345678901...
[ok] 送信成功: hello world!
[error] INVALID TOKEN
```

---

## 注意

- cwssidはセッションが切れると無効になる
- ループで動かし続ける場合はトークンが自動更新される
- 短時間に大量送信するとBANされる可能性あり