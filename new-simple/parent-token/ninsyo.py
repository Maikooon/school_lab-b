import zmq
import jwt  # PyJWTがインストールされていることを前提
import time
import os
import datetime

SECRET_KEY = "your_secret_key"  # JWT用のシークレットキー
LOG_FILE_PATH = "./auth_server_logs.txt"  # ログファイルのパス


# def generate_jwt(message):
#     # JWTのペイロードに必要なデータを追加
#     payload = {"message": message, "timestamp": int(time.time())}
#     # JWTを生成
#     jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
#     return jwt_token


def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=0),  # TODO: 有効期限を0にして失敗するか確認
        "iat": datetime.datetime.utcnow(),  # 発行時刻
    }
    print(payload)
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print("これが使用されています！")
    return token


def save_to_log(message, jwt_token, elapsed_time):
    # ログデータをファイルに保存
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(f"Time taken generate: {elapsed_time:.4f} seconds\n")
        log_file.write("-" * 40 + "\n")


def start_auth_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)  # REPソケットでクライアントの要求を待つ
    socket.bind("tcp://10.58.60.5:10006")  # ポート10006で接続を待機

    print("認証サーバが起動しました。")

    try:
        while True:
            # クライアントからの認証要求を受信
            message = socket.recv_string()
            print("Received authentication request:", message)

            # 時間計測開始
            start_time = time.time()
            # JWTを生成して応答として返す
            jwt_token = generate_jwt(message)
            # 時間計測終了
            elapsed_time = time.time() - start_time

            # 生成されたJWTがバイト形式であれば文字列に変換
            jwt_token = (
                jwt_token.decode("utf-8") if isinstance(jwt_token, bytes) else jwt_token
            )
            print("Generated JWT----------------------------:", jwt_token)

            # 生成したJWTをクライアントに返送
            socket.send_string(jwt_token)
            print("Sent JWT to client.")

            # ログをファイルに保存
            save_to_log(message, jwt_token, elapsed_time)

    except Exception as e:
        print("Error:", e)

    finally:
        socket.close()
        context.destroy()


if __name__ == "__main__":
    # ログファイルが存在しない場合は作成
    if not os.path.exists(LOG_FILE_PATH):
        open(LOG_FILE_PATH, "w").close()

    start_auth_server()
