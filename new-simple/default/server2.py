import zmq
import time
import random
import uuid
from message import Message
import ast


class Server2:
    def __init__(
        self,
        ip,
        port,
        server1_ip,
        server1_port,
        server2_ip,
        alpha=0.15,
        beta=0.6,
        path=[],
        public_key="PublicKeyPlaceholder",
        start_time=0,
    ):
        self.ip = ip
        self.port = port
        self.server1_ip = server1_ip
        self.server1_port = server1_port
        self.server2_ip = server2_ip
        self.alpha = alpha
        self.beta = beta
        self.path = path
        self.public_key = public_key
        self.start_time = start_time
        self.context = zmq.Context()

        # サーバ2の送信用ソケット（PUSH）
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.bind(f"tcp://{self.ip}:{self.port}")

        # サーバ1の受信用ソケット（PULL）
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.connect(f"tcp://{self.server1_ip}:{self.server1_port}")

    def run(self):
        print(f"Server2 started on {self.ip}:{self.port}")
        first = 0

        # メッセージをサーバ1またはサーバ2から受け取る
        while True:
            message = self.receiver.recv()  # メッセージを受信

            # バイト列をデコードして辞書形式に変換
            decoded_message = message.decode("utf-8")
            message_dict = ast.literal_eval(decoded_message)
            current_start_time = message_dict["start_time"]
            print(f"current_start_time", current_start_time)

            # メッセージの中に現在の時刻を入れておく
            # 初めの一回のみ、時間を保存
            print(f"Message", message)
            if first == 1:
                message_dict["start_time"] = time.time()
            first = 1
            print(f"Message received at {self.ip}")

            # 自分のIPをパスに追加
            self.path.append(self.ip)

            while True:  # 受け取ったメッセージでRWを行うコード
                # 終了確率をチェック
                end_probability = random.random()
                if end_probability < self.alpha:
                    print(f"Random walk ending at {self.ip}")
                    break

                # サーバ内でのHopか隣のサーバへの移動かを判断
                if random.random() < self.beta:
                    # 同じサーバ内でのHop
                    print(f"Hop within {self.ip}")
                    continue  # サーバ内で処理を続行
                else:
                    # 隣のサーバへメッセージを送信
                    target_server_ip = (
                        self.server1_ip
                        if self.ip == self.server2_ip
                        else self.server2_ip
                    )
                    print(f"Sending message to {target_server_ip}")

                    # 新しいメッセージを生成
                    message = Message(
                        ip=self.ip,
                        next_id=target_server_ip,  # 次のサーバのIP
                        path=self.path,
                        public_key=self.public_key,  # 公開鍵
                        jwt="JWT_TOKEN_PLACEHOLDER",  # JWTトークン
                        start_time=self.start_time,
                    )

                    # メッセージ送信
                    self.socket.send(bytes(message))  # メッセージをバイトとして送信
                    print(f"Message sent to {target_server_ip}")
                    break

                    # 再び受信を待機してループを続行
            if end_probability < self.alpha:
                break

        print("Random walk ended")
        end_time = time.perf_counter()  # 計測終了
        elapsed_time = end_time - self.start_time  # 経過時間の計算
        print(f"Elapsed time: {elapsed_time} seconds")


if __name__ == "__main__":

    # 公開鍵の設定
    # public_key = """
    # -----BEGIN PUBLIC KEY-----
    # MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7Y7wP0KhZEXFGEJTxp7d
    # czpc93LkEd7G3kTOk7K5eAO8ntNNFLWsIbdp67D3tX1HSHJmqtYhpYZdZfzjwO+z
    # ...
    # -----END PUBLIC KEY-----
    # """
    public_key = "PublicKey"

    # Server2のインスタンスを作成し、runメソッドを実行
    server2 = Server2(
        ip="10.58.60.6",
        port=3102,
        server1_ip="10.58.60.3",
        server1_port=3102,
        server2_ip="10.58.60.6",
        public_key=public_key,
        start_time=0,
    )
    server2.run()
