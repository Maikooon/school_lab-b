from Graph import *
from Message import *
from Jwt import *
import threading
import os
import socket
import sys
import json
import zmq
import time


LOG_FILE_PATH = "./access_limit_time.txt"  # 保存先のログファイルパス


def save_notify_log(user, end_walk):
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(f"Notified to {user}, End Walk: {end_walk}\n")
        log_file.write("-" * 40 + "\n")


class GraphManager:
    def __init__(self, id, graph, ip_addr):
        self.id = id
        self.graph = graph
        self.ip_addr = ip_addr
        self.port = 10026
        self.receive_queue = Queue()
        self.send_queue = Queue()
        self.notify_queue = Queue()
        # self.across_server_count_total = 0
        self.total_jwt_verify_time = 0
        self.total_jwt_connected = 0
        self.total_count_test = 0
        self.start()
        # self.total_move_count = 0

    @classmethod
    def init_for_espresso(cls, dir_path):
        host_name = os.uname()[1]
        host_ip = socket.gethostbyname(host_name)
        graph_txt_file = dir_path + host_name + ".txt"
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

        graph = Graph(ADJ, nodes)
        gm = GraphManager(host_name, graph, host_ip)
        gm.host_name = host_name

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

    """
    メッセージを取り出す
    処理を実行
    処理の結果、それを再びキューに格納するのかを指定
    """

    def random_walk(self):
        # キューからメッセージがなくなるまで繰り返す
        while True:
            message = self.receive_queue.get()
            end_walk, escaped_walk = self.graph.random_walk(
                message.source_id, message.count, message.alpha
            )
            # self.across_server_count_total += across_server_count  # またぎ回数を更新
            print("end_walk: {}, escaped_walk: {}".format(end_walk, escaped_walk))
            # # print('end_walk: {}, escaped_walk: {}'.format(end_walk, escaped_walk))
            # RWが終了したときの処理
            if len(end_walk) > 0:
                self.notify_queue.put([message.user, end_walk])
            # RWが継続するときの処理
            print("escaped_walk-------------------------", escaped_walk)
            if len(escaped_walk) > 0:
                self.total_count_test += 1
                for node_id, val in escaped_walk.items():
                    # TODO;キューに格納する前に、JWTを生成するために、認証サーバに接続する

                    context = zmq.Context()
                    socket = context.socket(zmq.REQ)
                    socket.connect("tcp://10.58.60.5:10006")  # 認証サーバへ接続
                    start_time_jwt_connected = time.perf_counter()
                    message_for_ninsyo = (
                        f"{node_id}:{val}"  # 例としてnode_idとvalを文字列に変換
                    )
                    socket.send_string(message_for_ninsyo)  # 認証要求を送信

                    # サーバからの応答を受け取る
                    response = socket.recv_string()
                    print("Received JWT from server:", response)  # 受け取ったJWTを表示
                    jwt = response  # 受け取ったJWTを変数に格納
                    end_time_jwt_connect = (
                        time.perf_counter()
                    )  # 　---------------------ここまでの時間
                    socket.close()
                    context.destroy()

                    print("Escaped Walk: kokokokokokoko", node_id, val)
                    self.send_queue.put(
                        Message(
                            node_id,
                            val,
                            self.graph.outside_nodes[node_id].manager,
                            message.user,
                            message.alpha,
                            jwt,
                        )
                    )
                    elapsed_time_jwt_connected = (
                        end_time_jwt_connect - start_time_jwt_connected
                    )
                    self.total_jwt_connected += elapsed_time_jwt_connected
            print("total_count_test", self.total_count_test)

    def notify_result(self):
        while True:
            user, end_walk = self.notify_queue.get()
            context = zmq.Context()
            socket = context.socket(zmq.PUSH)
            socket.connect("tcp://{}:{}".format(user, self.port))
            socket.send(str(end_walk).encode("utf-8"))
            socket.close()
            context.destroy()
            print("Notified to {}\n{}".format(user, end_walk))
            print("total_jwt_verify_time:", self.total_jwt_verify_time)
            print("total_jwt_connected:", self.total_jwt_connected)
            save_notify_log(
                self.total_jwt_verify_time,
                self.total_jwt_connected,
            )

    def send_message(self):
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
            print("total_time_jwt_connected", self.total_jwt_connected)

    def receive_message(self):
        # ここの回数ー初めに命令サーバから出された時
        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.bind("tcp://{}:{}".format(self.ip_addr, self.port))
        while True:
            message_bytes = socket.recv()
            message = Message.from_bytes(message_bytes)
            # 認証情報を確認してから受け取るのでは

            # TODO: JWTの検証を行う
            print("このJWTを検証する", message.jwt)
            start_time_jwt_verify = time.perf_counter()  # 　時間を計測
            jwt_result = verify_jwt(message.jwt)
            end_time_jwt_verify = time.perf_counter()
            elapsed_time_jwt_verify = end_time_jwt_verify - start_time_jwt_verify
            self.total_jwt_verify_time += elapsed_time_jwt_verify
            print("JWT検証結果", jwt_result)
            ######ここでTokenを検証する############################################################################
            # 検証が正当にされたら、受け取る
            # if jwt_result:
            #     self.receive_queue.put(message)

            self.receive_queue.put(message)
            print(
                "Recieved message\nsource {}, count {}".format(
                    message.source_id, message.count
                )
            )
            # self.total_move_count += 0


if __name__ == "__main__":
    gm = GraphManager.init_for_espresso(sys.argv[1])
    try:
        while True:
            pass
    except KeyboardInterrupt:
        # 終了時に 独自のフォルダにログを保存
        print("Exiting...")
        print("Total moves across servers: {}".format(gm.total_count_test))
        if not os.path.exists("./logs"):
            os.mkdir("./logs")
        with open("./logs/count.txt".format(gm.host_name), "w") as f:
            f.write("Total moves across servers: {}\n".format(gm.total_count_test))
