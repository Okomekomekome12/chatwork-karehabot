import requests, json, urllib.parse, time, re, threading

class CW:
    def __init__(self, room_id, myid, cwssid):
        self.room_id  = room_id
        self.myid     = myid
        self.hdrs     = {"Cookie": f"cwssid={cwssid}", "Referer": "https://www.chatwork.com/"}
        self.token    = {"v": None}
        self.send_url = f"https://www.chatwork.com/gateway/send_chat.php?myid={myid}&room_id={room_id}"
        self._start_refresh()
        time.sleep(2)

    def _get_token(self):
        t = re.search(r'ACCESS_TOKEN\s*[=:]\s*["\']([^"\']+)["\']',
                      requests.get("https://www.chatwork.com/", headers=self.hdrs).text)
        return t.group(1) if t else None

    def _start_refresh(self):
        def loop():
            while True:
                t = self._get_token()
                if t:
                    self.token["v"] = t
                    print(f"[token] 更新: {t[:20]}...")
                time.sleep(300)
        threading.Thread(target=loop, daemon=True).start()

    def messagesend(self, text):
        if not self.token["v"]:
            print("[error] トークンなし")
            return
        hdrs = {**self.hdrs, "Content-Type": "application/x-www-form-urlencoded"}
        body = "pdata=" + urllib.parse.quote(json.dumps({"text": text, "_t": self.token["v"]}))
        r    = requests.post(self.send_url, headers=hdrs, data=body)
        res  = r.json()
        if res.get("status", {}).get("success"):
            print(f"[ok] 送信成功: {text}")
        else:
            print(f"[error] {res.get('status', {}).get('message', '不明')}")
        return res

def setup(room_id, myid, cwssid):
    return CW(room_id, myid, cwssid)