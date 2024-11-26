import zmq
import time


class CommandServer:
    def __init__(self, ip, send_port, receive_port):
        self.ip = ip
        self.send_port = send_port
        self.receive_port = receive_port
        self.context = zmq.Context()

        # サーバ1への命令送信用ソケット
        self.sender = self.context.socket(zmq.PUSH)
        self.sender.bind(f"tcp://{self.ip}:{self.send_port}")

        # 終了メッセージを受信用ソケット
        self.receiver = self.context.socket(zmq.PULL)
        self.receiver.bind(f"tcp://{self.ip}:{self.receive_port}")

    def send_initial_command(self, message):
        # サーバ1に初期命令を送信
        print(f"Sending initial command to Server1: {message}")
        self.sender.send_string(message)

    def receive_termination_message(self):
        # 終了メッセージを受信
        message = self.receiver.recv_string()
        print(f"Received termination message: {message}")

    def run(self):
        start_time = time.perf_counter()
        # サーバ1に命令を送信
        self.send_initial_command("START")

        # 終了メッセージを受信
        self.receive_termination_message()
        print("メッセージを受信しました", self.ip)
        end_time = time.perf_counter()
        elast_time = end_time - start_time
        print(f"経過時間: {elast_time}秒")


if __name__ == "__main__":
    command_server = CommandServer(ip="10.58.60.11", send_port=3100, receive_port=3103)
    command_server.run()
