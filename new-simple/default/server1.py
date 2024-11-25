import zmq
import time
import random
import uuid
from message import Message
import ast


class Server1:
    def __init__(
        self,
        ip,
        port,
        server2_ip,
        server2_port,
        server1_ip,
        alpha=0.15,
        beta=0.3,
        path=[],
        public_key="PublicKeyPlaceholder",  # 公開鍵を受け取る
        start_time=0,
    ):
        self.ip = ip
        self.port = port
        self.server2_ip = server2_ip
        self.server2_port = server2_port
        self.server1_ip = server1_ip
        self.alpha = alpha
        self.beta = beta
        self.path = path
        self.public_key = public_key  # 公開鍵を保存
        self.start_time = start_time
        self.context = zmq.Context()

        # サーバ1の送信用ソケット（PUSH）
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.bind(f"tcp://{self.ip}:{self.port}")

        # サーバ2の受信用ソケット（PULL）
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.connect(f"tcp://{self.server2_ip}:{self.server2_port}")

    def run(self):
        print(f"Server1 started on {self.ip}:{self.port}")

        total_hops = 0
        total_move_server = 0

        self.path.append(self.ip)

        # 初回メッセージを生成して送信
        self.path.append(self.ip)
        initial_message = Message(
            ip=self.ip,
            next_id=self.server2_ip,
            path=self.path,
            public_key=self.public_key,
            jwt="JWT_TOKEN_PLACEHOLDER",
        )
        self.socket.send(bytes(initial_message))
        print("Initial message sent to Server2")

        while True:
            # メッセージを受信
            message = self.receiver.recv()  # 隣のサーバからのメッセージを受信
            # バイト列をデコードして辞書形式に変換
            # JSON文字列に変換
            print(f"Message received at {self.ip}")
            print(f"Message", message)

            decoded_message = message.decode("utf-8")
            message_dict = ast.literal_eval(decoded_message)
            current_start_time = message_dict["start_time"]
            self.start_time = current_start_time
            print(f"current_start_time", current_start_time)

            # 自分のIPをパスに追加
            self.path.append(self.ip)

            # 受け取ったメッセージをRWさせる
            while True:
                # 終了確率をチェック
                end_probability = random.random()
                if end_probability < self.alpha:
                    print("RWを終了します")
                    break
                # サーバ内でのHopか隣のサーバへの移動かを判断
                if random.random() < self.beta:
                    print(f"Hop within {self.ip}")  # サーバ内でのHop
                    continue  # サーバ内で処理を継続
                else:
                    total_move_server += 1
                    # 隣のサーバへメッセージを送信
                    target_server_ip = (
                        self.server2_ip
                        if self.ip == self.server1_ip
                        else self.server1_ip
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
                    self.socket.send(bytes(message))
                    print(f"Message sent to {target_server_ip}")
                    break
                    # このメッセージにおけるこのサーバでのHopは終わり、次にサーバから受信したら行う

                    # 受信待機に戻り、再度ループ
            # 外がわのループも抜けて、メッセージの受信を終わらせる
            if end_probability < self.alpha:
                # start_time = message.start_time
                break

        print("Random walk ended")
        end_time = time.perf_counter()  # 計測終了
        elapsed_time = end_time - start_time  # 経過時間の計算
        print(f"Elapsed time for sending 10 messages: {elapsed_time} seconds")
        print(f"Total hops: {total_hops}")
        print(f"Total move server: {total_move_server}")
        print("path", self.path)


if __name__ == "__main__":

    # # 公開鍵の設定
    # public_key = """
    # -----BEGIN PUBLIC KEY-----
    # MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7Y7wP0KhZEXFGEJTxp7d
    # czpc93LkEd7G3kTOk7K5eAO8ntNNFLWsIbdp67D3tX1HSHJmqtYhpYZdZfzjwO+z
    # ...
    # -----END PUBLIC KEY-----
    # """
    public_key = "PublicKey"
    # Server1のインスタンスを作成し、runメソッドを実行
    server1 = Server1(
        ip="10.58.60.3",
        port=3102,
        server2_ip="10.58.60.6",
        server2_port=3102,
        server1_ip="10.58.60.3",
        public_key=public_key,
        start_time=0,
    )
    server1.run()
