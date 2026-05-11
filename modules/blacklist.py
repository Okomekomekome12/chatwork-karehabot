from supabase import create_client

SUPABASE_URL = "https://xzphpphzzbffrdwuzgir.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6cGhwcGh6emJmZnJkd3V6Z2lyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwODAxOTIsImV4cCI6MjA4OTY1NjE5Mn0.L9c5Uz2zB6AZ8joMd1YdsgzxxcVpfiEwvenkbR_qtBE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
def add(account_id):
    data = {"account_id": account_id}
    result = supabase.table("accounts").insert(data).execute()
    print(f"account_id保存完了 : {account_id}")
    return result

def check(cw,account_id):
    result = supabase.table("accounts").select("*").eq("account_id", account_id).execute()
    print(result.data)
    if result.data:
        cw.messagesend("[info][title]圧　倒　的　警　告[/title]このユーザーはブラックリストに登録されているので、閲覧にします()[/info]")
        cw.viewer(account_id)
    else:
        pass

def delete(cw,account_id):
    result = supabase.table("accounts").delete().eq("account_id", account_id).execute()
    cw.messagesend(f"account_id削除完了 : {account_id}")
    return result

def accont_list(cw):
    result = supabase.table("accounts").select("*").execute()
    print(result.data)
    if not result.data:
        cw.messagesend("誰も居ません")
    txt = "[info][title]ブラックリスト一覧[/title]ユーザ:"
    for user in result.data:
        txt += f" [piconname:{user['account_id']}] アカウントID : {user['account_id']}\n" # type: ignore
        
    txt += "[/info]"
    cw.messagesend(txt)
    return result.data
