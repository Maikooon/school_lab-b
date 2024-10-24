"""
hostname -I
python3 -i User.py 10.58.58.97
"""

from GraphManager import *
from Graph import *
import ast
import time


class User:
    def __init__(self, ip_addr):
        self.response_queue = Queue()
        self.ip_addr = ip_addr
        self.port = 10030

    def send_query(self, source_id, count, GM):
        print("send_query")
        start_time = time.time()  # ここから時間を計測する
        self.response_queue = Queue()
        message = self.create_message(source_id, count, GM)
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.connect("tcp://{}:{}".format(message.GM, self.port))
        socket.send(bytes(message))
        socket.close()
        context.destroy()

        count = 0
        end_count = dict()
        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.bind("tcp://{}:{}".format(self.ip_addr, self.port))

        while count < message.count:
            print("Expected count: ", message.count)
            print("count: ", count)
            # パケットを受け取るまでブロック
            try:
                rtn_bytes = socket.recv()
                print("Received: ", rtn_bytes)

                # 受信したデータを辞書として評価
                received_message = ast.literal_eval(rtn_bytes.decode("utf-8"))
                end_walk = received_message["end_walk"]
                all_paths = received_message["all_paths"]

                print("End Walk: ", end_walk)
                print("All Paths: ", all_paths)

                for node_id, val in end_walk.items():
                    end_count[node_id] = end_count.get(node_id, 0) + val
                    count += val
                    print("count: ", count)

            except Exception as e:
                print("Error receiving data: ", e)

        # average_path_length = len(all_paths) / count
        # print("Average path length: ", average_path_length)

        print("Query solved: ", end_count)
        socket.close()
        context.destroy()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time:.4f} seconds")  # 経過時間を表示

    def create_message(self, source_id, count, GM):
        print("create_message")
        return Message(source_id, count, GM, self.ip_addr)


if __name__ == "__main__":
    user = User(sys.argv[1])
