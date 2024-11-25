import zmq
import time
import random
import uuid
from message import Message


class Server2:
    def __init__(
        self,
        ip,
        port,
        server1_ip,
        server1_port,
        alpha=0.15,
        beta=0.6,
        path=[],
        public_key="PublicKeyPlaceholder",
    ):
        self.ip = ip
        self.port = port
        self.server1_ip = server1_ip
        self.server1_port = server1_port
        self.alpha = alpha
        self.beta = beta
        self.path = path
        self.public_key = public_key
        self.context = zmq.Context()

        # サーバ2の送信用ソケット（PUSH）
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.bind(f"tcp://{self.ip}:{self.port}")

        # サーバ1の受信用ソケット（PULL）
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.connect(f"tcp://{self.server1_ip}:{self.server1_port}")

    def run(self):
        print(f"Server2 started on {self.ip}:{self.port}")
        total_move_server = 0
        total_hops = 0

        while True:
            # メッセージをサーバ1から受け取る
            message = self.receiver.recv()  # サーバ1からメッセージを受信
            print("Server2 received message from Server1")
            self.path.append(self.ip)
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
                    print("サーバ1にメッセージを送ります")

                    # メッセージを生成
                    message = Message(
                        ip=self.ip,
                        next_id=self.server1_ip,  # 次のサーバのIP
                        path=self.path,
                        public_key=self.public_key,  # 公開鍵
                        jwt="JWT_TOKEN_PLACEHOLDER",  # JWTトークン
                    )

                    # メッセージ送信
                    self.socket.send(bytes(message))  # メッセージをバイトとして送信
                    print("メッセージをサーバ1に送信しました")

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

    # Server2のインスタンスを作成し、runメソッドを実行
    server2 = Server2(
        ip="10.58.60.6",
        port=3102,
        server1_ip="10.58.60.3",
        server1_port=3102,
        public_key=public_key,
    )
    server2.run()
