import zmq
import random
import time
from message import Message


class Server1:
    def __init__(
        self,
        ip,
        port,
        server2_ip,
        server2_port,
        command_server_ip,
        command_server_port,
        public_key,
        alpha,
        beta,
    ):
        self.ip = ip
        self.port = port
        self.server2_ip = server2_ip
        self.server2_port = server2_port
        self.command_server_ip = command_server_ip
        self.command_server_port = command_server_port
        self.public_key = public_key
        self.alpha = alpha
        self.beta = beta
        self.context = zmq.Context()

        # サーバ1の受信用ソケット（PULL）
        self.receiver_from_command = self.context.socket(zmq.PULL)
        self.receiver_from_command.connect(
            f"tcp://{self.command_server_ip}:{self.port}"
        )
        # サーバ2の受信用ソケット（PULL）
        self.receiver_from_server2 = self.context.socket(zmq.PULL)
        self.receiver_from_server2.bind(f"tcp://{self.ip}:{self.port}")

        # サーバ2送信用ソケット（PUSH）
        self.sender_to_server2 = self.context.socket(zmq.PUSH)
        self.sender_to_server2.connect(f"tcp://{self.server2_ip}:{self.server2_port}")

        # 命令サーバ送信用ソケット（PUSH）
        self.sender_to_command = self.context.socket(zmq.PUSH)
        self.sender_to_command.connect(
            f"tcp://{self.command_server_ip}:{self.command_server_port}"
        )

    def receive_initial_command(self):
        # 命令サーバから初期命令を受信
        message = self.receiver_from_command.recv_string()
        print(f"Received initial command: {message}")
        return message

    def receive_message_from_server2(self):
        # サーバ2からメッセージを受信
        message = self.receiver_from_server2.recv_string()
        print(f"Received message from Server1: {message}")
        # 受信した文字列をMessageオブジェクトに変換
        message = Message.from_string(message)

        return Message(
            ip=self.server2_ip,
            next_id=self.ip,
            across_server=message.across_server,  # そのまま
            public_key="Server1_Public_Key",
            jwt="Dummy_JWT_Token",
        )

    def send_message_to_random_server(self, message):
        # サーバ2にメッセージ送信
        print(f"Sending to Server2 ")
        # Message オブジェクトを文字列化して送信
        self.sender_to_server2.send_string(message.to_string())

    def process_message(self, message):
        print(f"Processing message: {message}")
        across_server_count = 0
        end_flag = False

        while True:
            # 終了確立よりも大きいときには、継続
            if random.random() < self.alpha:
                other_server_probability = random.random()
                # 他のサーバに遷移する確立を計算、ここでまたぎ回数をコントロールする
                if other_server_probability < self.beta:
                    # 他のサーバにメッセージを送信
                    print(
                        f"Sending message to the other server (across_server {across_server_count + 1})"
                    )
                    target_server_ip = "10.58.60.7"  # 次のサーバIP（例）
                    new_message = Message(
                        ip=self.ip,
                        next_id=target_server_ip,
                        across_server=message.across_server + 1,
                        public_key=self.public_key,
                        jwt="JWT_TOKEN_PLACEHOLDER",  # 実際には有効なJWTを生成する
                    )
                    self.send_message_to_random_server(new_message)
                    print(new_message.jwt)
                    break  # メッセージを送信したら終了
                else:
                    print("Message not sent to the other server (retry).")
            # 終了確立に達したので終了する
            else:
                print("Message not sent to the other server. Ending process.")
                end_flag = True
                break  # 送信せず終了

        # 必要に応じて命令サーバに終了メッセージを送信
        if end_flag:
            print(f"Sending termination message")
            self.sender_to_command.send_string(message.to_string())

    def run(self):
        print("Server is running. Waiting for messages...")

        # 初期命令を受信
        initial_command = self.receive_initial_command()

        # 初期命令に応じた処理（必要に応じて内容変更）
        if initial_command == "START":
            print("initial START ")
            # ここで初めてのメッセージを作成して、送信準備
            self.process_message(
                message=Message(
                    ip=self.ip,
                    next_id=self.server2_ip,
                    across_server=0,
                    public_key=self.public_key,
                    jwt="JWT_TOKEN_PLACE",
                )
            )

        # その後、Server2からのメッセージ待受
        while True:
            try:
                # Server2からのメッセージ受信
                print("Waiting for messages from Server2...")
                message = self.receive_message_from_server2()
                print(f"Received from 2: {message}")

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
    server1 = Server1(
        ip="10.58.60.3",
        port=3100,
        server2_ip="10.58.60.6",
        server2_port=3102,
        command_server_ip="10.58.60.11",
        command_server_port=3103,
        public_key="Server1_Public_Key",  # 公開鍵
        alpha=0.15,
    )
    server1.run()
