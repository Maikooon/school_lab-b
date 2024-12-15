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
        server3_ip,
        server3_port,
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
        self.server3_ip = server3_ip
        self.server3_port = server3_port
        self.command_server_ip = command_server_ip
        self.command_server_port = command_server_port
        self.public_key = public_key
        self.alpha = alpha
        self.beta = beta
        self.rw_count = rw_count
        self.context = zmq.Context()

        # サーバ1の受信用ソケット（PULL）  命令サーバの受信
        self.receiver_from_command = self.context.socket(zmq.PULL)
        self.receiver_from_command.connect(
            f"tcp://{self.command_server_ip}:{self.port}"
        )
        # 命令サーバ送信用ソケット（PUSH）
        self.sender_to_command = self.context.socket(zmq.PUSH)
        self.sender_to_command.connect(
            f"tcp://{self.command_server_ip}:{self.command_server_port}"
        )
        #### この二つは、命令サーバとの通信のためのもので、サーバ１に固有

        # サーバ2の受信用ソケット（PULL） サーバ2からの受信
        self.receiver_from_server2 = self.context.socket(zmq.PULL)
        self.receiver_from_server2.bind(f"tcp://{self.ip}:{self.port}")
        # サーバ2送信用ソケット（PUSH）サーバ２への送信
        self.sender_to_server2 = self.context.socket(zmq.PUSH)
        self.sender_to_server2.connect(f"tcp://{self.server2_ip}:{self.server2_port}")

        # サーバ3の受信用ソケット（PULL） サーバ3からの受信
        self.receiver_from_server3 = self.context.socket(zmq.PULL)
        self.receiver_from_server3.bind(f"tcp://{self.ip}:{self.port}")
        # サーバ3送信用ソケット（PUSH）サーバ3への送信
        self.sender_to_server3 = self.context.socket(zmq.PUSH)
        self.sender_to_server3.connect(f"tcp://{self.server3_ip}:{self.server3_port}")

    def receive_initial_command(self):
        # 命令サーバから初期命令を受信
        message = self.receiver_from_command.recv_string()
        print(f"Received initial command")
        return message

    def receive_message_from_server2(self):
        # サーバ2からメッセージを受信
        message = self.receiver_from_server2.recv_string()
        print(f"2->")
        # 受信した文字列をMessageオブジェクトに変換
        message = Message.from_string(message)
        return message

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
            self.sender_to_server2.send_string(message.to_string())
        else:
            print("Sending message to Server3")
            self.sender_to_server3.send_string(message.to_string())

    def process_message(self, message):
        across_server_count = 0
        end_flag = False
        total_across_servers = message.across_server
        print(f"Total across_servers: {total_across_servers}")

        while True:
            # 終了確立よりも大きいときには、継続
            if random.random() > self.alpha:
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
                        end_flag=False,
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
        return end_flag

    def run(self):
        print("Server is running. Waiting for messages...")
        total_move_server = 0

        # 初期命令を受信
        initial_command = self.receive_initial_command()

        # 初期命令に応じた処理（必要に応じて内容変更）
        if initial_command == "START":
            print("initial START ")
            # 以下のメッセージを送ってRWを行う処理を任意の回数繰り返す
            for i in range(self.rw_count):
                # ここで初めてのメッセージを作成して、送信準備
                end_flag = self.process_message(
                    message=Message(
                        ip=self.ip,
                        end_flag=False,
                        next_id=self.server2_ip,
                        across_server=0,
                        public_key=self.public_key,
                        jwt="JWT_TOKEN_PLACE",
                    )
                )
                # 初回でなった時も、終了メッセージを命令さ＝ばに送る
                if end_flag:
                    # 情報量はないが、送受信のフォーマットが決まっているので合わせる
                    message = Message(
                        ip=self.ip,
                        next_id=self.server2_ip,
                        across_server=0,
                        public_key=self.public_key,
                        jwt="JWT_TOKEN_PLACE",
                        end_flag=True,
                    )
                    print("[first]Ending server process as instructed.")
                else:
                    # その後、Server2,3からのメッセージ待受
                    poller = zmq.Poller()
                    poller.register(self.receiver_from_server1, zmq.POLLIN)
                    poller.register(self.receiver_from_server3, zmq.POLLIN)

                    while True:
                        try:
                            # Server2からのメッセージ受信,このメッセージには、終了メッセージも含まれる
                            print("Waiting for messages from Server2...")
                            message = self.receive_message_from_server2()
                            sockets = dict(poller.poll())

                            if self.receiver_from_server1 in sockets:
                                message = self.receive_message_from_server1()
                            elif self.receiver_from_server3 in sockets:
                                message = self.receive_message_from_server3()
                            else:
                                print("No message received.")
                                continue

                            # 継続のメッセージの場合は、メッセージを処理
                            # end_flag = self.process_message(message)
                            # 終了のメッセージの場合は、ループを終了して、新しいメッセージを送信する
                            if message.end_flag:
                                total_move_server += message.across_server
                                end_flag = True
                            else:
                                end_flag = self.process_message(message)
                                total_move_server += message.across_server
                                # ここがTrueなら、終了確立に達したので、終了
                                # Falseなら、tryの継続

                            # 終了指示があればループ終了
                            if end_flag:
                                print("Ending server process as instructed.")
                                # self.sender_to_command.send_string(message.to_string())
                                break

                        except Exception as e:
                            print(f"Error occurred: {e}")
                            break
                print("次の実行に移ります")
            # すべての実行が終わったので、メッセージを送信します
            message = Message(
                ip=self.ip,
                next_id=self.server2_ip,  # このIDはあんまり関係ない
                across_server=total_move_server,
                public_key=self.public_key,
                jwt="JWT_TOKEN_PLACE",
                end_flag=True,
            )
            print("[last]Ending server process as instructed.")
            # print("次のメッセージを命令サーバに送信", message.to_string())
            self.sender_to_command.send_string(message.to_string())


if __name__ == "__main__":
    server1 = Server1(
        ip="10.58.60.3",
        port=3200,
        server2_ip="10.58.60.6",
        server2_port=3202,
        server3_ip="10.58.60.5",
        server3_port=3205,
        command_server_ip="10.58.60.11",
        command_server_port=3203,
        public_key="Server1_Public_Key",  # 公開鍵
        alpha=0.15,  # RWの終了確立
        beta=0.2,
        rw_count=100,
    )
    server1.run()
