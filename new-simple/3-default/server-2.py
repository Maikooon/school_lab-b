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
        self.public_key = public_key  # 公開鍵
        self.alpha = alpha
        self.beta = beta
        self.context = zmq.Context()

        # サーバ１からのの受信用ソケット（PULL）
        self.receiver_from_server1 = self.context.socket(zmq.PULL)
        self.receiver_from_server1.bind(f"tcp://{self.ip}:{self.port}")
        # サーバ1への送信用ソケット（PUSH）
        self.sender_to_server1 = self.context.socket(zmq.PUSH)
        self.sender_to_server1.connect(f"tcp://{self.server1_ip}:{self.server1_port}")

        # 　サーバ３とのやり取り
        # サーバ１からのの受信用ソケット（PULL）
        self.receiver_from_server3 = self.context.socket(zmq.PULL)
        self.receiver_from_server3.bind(f"tcp://{self.ip}:{self.port}")
        # サーバ1への送信用ソケット（PUSH）
        self.sender_to_server3 = self.context.socket(zmq.PUSH)
        self.sender_to_server3.connect(f"tcp://{self.server3_ip}:{self.server3_port}")

        # 命令サーバ送信用ソケット（PUSH）　　　多分使用されていない
        self.sender_to_command = self.context.socket(zmq.PUSH)
        self.sender_to_command.connect(
            f"tcp://{self.command_server_ip}:{self.command_server_port}"
        )

    # NOTE:サーバ１からの受信
    def receive_message_from_server1(self):
        # サーバ1からメッセージを受信
        message = self.receiver_from_server1.recv_string()
        print(f"1->")
        # 受信した文字列をMessageオブジェクトに変換
        message = Message.from_string(message)
        return message

    # NOTE:サーバ３とのやり取り
    def receive_message_from_server3(self):
        # サーバ3からメッセージを受信
        message = self.receiver_from_server3.recv_string()
        print(f"3->")
        # 受信した文字列をMessageオブジェクトに変換
        message = Message.from_string(message)
        return message

    def send_message_to_random_server(self, message):
        # サーバ1またはサーバ3にランダムでメッセージを送信
        if random.random() < 0.5:
            print("Sending message to Server1")
            self.sender_to_server1.send_string(message.to_string())
        else:
            print("Sending message to Server3")
            self.sender_to_server3.send_string(message.to_string())

    def process_message(self, message):
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

        poller = zmq.Poller()
        poller.register(self.receiver_from_server1, zmq.POLLIN)
        poller.register(self.receiver_from_server3, zmq.POLLIN)
        # その後、Server1からのメッセージ待受
        while True:
            try:
                print("Waiting for messages from Server1 or Server3...")

                # サーバ1またはサーバ3からメッセージを受信
                sockets = dict(poller.poll())

                if self.receiver_from_server1 in sockets:
                    message = self.receive_message_from_server1()
                elif self.receiver_from_server3 in sockets:
                    message = self.receive_message_from_server3()
                else:
                    print("No message received.")
                    continue

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
        port=3202,
        server1_ip="10.58.60.3",
        server1_port=3200,
        server3_ip="10.58.60.5",
        server3_port=3205,
        command_server_ip="10.58.60.11",
        command_server_port=3203,
        public_key="Server1_Public_Key",  # 公開鍵
        alpha=0.15,
        beta=0.3,
    )
    server2.run()
