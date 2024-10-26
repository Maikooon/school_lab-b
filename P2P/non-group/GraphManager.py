from Graph import *
from Message import *
from Jwt import *
import threading
import time
import zmq
import os
import socket
import sys
import re


class GraphManager:
    def __init__(self, id, graph, ip_addr):
        self.id = id
        self.graph = graph
        self.ip_addr = ip_addr
        self.port = 10030
        self.receive_queue = Queue()
        self.send_queue = Queue()
        self.notify_queue = Queue()
        self.start_node_id = None  # Initialize start_node_id
        self.start_node_community = None  # Initialize start_node_community
        self.total_jwt_verify_time = 0
        self.total_jwt_generate = 0
        self.start()

    @classmethod
    def init_for_espresso(cls, dir_path):
        total_time_read_file = 0
        host_name = os.uname()[1]
        host_ip = socket.gethostbyname(host_name)
        # 　読み込むファイル名をIPに基づいて変更
        graph_txt_file = dir_path + host_name + ".txt"
        print("Graph txt file: ", graph_txt_file)
        f = open(graph_txt_file)
        data = f.read()
        f.close()
        data = data.split("\n")
        del data[-1]
        for i in range(len(data)):
            data[i] = data[i].split(",")

        ADJ = dict()
        nodes = dict()
        for line in data:
            edge = [line[0], line[1]]
            dest_ip = line[2]
            if edge[0] not in nodes.keys():
                nodes[edge[0]] = Node(edge[0], host_ip)
            if edge[0] not in ADJ.keys():
                ADJ[edge[0]] = list()
            if edge[1] not in nodes.keys():
                nodes[edge[1]] = Node(edge[1], dest_ip)
            ADJ[edge[0]].append(edge[1])

        # ng_list_fileを辞書として初期化
        ng_list = {}
        ng_list_path = os.path.join(dir_path, "non_group-ng_nodes.txt")

        with open(ng_list_path, "r") as f:
            lines = f.readlines()

        # NGリストファイルをパース
        for line in lines:
            if line.strip():  # 行が空でないことを確認
                key, values = line.split(":")
                key = int(key.strip())  # キーを整数に変換
                values = [int(v.strip()) for v in values.split(",")]  # 各値を整数に変換
                ng_list[key] = values  # 辞書に追加

        # print("NG list loaded:", ng_list)

        # 4. GraphManagerのインスタンス作成
        graph = Graph(ADJ, nodes, ng_list)
        gm = GraphManager(host_name, graph, host_ip)
        gm.host_name = host_name
        gm.ng_list = ng_list
        print("データを読み込み終わりました")
        return gm

    def __repr__(self):
        rtn = ""
        rtn += "Graph Manager {}\n".format(self.id)
        for node in self.graph.nodes.values():
            rtn += "Node: {}, ADJ:".format(node.id)
            for adj_node in node.adj.values():
                rtn += " {}({}),".format(adj_node.id, adj_node.manager)
            rtn = rtn[:-1] + "\n"
        return rtn

    def start(self):
        thr_random_walk = threading.Thread(target=self.random_walk, daemon=False)
        thr_random_walk.start()
        thr_notify_result = threading.Thread(target=self.notify_result, daemon=False)
        thr_notify_result.start()
        thr_send_message = threading.Thread(target=self.send_message, daemon=False)
        thr_send_message.start()
        thr_receive_message = threading.Thread(
            target=self.receive_message, daemon=False
        )
        thr_receive_message.start()
        print(
            "GraphManager started. IP addr: {}, recv port: {}".format(
                self.ip_addr, self.port
            )
        )

    def random_walk(self):
        # 本当の原点は、self.start_node_idに格納
        # print("random_walk-self")
        while True:
            # キューからメッセージを取り出す、RWを実行するためのメッセージが得られる
            message = self.receive_queue.get()

            # 原点を渡すための処理
            # print("受け取ったメッセ", message)
            if message.start_node_id is None:
                message.start_node_id = message.source_id  # 初期のstart_node_idを設定
            else:
                print(f"start_node_id は既に設定されています: {self.start_node_id}")
            # 　ここでノード情報をコミュニティ情報に更新してしまう         -------------------------------------------------------------------------------------------------------

            self.start_node_id = message.start_node_id
            self.start_node_community = message.start_node_community
            # print(
            #     f"RWが一番初めにHopし始めたノード{self.start_node_id}、コミュニティ{self.start_node_community}"
            # )
            # print(message.start_node_community)
            # ここまで

            # print("このJWTを検証する", message.jwt)
            # TODO: JWTの検証を行う
            start_time_jwt_verify = time.time()  # 　時間を計測
            jwt_result = verify_jwt(message.jwt)
            end_time_jwt_verify = time.time()
            elapsed_time_jwt_verify = end_time_jwt_verify - start_time_jwt_verify
            self.total_jwt_verify_time += elapsed_time_jwt_verify
            ######ここでTokenを検証する############################################################################
            print("JWT検証結果", jwt_result)

            # 取り出したところで処理していいのかを査定する
            print("ここでTokenを検証して認証したい")

            # RWを実行
            end_walk, escaped_walk, all_paths = self.graph.random_walk(
                message.source_id,
                message.count,
                message.alpha,
                message.all_paths,
                self.start_node_id,
                self.start_node_community,
            )

            # print("RWの実行終了")
            # 終了RWとして集計用箱に格納
            # print("end_walk", end_walk)
            if len(end_walk) > 0:
                # print("put", message.user, end_walk, all_paths)
                self.notify_queue.put(
                    {"user": message.user, "end_walk": end_walk, "all_paths": all_paths}
                )
            # print("escaped_walk", escaped_walk)
            # 他サーバへ向かうRW_>他サーバにRW情報を送信
            if len(escaped_walk) > 0:
                for node_id, val in escaped_walk.items():
                    # 続きのサーバにRW情報を送信するために、キューに格納される
                    # 何を認証すればいいのかわからないので、とりあえずnode_idを認証情報として使う
                    start_time_jwt_generate = time.time()  # 　時間を計測
                    jwt = generate_jwt(node_id)
                    end_time_jwt_generate = time.time()
                    elapsed_time_jwt_generate = (
                        end_time_jwt_generate - start_time_jwt_generate
                    )
                    self.total_jwt_generate += elapsed_time_jwt_generate
                    self.send_queue.put(
                        Message(
                            node_id,
                            val,
                            self.graph.outside_nodes[node_id].manager,
                            message.user,
                            message.alpha,
                            message.all_paths,
                            jwt,
                            start_node_id=self.start_node_id,
                            start_node_community=self.start_node_community,
                        )
                    )

    def notify_result(self):
        # print("notify_result")
        while True:
            result = self.notify_queue.get()

            # 結果からユーザー、終了ウォーク、全経路情報を取得
            user = result["user"]
            end_walk = result["end_walk"]
            all_paths = result.get("all_paths", [])  # デフォルトで空リスト

            context = zmq.Context()
            socket = context.socket(zmq.PUSH)
            socket.connect("tcp://{}:{}".format(user, self.port))
            # 辞書にまとめて送信
            message = {"end_walk": end_walk, "all_paths": all_paths}

            socket.send_string(str(message))  # 辞書を文字列に変換して送信
            socket.close()
            context.destroy()
            print("Notified to {},{}".format(user, end_walk))
            print("total_jwt_verify_time:", self.total_jwt_verify_time)
            print("total_jwt_generate:", self.total_jwt_generate)

    def send_message(self):
        # print("send_message-self")
        while True:
            message = self.send_queue.get()
            context = zmq.Context()
            socket = context.socket(zmq.PUSH)
            socket.connect("tcp://{}:{}".format(message.GM, self.port))
            socket.send(bytes(message))
            socket.close()
            context.destroy()
            print("Sent to {}\n{}".format(message.GM, message))
            print("total_time_jwt_verify", self.total_jwt_verify_time)
            print("total_time_jwt_generate", self.total_jwt_generate)
            # print("total_time_read_file", self.total_time_read_file)

    # サーバが別のサーバからのRW情報を受け取る
    def receive_message(self):
        print("receive_message")
        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.bind("tcp://{}:{}".format(self.ip_addr, self.port))
        while True:
            message_bytes = socket.recv()
            message = Message.from_bytes(message_bytes)
            # 他から受け取ったメッセージを.pathを朱通力したかったらここで見る保存
            self.receive_queue.put(message)
            print(
                "Recieved message\nsource {}, count {} ".format(
                    message.source_id, message.count
                )
            )


if __name__ == "__main__":
    gm = GraphManager.init_for_espresso(sys.argv[1])
