from flask import Flask

app = Flask(__name__)

# <username>の部分が変数としてビュー関数に渡される
@app.route("/")
def root():
    return "hello world"
@app.route('/user/<username>')
def show_user(username):
    # username変数にURLの文字列が格納されている
    return f'ユーザー名: {username}'

if __name__ == '__main__':
    app.run()
