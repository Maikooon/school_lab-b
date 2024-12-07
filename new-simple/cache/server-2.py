import zmq
import random
import time
from message import Message
from Jwt import *


class Server2:
    def __init__(
        self,
        ip,
        port,
        server1_ip,
        server1_port,
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
        self.command_server_ip = command_server_ip
        self.command_server_port = command_server_port
        self.public_key = public_key  # 公開鍵
        self.alpha = alpha
        self.beta = beta
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
        print(f"1->")
        # 受信した文字列をMessageオブジェクトに変換
        message = Message.from_string(message)
        return message

    def send_message_to_random_server(self, message):
        # サーバ1にメッセージ送信
        print(f"->1")
        self.sender_to_server1.send_string(message.to_string())

    def process_message(self, message):
        total_across_servers = message.across_server
        print(f"Total across_servers: {total_across_servers}")

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

        if total_across_servers == 5:
            print(f"Sending termination message 1 -> 2")
            target_server_ip = "10.58.60.7"  # 次のサーバIP（例）
            new_message = Message(
                ip=self.ip,
                next_id=target_server_ip,
                across_server=message.across_server,  # 命令サーバへの祖神なのでカウントしない
                public_key=self.public_key,
                jwt=message.jwt,  # 実際には有効なJWTを生成する
                end_flag=True,
            )
            self.sender_to_server1.send_string(new_message.to_string())
            return True

    def run(self):
        print("Server is running. Waiting for messages...")
        # メッセージを受信し、ランダムホップを開始
        end_flag = False
        cache = 0
        total_rw_hop_count = 0
        # その後、Server1からのメッセージ待受
        while True:
            try:
                # Server1からのメッセージ受信
                print("Waiting for messages from Server1...")
                message = self.receive_message_from_server1()
                total_rw_hop_count += 1

                # -初めてのメッセージでキャッシュがなかったら検証する
                if cache == 0:
                    print("初めてのメッセージでキャッシュがなかったら検証する")
                    cache = validate_child_token(message.jwt)
                    cache_time = time.perf_counter()
                # -2回目以降のメッセージ
                else:
                    # -- キャッシュを使用する場合
                    if random.random() < 0.5:  # キャッシュを使用して検証
                        print("キャッシュを使用して検証")
                        # キャッシュの有効期限が切れていない
                        # TODO:有効期限を設定
                        if cache_time + 0.125 > time.perf_counter():
                            print("キャッシュの有効期限が切れていないのでそのまま通過")
                        # キャッシュの有効期限が切れている
                        else:
                            print("キャッシュの有効期限が切れているので検証する")
                            # start_time = time.time()
                            cache = validate_child_token(message.jwt)
                            # 時間を更新
                            cache_time = time.perf_counter()  # end_time = time.time()
                            # all_time = end_time - start_time
                            # print("検証にかかった時間", all_time)
                    # 　-- 初めてのサーバになりすまして、キャッシュを使用せず検証する場合
                    else:
                        print(
                            "キャッシュを使用せず検証する,キャッシュは新規サーバのものとして保存"
                        )
                        start_time = time.time()
                        cache_new = validate_child_token(message.jwt)
                        end_time = time.time()
                        all_time = end_time - start_time
                        print("検証にかかった時間", all_time)
                # print("子Tokenの検証結果", jwt_result)
                ############################
                print("-" * 50)
                if total_rw_hop_count == 5:
                    end_flag = True
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
        public_key="Server1_Public_Key",  # 公開鍵
        alpha=0,
        beta=1,
    )
    server2.run()