from GraphManager import *
import ast
import os
import time
import zmq


def save_to_file(self, end_count, elapsed_time):
    # 保存先ディレクトリとファイルパス
    directory = "./results"
    file_path = os.path.join(directory, "message.txt")

    # ディレクトリが存在しない場合は作成
    if not os.path.exists(directory):
        os.makedirs(directory)

    # ファイルに追記
    with open(file_path, "a") as file:
        file.write(f"Query solved: {end_count}\n")
        file.write(f"Execution time: {elapsed_time:.4f} seconds\n")
        file.write("\n")


class User:
    def __init__(self, ip_addr):
        self.response_queue = Queue()
        self.ip_addr = ip_addr
        self.port = 10020

    # コマンドラインからこれを直接入力することで、Userクラスを実行
    def send_query(self, source_id, count, GM):
        # start_time = time.time()  # 計測を開始
        start_time = time.perf_counter()  # 計測を開始 (高精度)
        self.response_queue = Queue()
        message = self.create_message(source_id, count, GM)
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.connect("tcp://{}:{}".format(message.GM, self.port))
        socket.send(bytes(message))
        socket.close()
        context.destroy()
        # print('User{} sent to {}\n{}'.format(self.id, message.GM, message))

        count = 0
        end_count = dict()
        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.bind("tcp://{}:{}".format(self.ip_addr, self.port))
        while count < message.count:
            # パケットを受け取るまでブロック
            rtn_bytes = socket.recv()
            # literal_eval(str): strを評価して代入
            # e.g., literal_eval('{'a': 1, 'b': 2}') で 辞書が代入される
            end_walk = ast.literal_eval(rtn_bytes.decode("utf-8"))
            for node_id, val in end_walk.items():
                # dict.get(引数, デフォルト値) で引数が存在すればdict[引数]それ以外はデフォルト値を返す
                end_count[node_id] = end_count.get(node_id, 0) + val
                count += val
        socket.close()
        context.destroy()
        # print('Query solved: ', end_count)
        # end_time = time.time()  # 計測を終了
        end_time = time.perf_counter()  # 計測を終了
        elapsed_time = end_time - start_time
        print("Elapsed time---: ", elapsed_time)
        save_to_file(self, end_count, elapsed_time)
        return end_count

    def create_message(self, source_id, count, GM):
        return Message(source_id, count, GM, self.ip_addr)


if __name__ == "__main__":
    user = User(sys.argv[1])
