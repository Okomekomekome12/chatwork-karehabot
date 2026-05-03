import requests

def check_status(cw):
    url = "https://raw.githubusercontent.com/senninsugar/Ytdlp-check/refs/heads/main/all/all.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        last_update = data.get("last_update", "不明")
        apis = data.get("apis", [])
        
        status_text = f"[info][title]Ytdlp 稼働状況[/title]最終更新: {last_update}\n"
        for api in apis:
            name = api.get("name")
            status = api.get("status")
            status_text += f"・{name}: {status}\n"
        status_text += "[/info]"
        
        cw.messagesend(status_text)
    except Exception as e:
        cw.messagesend(f"[info][title]エラー[/title]ステータスの取得に失敗しました。[/info]")
