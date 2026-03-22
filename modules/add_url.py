from supabase import create_client

SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TYPES = {
    "rammerhead": "Rammerhead",
    "utopia": "Utopia",
    "wakame": "Wakame",
    "other": "その他"
}


def add_rammerhead(body, cw):
    supabase.table("urls").insert({"type": "rammerhead", "url": body}).execute()
    cw.messagesend(f"Rammerheadに追加しました: {body}")

def add_utopia(body, cw):
    supabase.table("urls").insert({"type": "utopia", "url": body}).execute()
    cw.messagesend(f"Utopiaに追加しました: {body}")

def add_wakame(body, cw):
    supabase.table("urls").insert({"type": "wakame", "url": body}).execute()
    cw.messagesend(f"Wakameに追加しました: {body}")

def add_other(body, cw):
    supabase.table("urls").insert({"type": "other", "url": body}).execute()
    cw.messagesend(f"その他に追加しました: {body}")


def show_list(cw):
    result = supabase.table("urls").select("*").execute()
    data = result.data

    message = "[info][title]リンク一覧[/title]"
    for url_type, name in TYPES.items():
        urls = [row["url"] for row in data if row["type"] == url_type] # type: ignore
        url_text = "\n".join(f"・{url}" for url in urls) if urls else "なし"
        message += f"[info]【{name}】\n{url_text}[/info]"
    message += "[/info]"

    cw.messagesend(message)