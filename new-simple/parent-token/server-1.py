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
        parent_token,
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
        self.parent_token = parent_token
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

    def request_jwt_from_server(self, server_address, auth_message, timeout=5):
        """
        認証サーバと通信してJWTトークンを取得する関数。

        Args:
            server_address (str): 認証サーバのアドレス (例: "tcp://10.58.60.5:10006")
            auth_message (str): 認証要求メッセージ
            timeout (int): サーバからの応答待機時間（秒）

        Returns:
            str: JWTトークン（成功時）
            None: エラー発生時
        """
        try:
            # ZMQ通信のセットアップ
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect(server_address)
            socket.setsockopt(
                zmq.RCVTIMEO, timeout * 1000
            )  # タイムアウト設定（ミリ秒）

            # 認証要求を送信
            start_time = time.perf_counter()
            socket.send_string(auth_message)

            # サーバからの応答を受信
            jwt_token = socket.recv_string()
            elapsed_time = time.perf_counter() - start_time

            print(f"認証サーバからの応答を受信しました: {jwt_token}")
            print(f"通信時間: {elapsed_time:.2f}秒")
            return jwt_token
        except zmq.ZMQError as e:
            print(f"通信エラー: {e}")
            return None
        except Exception as e:
            print(f"予期しないエラー: {e}")
            return None
        finally:
            # ソケットとコンテキストをクリーンアップ
            socket.close()
            context.destroy()

    def generate_child_token(self, parent_token, rw_id):
        """
        親トークンを使って子トークンを生成する
        """
        # 仮の子トークン生成処理（実際はHMACや暗号化手法を用いることを推奨）
        print("ここで子供のTokenを生成します")
        return f"{parent_token}-{rw_id}"

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
                ## 親Tokenが有効ではない時の処理
                if self.parent_token is None or not verify_jwt(self.parent_token):
                    # TODO:親Tokenを得るための処理
                    print("認証サーバと通信を開始します...")
                    self.parent_token = self.request_jwt_from_server(
                        server_address="tcp://10.58.60.5:10006",
                        auth_message="ここに認証したい文字列を入れる",
                    )
                    print("認証サーバとの通信が完了し、親Tokenが生成されました")
                # 親Tokenが正当である時には、子供のTokenを生成する
                rw_id = f"RW-{i+1}"  # 各RWのID
                jwt = self.generate_child_token(self.parent_token, rw_id)

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
                # 初回でなった時も、終了メッセージを命令サーバに送信
                # 情報量はないが、送受信のフォーマットが決まっているので合わせる
                if end_flag:
                    message = Message(
                        ip=self.ip,
                        next_id=self.server2_ip,
                        across_server=0,
                        public_key=self.public_key,
                        jwt=jwt,
                        end_flag=True,
                    )
                    print("[first]Ending server process as instructed.")
                    total_move_server += message.across_server
                    print("次のサーバに移行")
                else:
                    # その後、Server2からのメッセージ待受
                    while True:
                        try:
                            # Server2からのメッセージ受信
                            print("Waiting for messages from Server2...")
                            message = self.receive_message_from_server2()

                            # 継続のメッセージの場合は、メッセージを処理
                            # 終了のメッセージの場合は、ループを終了して、新しいメッセージを送信する
                            if message.end_flag:
                                total_move_server += message.across_server
                                end_flag = True
                            else:
                                # Tokenを検証
                                start_time_jwt_verify = (
                                    time.perf_counter()
                                )  # 　時間を計測
                                print(message.jwt)  # ここでは子tokenが検証される
                                jwt_result = validate_child_token(
                                    message.jwt, self.parent_token, rw_id
                                )
                                end_time_jwt_verify = time.perf_counter()
                                elapsed_time_jwt_verify = (
                                    end_time_jwt_verify - start_time_jwt_verify
                                )
                                print("JWT検証結果", jwt_result)
                                #####ここでTokenを検証する############################################################################
                                end_flag = self.process_message(message)
                                total_move_server += message.across_server

                            # 終了指示があればループ終了
                            if end_flag:
                                print("Ending server process as instructed.")
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
        rw_count=3,
        parent_token=None,
    )
    server1.run()
