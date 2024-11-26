import zmq
import random
import time


class Server2:
    def __init__(
        self,
        ip,
        port,
        server1_ip,
        server1_port,
        command_server_ip,
        command_server_port,
        max_hops,
    ):
        self.ip = ip
        self.port = port
        self.server1_ip = server1_ip
        self.server1_port = server1_port
        self.command_server_ip = command_server_ip
        self.command_server_port = command_server_port
        self.max_hops = max_hops
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
        return message

    def send_message_to_random_server(self, message, hop_count):
        if hop_count < self.max_hops:
            # サーバ1にメッセージ送信
            print(f"Sending message to Server1 at hop {hop_count + 1}")
            self.sender_to_server1.send_string(message)
        else:
            # 終了メッセージを命令サーバに送信
            termination_message = (
                f"Message reached Server2 after {hop_count} hops. Terminating."
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
                if random.random() < 0.5:
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
            termination_message = f"total {hop_count} hops."
            print(f"Sending termination message: {termination_message}")
            self.sender_to_command.send_string(termination_message)

    def run(self):
        print("Server is running. Waiting for messages...")
        # メッセージを受信し、ランダムホップを開始
        end_flag = False

        # その後、Server2からのメッセージ待受
        while True:
            try:
                # Server2からのメッセージ受信
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
        max_hops=5,  # 最大ホップ数
    )
    server2.run()
