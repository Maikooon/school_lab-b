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

    def run(self):
        # 初期命令を受信
        self.receive_initial_command()

        # ランダムホップを開始
        message = "Message from Server1"
        hop_count = 0
        while hop_count < self.max_hops:
            self.send_message_to_random_server(message, hop_count)
            hop_count += 1
            time.sleep(1)  # ホップ間の間隔

        # hop_countがmax_hopsに達したら終了、命令サーバに終了メッセージを送信
        termination_message = (
            "Server1 has reached the maximum number of hops. Terminating."
        )
        self.sender_to_command.send_string(termination_message)
        print(termination_message)


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
