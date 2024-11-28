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

    def process_message(self, message):
        total_across_servers = message.across_server
        print(f"Total across_servers: {total_across_servers}")

        while True:
            # 終了確率をチェック
            if random.random() > self.alpha:
                if random.random() < self.beta:
                    # 他のサーバにメッセージを送信
                    # 今回は毎回行うので、認証サーバと通信を行います
                    print("認証サーバと通信を開始します...")
                    jwt = self.request_jwt_from_server(
                        server_address="tcp://10.58.60.5:10006",
                        auth_message="ここに認証したい文字列を入れる",
                    )
                    if jwt is None:
                        print("JWTトークンの取得に失敗しました。処理を中断します。")
                        break
                    print("認証サーバとの通信が完了しました。")
                    # パスに現在のIDを追加し、次のサーバに送信
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
                    jwt=message.jwt,  # 実際には有効なJWTを生成する
                    end_flag=True,
                )
                self.sender_to_server1.send_string(new_message.to_string())
                break  # 送信せず終了

    def run(self):
        print("Server is running. Waiting for messages...")
        # メッセージを受信し、ランダムホップを開始
        end_flag = False

        # その後、Server1からのメッセージ待受
        while True:
            try:
                # Server1からのメッセージ受信
                print("Waiting for messages from Server1...")
                message = self.receive_message_from_server1()

                # TODO:ここでTokenを検証
                jwt_result = verify_jwt(message.jwt)
                end_time_jwt_verify = time.perf_counter()
                # elapsed_time_jwt_verify = end_time_jwt_verify - start_time_jwt_verify
                # self.total_jwt_verify_time += elapsed_time_jwt_verify
                print("JWT検証結果", jwt_result)
                ############################

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
        port=3112,
        server1_ip="10.58.60.3",
        server1_port=3110,
        command_server_ip="10.58.60.11",
        command_server_port=3113,
        public_key="Server1_Public_Key",  # 公開鍵
        alpha=0.15,
        beta=0.5,
    )
    server2.run()
