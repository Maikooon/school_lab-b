import zmq
import random
import time


class Server1:
    def __init__(
        self,
        ip,
        port,
        server2_ip,
        server2_port,
        command_server_ip,
        command_server_port,
        max_hops,
    ):
        self.ip = ip
        self.port = port
        self.server2_ip = server2_ip
        self.server2_port = server2_port
        self.command_server_ip = command_server_ip
        self.command_server_port = command_server_port
        self.max_hops = max_hops  # 最大ホップ数
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
        # サーバ1からメッセージを受信
        message = self.receiver_from_server2.recv_string()
        print(f"Received message from Server1: {message}")
        return message

    def send_message_to_random_server(self, message, hop_count):
        if hop_count < self.max_hops:
            # サーバ2にメッセージ送信
            print(f"Sending message to Server2 at hop {hop_count + 1}")
            self.sender_to_server2.send_string(message)
        else:
            # 終了メッセージを命令サーバに送信
            termination_message = (
                f"Message reached Server1 after {hop_count} hops. Terminating."
            )
            self.sender_to_command.send_string(termination_message)
            print(termination_message)

    def process_message(self, message):
        print(f"Processing message: {message}")
        hop_count = 0
        end_flag = False

        while True:
            if random.random() < 0.5:
                hop_count += 1
                other_server_probability = random.random()
                if other_server_probability < 0.9:
                    # 他のサーバにメッセージを送信
                    print(f"Sending message to the other server (hop {hop_count + 1})")
                    self.send_message_to_random_server(message, hop_count)
                    break  # メッセージを送信したら終了
                else:
                    print("Message not sent to the other server (retry).")
            else:
                print("Message not sent to the other server. Ending process.")
                end_flag = True
                break  # 送信せず終了

        # 必要に応じて命令サーバに終了メッセージを送信
        if end_flag:
            termination_message = f" {hop_count} hops."
            print(
                f"Sending termination message to Command Server: {termination_message}"
            )
            self.sender_to_command.send_string(termination_message)

    def run(self):
        print("Server is running. Waiting for messages...")

        # 初期命令を受信
        initial_command = self.receive_initial_command()

        # 初期命令に応じた処理（必要に応じて内容変更）
        if initial_command == "START":
            print("initial START ")
            self.process_message("Initial START command processed")

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
        max_hops=5,  # 最大ホップ数
    )
    server1.run()
