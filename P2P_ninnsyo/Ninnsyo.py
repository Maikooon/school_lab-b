import zmq
import jwt  # PyJWTライブラリが必要


# 　これは秘密鍵なので、公開鍵とはことnaru
SECRET_KEY = "your_secret_key"


def generate_jwt(data):
    # JWTを生成する
    token = jwt.encode({"data": data}, SECRET_KEY, algorithm="HS256")
    return token


def start_auth_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)  # REPソケットでクライアントの要求を待つ
    socket.bind("tcp://*:10006")  # ポート10006で接続を待機

    print("認証サーバが起動しました。")

    try:
        while True:
            # クライアントからの認証要求を受信
            message = socket.recv_string()
            print("Received authentication request:", message)

            # JWTを生成して応答として返す
            jwt_token = generate_jwt(message)
            socket.send_string(jwt_token)  # 生成したJWTをクライアントに返送

    finally:
        socket.close()
        context.destroy()


# サーバを起動
start_auth_server()
