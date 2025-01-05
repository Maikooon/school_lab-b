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
        server3_ip,
        server3_port,
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
        self.server3_ip = server3_ip
        self.server3_port = server3_port
        self.command_server_ip = command_server_ip
        self.command_server_port = command_server_port
        self.public_key = public_key
        self.alpha = alpha
        self.beta = beta
        self.context = zmq.Context()

        # サーバ2の受信用ソケット（PULL）
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.bind(f"tcp://{self.ip}:{self.port}")

        # サーバ1送信用ソケット（PUSH）
        self.sender_to_server1 = self.context.socket(zmq.PUSH)
        self.sender_to_server1.connect(f"tcp://{self.server1_ip}:{self.server1_port}")

        # サーバ3送信用ソケット（PUSH）
        self.sender_to_server3 = self.context.socket(zmq.PUSH)
        self.sender_to_server3.connect(f"tcp://{self.server3_ip}:{self.server3_port}")

        # 命令サーバ送信用ソケット（PUSH）
        self.sender_to_command = self.context.socket(zmq.PUSH)
        self.sender_to_command.connect(
            f"tcp://{self.command_server_ip}:{self.command_server_port}"
        )

    def receive_message(self):
        # 他のサーバからメッセージを受信
        message = self.receiver.recv_string()
        print(f"Message received: {message}")
        return Message.from_string(message)

    def send_message_to_random_server(self, message):
        # サーバ1またはサーバ3にランダムにメッセージ送信
        target_server = random.choice(["server1", "server3"])
        if target_server == "server1":
            print("Sending message to Server1.")
            self.sender_to_server1.send_string(message.to_string())
        else:
            print("Sending message to Server3.")
            self.sender_to_server3.send_string(message.to_string())

    def process_message(self, message):
        # メッセージ処理ロジック
        if random.random() > self.alpha:
            if random.random() < self.beta:
                # 他のサーバに送信
                print("Processing message to send to another server.")
                new_message = Message(
                    ip=self.ip,
                    next_id=message.next_id,
                    across_server=message.across_server + 1,
                    public_key=self.public_key,
                    jwt="JWT_TOKEN_PLACEHOLDER",
                    end_flag=False,
                )
                self.send_message_to_random_server(new_message)
            else:
                print("Message processing skipped (retry).")
        else:
            print("Ending message processing and notifying command server.")
            termination_message = Message(
                ip=self.ip,
                next_id=message.next_id,
                across_server=message.across_server,
                public_key=self.public_key,
                jwt="JWT_TOKEN_PLACEHOLDER",
                end_flag=True,
            )
            self.sender_to_command.send_string(termination_message.to_string())

    def run(self):
        print("Server2 is running. Waiting for messages...")
        while True:
            try:
                # メッセージ受信
                message = self.receive_message()

                # メッセージ処理
                self.process_message(message)
            except Exception as e:
                print(f"Error occurred: {e}")
                break


if __name__ == "__main__":
    server2 = Server2(
        ip="10.58.60.6",
        port=3202,
        server1_ip="10.58.60.3",
        server1_port=3200,
        server3_ip="10.58.60.8",
        server3_port=3204,
        command_server_ip="10.58.60.11",
        command_server_port=3203,
        public_key="Server2_Public_Key",
        alpha=0.15,
        beta=0.3,
    )
    server2.run()
