from supabase import create_client
SUPABASE_URL = "https://xzphpphzzbffrdwuzgir.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6cGhwcGh6emJmZnJkd3V6Z2lyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwODAxOTIsImV4cCI6MjA4OTY1NjE5Mn0.L9c5Uz2zB6AZ8joMd1YdsgzxxcVpfiEwvenkbR_qtBE"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
def commitmsg(cw,commitmsg):
    response = (
        supabase.table("commitmsg")
        .insert({"message": commitmsg})
        .execute()
    )
    cw.messagesend("[info][title]追加完了[/title]追加しました[/info]")