# 1. ベースとなるPythonイメージを指定
FROM python:3.10-slim

# 2. コンテナ内の作業ディレクトリを設定
WORKDIR /app

# 3. 依存関係（ライブラリ）のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. アプリケーションコードのコピー
COPY . .

# 5. アプリの起動コマンド（外部アクセスを許可するためポートとホストを指定）
CMD ["python", "index.py", "--host=0.0.0.0", "--port=8080"]
