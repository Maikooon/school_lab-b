import zmq
import time
import random
import uuid
from message import Message


class Server1:
    def __init__(
        self,
        ip,
        port,
        server2_ip,
        server2_port,
        alpha=0.15,
        beta=0.3,
        path=[],
        public_key="PublicKeyPlaceholder",  # 公開鍵を受け取る
    ):
        self.ip = ip
        self.port = port
        self.server2_ip = server2_ip
        self.server2_port = server2_port
        self.alpha = alpha
        self.beta = beta
        self.path = path
        self.public_key = public_key  # 公開鍵を保存
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.bind(f"tcp://{self.ip}:{self.port}")
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.connect(f"tcp://{self.server2_ip}:{self.server2_port}")

    def run(self):
        print(f"Server1 started on {self.ip}:{self.port}")

        total_hops = 0
        total_move_server = 0

        start_time = time.perf_counter()  # 計測開始

        self.path.append(self.ip)
        while True:
            total_hops += 1
            # 終了確立を定義
            if random.random() < self.alpha:
                print("RWを終了します")
                break
            else:
                self.path.append(self.ip)
                if random.random() < self.beta:
                    print("同じサーバ内でHopします")
                else:
                    total_move_server += 1
                    print("サーバ2にメッセージを送ります")

                    # メッセージを生成
                    message_id = str(uuid.uuid4())  # UUIDでメッセージIDを生成
                    message = Message(
                        ip=self.ip,
                        next_id=self.server2_ip,  # 次のサーバのIP
                        path=self.path,
                        public_key=self.public_key,  # 公開鍵
                        jwt="JWT_TOKEN_PLACEHOLDER",  # JWTトークン
                    )

                    # メッセージ送信
                    self.socket.send(bytes(message))  # メッセージをバイトとして送信

        end_time = time.perf_counter()  # 計測終了
        elapsed_time = end_time - start_time  # 経過時間の計算
        print(f"Elapsed time for sending 10 messages: {elapsed_time} seconds")
        print(f"Total hops: {total_hops}")
        print(f"Total move server: {total_move_server}")


if __name__ == "__main__":

    # 公開鍵の設定
    public_key = """
    -----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7Y7wP0KhZEXFGEJTxp7d
    czpc93LkEd7G3kTOk7K5eAO8ntNNFLWsIbdp67D3tX1HSHJmqtYhpYZdZfzjwO+z
    ...
    -----END PUBLIC KEY-----
    """

    # Server1のインスタンスを作成し、runメソッドを実行
    server1 = Server1(
        ip="10.58.60.3",
        port=3102,
        server2_ip="10.58.60.6",
        server2_port=3102,
        public_key=public_key,
    )
    server1.run()
