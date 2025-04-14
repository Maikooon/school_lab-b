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

        # TODO:ここを追加
        self.graph = self.load_graph("graph_server1.txt")
        self.server_node_map = self.load_node_to_server_map("node_to_server.txt")
        self.local_nodes = set(self.graph.keys())  # 自分が持っているノード

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

    def find_server_by_node(self, node_id):
        if node_id in self.server_node_map:
            return self.server_node_map[node_id]
        else:
            raise ValueError(f"ノード {node_id} の担当サーバが見つかりません。")

    def process_message(self, message):
        end_flag = False
        current_node = message.next_id  # 現在のノードID

        print(
            f"Start RW from Node {current_node}, total across: {message.across_server}"
        )

        while True:
            # α の確率で遷移、1-α で終了
            if random.random() < self.alpha:
                neighbors = self.graph.get(current_node, [])
                if not neighbors:
                    print(f"ノード {current_node} に隣接ノードがありません。終了。")
                    end_flag = True
                    break

                next_node = random.choice(neighbors)
                print(f"選ばれた次ノード: {next_node}")

                if next_node in self.local_nodes:
                    # 同一サーバ内
                    print(f"ノード {next_node} はローカル。遷移継続。")
                    current_node = next_node
                else:
                    # 他サーバへ移動
                    target_server_ip = self.find_server_by_node(next_node)
                    print(f"ノード {next_node} は他サーバ。{target_server_ip} に送信。")

                    new_message = Message(
                        ip=self.ip,
                        next_id=next_node,
                        across_server=message.across_server + 1,
                        public_key=self.public_key,
                        jwt="JWT_TOKEN_PLACEHOLDER",  # JWT生成関数に置き換え可能
                        end_flag=False,
                    )
                    self.send_message_to(target_server_ip, new_message)
                    break  # サーバ間通信が発生したら処理終了
            else:
                print("確率で終了処理に到達。ランダムウォーク終了。")
                end_flag = True
                break

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
                    # その後、Server2からのメッセージ待受
                    while True:
                        try:
                            # Server2からのメッセージ受信,このメッセージには、終了メッセージも含まれる
                            print("Waiting for messages from Server2...")
                            message = self.receive_message_from_server2()

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
                next_id=self.server2_ip,
                across_server=total_move_server,
                public_key=self.public_key,
                jwt="JWT_TOKEN_PLACE",
                end_flag=True,
            )
            print("[last]Ending server process as instructed.")
            # print("次のメッセージを命令サーバに送信", message.to_string())
            self.sender_to_command.send_string(message.to_string())

    def load_graph(self, filename):
        graph = {}
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                src = int(parts[0])
                dst = int(parts[1])
                graph.setdefault(src, []).append(dst)
                graph.setdefault(dst, []).append(src)  # 無向グラフ想定
        return graph

    def load_node_to_server_map(self, filename):
        mapping = {}
        with open(filename, "r") as f:
            for line in f:
                node_id, ip = line.strip().split()
                mapping[int(node_id)] = ip
        return mapping


if __name__ == "__main__":
    server1 = Server1(
        ip="10.58.60.5",
        port=3200,
        server2_ip="10.58.60.6",
        server2_port=3202,
        command_server_ip="10.58.60.11",
        command_server_port=3203,
        public_key="Server1_Public_Key",  # 公開鍵
        alpha=0.15,  # RWの終了確立
        beta=0.001,
        rw_count=10000,
    )

    server1.run()
