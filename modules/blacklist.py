from supabase import create_client

SUPABASE_URL = "chatwork-karehabot/modules/add_url.py"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6cGhwcGh6emJmZnJkd3V6Z2lyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwODAxOTIsImV4cCI6MjA4OTY1NjE5Mn0.L9c5Uz2zB6AZ8joMd1YdsgzxxcVpfiEwvenkbR_qtBE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
def add(account_id):
    data = {"account_id": account_id}
    result = supabase.table("accounts").insert(data).execute()
    print(f"account_id保存完了 : {account_id}")
    return result
def check(cw,account_id):
    result = supabase.table("accounts").select("*").eq("account_id", account_id).execute()
    