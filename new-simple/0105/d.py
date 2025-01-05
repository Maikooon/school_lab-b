import zmq
import random
import time
from message import Message


class Server3:
    def __init__(
        self,
        ip,
        port,
        server2_ip,
        server2_port,
        server1_ip,
        server1_port,
        public_key,
        alpha,
        beta,
    ):
        self.ip = ip
        self.port = port
        self.server2_ip = server2_ip
        self.server2_port = server2_port
        self.server1_ip = server1_ip
        self.server1_port = server1_port
        self.public_key = public_key  # 公開鍵
        self.alpha = alpha
        self.beta = beta
        self.context = zmq.Context()

        # サーバ3の受信用ソケット（PULL）
        self.receiver_from_server2 = self.context.socket(zmq.PULL)
        self.receiver_from_server2.bind(f"tcp://{self.ip}:{self.port}")

        # サーバ2送信用ソケット（PUSH）
        self.sender_to_server2 = self.context.socket(zmq.PUSH)
        self.sender_to_server2.connect(f"tcp://{self.server2_ip}:{self.server2_port}")

        # サーバ1送信用ソケット（PUSH）
        self.sender_to_server1 = self.context.socket(zmq.PUSH)
        self.sender_to_server1.connect(f"tcp://{self.server1_ip}:{self.server1_port}")

    def receive_message_from_server(self):
        # 他のサーバからメッセージを受信
        message = self.receiver_from_server2.recv_string()
        print(f"Message received by Server3: {message}")
        # 受信した文字列をMessageオブジェクトに変換
        message = Message.from_string(message)
        return message

    def send_message_to_random_server(self, message):
        # ランダムにサーバ1またはサーバ2にメッセージ送信
        target_server = random.choice(["server1", "server2"])
        print(f"Sending message to {target_server}")

        if target_server == "server1":
            self.sender_to_server1.send_string(message.to_string())
        else:
            self.sender_to_server2.send_string(message.to_string())

    def process_message(self, message):
        across_server_count = message.across_server
        print(
            f"Processing message at Server3. Current across_server_count: {across_server_count}"
        )

        if random.random() > self.alpha:
            if random.random() < self.beta:
                # 次のサーバにメッセージを送信
                print("Forwarding message to another server.")
                new_message = Message(
                    ip=self.ip,
                    next_id="RandomServer",
                    across_server=message.across_server + 1,
                    public_key=self.public_key,
                    jwt="JWT_TOKEN_PLACEHOLDER",  # 実際には有効なJWTを生成する
                    end_flag=False,
                )
                self.send_message_to_random_server(new_message)
            else:
                print("Message not sent to another server (retry).")
        else:
            print("End flag detected. Processing termination.")
            return True  # 終了

        return False  # 継続

    def run(self):
        print("Server3 is running. Waiting for messages...")
        while True:
            try:
                # 他のサーバからのメッセージを受信
                print("Waiting for messages...")
                message = self.receive_message_from_server()

                # メッセージを処理
                end_flag = self.process_message(message)

                # 終了フラグが立っている場合は終了
                if end_flag:
                    print("Ending server process as instructed.")
                    break

            except Exception as e:
                print(f"Error occurred: {e}")
                break


if __name__ == "__main__":
    server3 = Server3(
        ip="10.58.60.7",
        port=3204,
        server2_ip="10.58.60.6",
        server2_port=3202,
        server1_ip="10.58.60.3",
        server1_port=3200,
        public_key="Server3_Public_Key",  # 公開鍵
        alpha=0.15,
        beta=0.3,
    )
    server3.run()
