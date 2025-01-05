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
        rw_count,
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
        self.rw_count = rw_count
        self.context = zmq.Context()

        # 命令サーバとの通信設定
        self.receiver_from_command = self.context.socket(zmq.PULL)
        self.receiver_from_command.connect(
            f"tcp://{self.command_server_ip}:{self.port}"
        )
        self.sender_to_command = self.context.socket(zmq.PUSH)
        self.sender_to_command.connect(
            f"tcp://{self.command_server_ip}:{self.command_server_port}"
        )

        # サーバ2との通信設定
        self.receiver_from_server2 = self.context.socket(zmq.PULL)
        self.receiver_from_server2.bind(f"tcp://{self.ip}:{self.port}")
        self.sender_to_server2 = self.context.socket(zmq.PUSH)
        self.sender_to_server2.connect(f"tcp://{self.server2_ip}:{self.server2_port}")

    def send_initial_message(self):
        # 命令サーバに開始メッセージを送信
        message = Message(
            ip=self.ip,
            next_id=self.server2_ip,
            across_server=0,
            public_key=self.public_key,
            jwt="INITIAL_MESSAGE",
            end_flag=False,
        )
        self.sender_to_command.send_string(message.to_string())
        print("[INFO] Sent initial message to command server.")

    def receive_message(self, socket):
        try:
            message = socket.recv_string()
            return Message.from_string(message)
        except Exception as e:
            print(f"[ERROR] Failed to receive message: {e}")
            return None

    def send_message(self, socket, message):
        try:
            socket.send_string(message.to_string())
            print(f"[INFO] Message sent: {message}")
        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")

    def process_message(self, message):
        if random.random() <= self.alpha:
            # 終了確率に達した場合
            print("[INFO] Termination condition met.")
            message.end_flag = True
            return True

        if random.random() <= self.beta:
            # 他サーバへ送信
            print("[INFO] Sending message to server2.")
            message.across_server += 1
            self.send_message(self.sender_to_server2, message)
            return False
        else:
            print("[INFO] Retrying message processing.")
            return False

    def run(self):
        print("[INFO] Server1 is running...")
        self.send_initial_message()
        total_across_servers = 0

        for _ in range(self.rw_count):
            message = self.receive_message(self.receiver_from_command)
            if not message:
                print("[ERROR] Failed to receive initial command. Skipping...")
                continue

            end_flag = False
            while not end_flag:
                end_flag = self.process_message(message)

            # 終了状態を命令サーバに送信
            total_across_servers += message.across_server
            final_message = Message(
                ip=self.ip,
                next_id=self.server2_ip,
                across_server=total_across_servers,
                public_key=self.public_key,
                jwt="FINAL_MESSAGE",
                end_flag=True,
            )
            self.send_message(self.sender_to_command, final_message)
            print("[INFO] Final message sent to command server.")

        print("[INFO] Server1 process completed.")


if __name__ == "__main__":
    server1 = Server1(
        ip="10.58.60.3",
        port=3200,
        server2_ip="10.58.60.6",
        server2_port=3202,
        command_server_ip="10.58.60.11",
        command_server_port=3203,
        public_key="Server1_Public_Key",
        alpha=0.15,
        beta=0.2,
        rw_count=100,
    )
    server1.run()
