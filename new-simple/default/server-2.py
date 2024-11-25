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

    def run(self):
        # メッセージを受信し、ランダムホップを開始
        hop_count = 0
        while hop_count < self.max_hops:
            message = self.receive_message_from_server1()
            self.send_message_to_random_server(message, hop_count)
            hop_count += 1
            time.sleep(1)  # ホップ間の間隔
        # hop_countがmax_hopsに達したら終了、命令サーバに終了メッセージを送信
        termination_message = "Message reached Server2 after 5 hops. Terminating."
        self.sender_to_command.send_string(termination_message)
        print(termination_message)


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
