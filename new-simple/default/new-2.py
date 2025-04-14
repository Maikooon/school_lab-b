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

        # TODO:ここを追加
        self.graph = self.load_graph("graph_server2.txt")
        self.server_node_map = self.load_node_to_server_map("node_to_server.txt")
        self.local_nodes = set(self.graph.keys())  # 自分が持っているノード

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
        # メッセージを受信し、ランダムホップを開始
        end_flag = False

        # その後、Server1からのメッセージ待受
        while True:
            try:
                # Server1からのメッセージ受信
                print("Waiting for messages from Server1...")
                message = self.receive_message_from_server1()

                # メッセージを処理
                end_flag = self.process_message(message)

                # 終了指示があればループ終了
                if end_flag:
                    print("Ending server process as instructed.")
                    break

            except Exception as e:
                print(f"Error occurred: {e}")
                break

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
    server2 = Server2(
        ip="10.58.60.6",
        port=3202,
        server1_ip="10.58.60.5",
        server1_port=3200,
        command_server_ip="10.58.60.11",
        command_server_port=3203,
        public_key="Server1_Public_Key",  # 公開鍵
        alpha=0.15,
        beta=0.3,
    )
    server2.run()
