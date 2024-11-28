import zmq
import random
import time
from message import Message
from Jwt import *


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
        print(f"Received initial command")
        return message

    def receive_message_from_server2(self):
        # サーバ2からメッセージを受信
        message = self.receiver_from_server2.recv_string()
        print(f"2->")
        # 受信した文字列をMessageオブジェクトに変換
        message = Message.from_string(message)
        return message

    def send_message_to_random_server(self, message):
        # サーバ2にメッセージ送信
        print(f"Sending to Server2 ")
        # Message オブジェクトを文字列化して送信
        self.sender_to_server2.send_string(message.to_string())

    def process_message(self, message):
        across_server_count = 0
        end_flag = False

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
                        jwt=message.jwt,  # 実際には有効なJWTを生成する
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
                # 初回のみTokenを得るためにサーバと通信する
                # TODO:Tokenを得るための処理
                print(
                    "認証サーバと通信しますーーーーーーーーーーーーーーーーーーーーーーー"
                )
                context = zmq.Context()
                socket = context.socket(zmq.REQ)
                socket.connect("tcp://10.58.60.5:10009")
                start_time_jwt_connected = time.perf_counter()  # 　時間を計測
                message_for_ninsyo = "ここに認証したい文字列を入れる"  # 例としてnode_idとvalを文字列に変換
                socket.send_string(message_for_ninsyo)  # 認証要求を送信
                # サーバからの応答を受け取る
                response = socket.recv_string()
                print("Received JWT from server:", response)  # 受け取ったJWTを表示
                jwt = response  # 受け取ったJWTを変数に格納
                socket.close()
                context.destroy()
                ##########################################################
                print("認証サーバとの通信が終了しました")
                # ここで初めてのメッセージを作成して、送信準備
                end_flag = self.process_message(
                    message=Message(
                        ip=self.ip,
                        end_flag=False,
                        next_id=self.server2_ip,
                        across_server=0,
                        public_key=self.public_key,
                        jwt=jwt,
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
                        jwt=jwt,
                        end_flag=True,
                    )
                    print("[first]Ending server process as instructed.")
                    # 次のRW実行に移る
                    # break
                else:
                    # その後、Server2からのメッセージ待受
                    while True:
                        try:
                            # Server2からのメッセージ受信
                            print("Waiting for messages from Server2...")
                            message = self.receive_message_from_server2()

                            # 継続のメッセージの場合は、メッセージを処理
                            # end_flag = self.process_message(message)
                            # 終了のメッセージの場合は、ループを終了して、新しいメッセージを送信する
                            if message.end_flag:
                                total_move_server += message.across_server
                                end_flag = True
                            else:
                                # TODO: JWTの検証を行う
                                start_time_jwt_verify = (
                                    time.perf_counter()
                                )  # 　時間を計測
                                print(message.jwt)
                                jwt_result = verify_jwt(message.jwt)
                                end_time_jwt_verify = time.perf_counter()
                                elapsed_time_jwt_verify = (
                                    end_time_jwt_verify - start_time_jwt_verify
                                )
                                print("JWT検証結果", jwt_result)
                                #####ここでTokenを検証する############################################################################
                                ############################
                                end_flag = self.process_message(message)
                                if end_flag:
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
                next_id=self.server2_ip,
                across_server=total_move_server,
                public_key=self.public_key,
                jwt=jwt,
                end_flag=True,
            )
            print("[last]Ending server process as instructed.")
            self.sender_to_command.send_string(message.to_string())


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
        beta=0.5,
        rw_count=100,
    )
    server1.run()
