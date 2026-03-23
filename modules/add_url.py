from supabase import create_client

SUPABASE_URL = "https://xzphpphzzbffrdwuzgir.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6cGhwcGh6emJmZnJkd3V6Z2lyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwODAxOTIsImV4cCI6MjA4OTY1NjE5Mn0.L9c5Uz2zB6AZ8joMd1YdsgzxxcVpfiEwvenkbR_qtBE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TYPES = {
    "rammerhead": "Rammerhead",
    "utopia": "Utopia",
    "wakame": "わかめtube",
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
    cw.messagesend(f"わかめtubeに追加しました: {body}")

def add_other(body, cw):
    supabase.table("urls").insert({"type": "other", "url": body}).execute()
    cw.messagesend(f"その他に追加しました: {body}")


def delete_rammerhead(body, cw):
    result = supabase.table("urls").delete().eq("type", "rammerhead").eq("url", body).execute()
    if result.data:
        cw.messagesend(f"Rammerheadから削除しました: {body}")
    else:
        cw.messagesend(f"見つかりませんでした: {body}")

def delete_utopia(body, cw):
    result = supabase.table("urls").delete().eq("type", "utopia").eq("url", body).execute()
    if result.data:
        cw.messagesend(f"Utopiaから削除しました: {body}")
    else:
        cw.messagesend(f"見つかりませんでした: {body}")

def delete_wakame(body, cw):
    result = supabase.table("urls").delete().eq("type", "wakame").eq("url", body).execute()
    if result.data:
        cw.messagesend(f"わかめtubeから削除しました: {body}")
    else:
        cw.messagesend(f"見つかりませんでした: {body}")

def delete_other(body, cw):
    result = supabase.table("urls").delete().eq("type", "other").eq("url", body).execute()
    if result.data:
        cw.messagesend(f"その他から削除しました: {body}")
    else:
        cw.messagesend(f"見つかりませんでした: {body}")


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