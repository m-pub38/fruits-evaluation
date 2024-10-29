# ベースイメージを指定する
FROM python:3.9-slim

# 作業ディレクトリを設定する
WORKDIR /app

# ライブラリをインストールする
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt -y update && apt -y upgrade
RUN apt -y install libopencv-dev

# ソースコードをコンテナにコピーする
COPY . .

# エントリーポイントを設定する
ENTRYPOINT ["python", "main.py"]
