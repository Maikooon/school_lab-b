import zmq
import random
import time
from message import Message


class Server2:
    def __init__(
        self,
        ip,
        port,
        server1_ip,
        server1_port,
        command_server_ip,
        command_server_port,
        public_key,
        alpha,
        beta,
    ):
        self.ip = ip
        self.port = port
        self.server1_ip = server1_ip
        self.server1_port = server1_port
        self.command_server_ip = command_server_ip
        self.command_server_port = command_server_port
        self.public_key = public_key  # 公開鍵
        self.alpha = alpha
        self.beta = beta
        self.context = zmq.Context()

        # サーバ2の受信用ソケット（PULL）
        self.receiver_from_server1 = self.context.socket(zmq.PULL)
        self.receiver_from_server1.bind(f"tcp://{self.ip}:{self.port}")

        # サーバ1送信用ソケット（PUSH）
        self.sender_to_server1 = self.context.socket(zmq.PUSH)
        self.sender_to_server1.connect(f"tcp://{self.server1_ip}:{self.server1_port}")

        # 命令サーバ送信用ソケット（PUSH）
        self.sender_to_command = self.context.socket(zmq.PUSH)
        self.sender_to_command.connect(
            f"tcp://{self.command_server_ip}:{self.command_server_port}"
        )

    def receive_message_from_server1(self):
        # サーバ1からメッセージを受信
        message = self.receiver_from_server1.recv_string()
        print(f"Received message from Server1: {message}")
        # 受信した文字列をMessageオブジェクトに変換
        message = Message.from_string(message)
        return message

    def send_message_to_random_server(self, message):
        # サーバ1にメッセージ送信
        print(f"Sending to Server1")
        self.sender_to_server1.send_string(message.to_string())

    def process_message(self, message):
        print(f"Processing message: {message}")
        across_server_count = 0
        end_flag = False
        total_across_servers = message.across_server
        print(f"Total across_servers: {total_across_servers}")

        while True:
            # 終了確率をチェック
            if random.random() > self.alpha:
                if random.random() < self.beta:
                    # 他のサーバにメッセージを送信
                    # パスに現在のIDを追加し、次のサーバに送信
                    target_server_ip = "10.58.60.7"  # 次のサーバIP（例）
                    new_message = Message(
                        ip=self.ip,
                        next_id=target_server_ip,
                        across_server=message.across_server + 1,
                        public_key=self.public_key,
                        jwt="JWT_TOKEN_PLACEHOLDER",  # 実際には有効なJWTを生成する
                        end_flag=False,
                    )
                    self.send_message_to_random_server(new_message)
                    break  # メッセージを送信したら終了
                else:
                    print("Message not sent to the other server (retry).")
            else:
                print("Message not sent to the other server. Ending process.")
                print(f"Sending termination message 1 -> 2")
                target_server_ip = "10.58.60.7"  # 次のサーバIP（例）
                new_message = Message(
                    ip=self.ip,
                    next_id=target_server_ip,
                    across_server=message.across_server,  # 命令サーバへの祖神なのでカウントしない
                    public_key=self.public_key,
                    jwt="JWT_TOKEN_PLACEHOLDER",  # 実際には有効なJWTを生成する
                    end_flag=True,
                )
                self.sender_to_server1.send_string(new_message.to_string())
                break  # 送信せず終了

    def run(self):
        print("Server is running. Waiting for messages...")
        # メッセージを受信し、ランダムホップを開始
        end_flag = False

        # その後、Server1からのメッセージ待受
        while True:
            try:
                # Server1からのメッセージ受信
                print("Waiting for messages from Server1...")
                message = self.receive_message_from_server1()
                print(f"Received: {message}")

                # メッセージを処理
                end_flag = self.process_message(message)

                # 終了指示があればループ終了
                if end_flag:
                    print("Ending server process as instructed.")
                    break

            except Exception as e:
                print(f"Error occurred: {e}")
                break


if __name__ == "__main__":
    server2 = Server2(
        ip="10.58.60.6",
        port=3102,
        server1_ip="10.58.60.3",
        server1_port=3100,
        command_server_ip="10.58.60.11",
        command_server_port=3103,
        public_key="Server1_Public_Key",  # 公開鍵
        alpha=0.15,
        beta=0.5,
    )
    server2.run()
