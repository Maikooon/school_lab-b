"""
hostname -I
python3 -i User.py 10.58.58.97
"""

from GraphManager import *
import ast


class User:
    def __init__(self, ip_addr):
        self.response_queue = Queue()
        self.ip_addr = ip_addr
        self.port = 10010

    def send_query(self, source_id, count, GM):
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
            print("Expected count: ", message.count)
            print("count: ", count)
            # パケットを受け取るまでブロック
            rtn_bytes = socket.recv()
            print("Received: ", rtn_bytes)
            # literal_eval(str): strを評価して代入
            # e.g., literal_eval('{'a': 1, 'b': 2}') で 辞書が代入される
            # end_walk = ast.literal_eval(rtn_bytes.decode("utf-8"))

            # メッセージをデコードして、end_walk と all_paths を取得
            received_data = ast.literal_eval(rtn_bytes.decode("utf-8"))

            # received_data に end_walk がない場合の対処
            # TODO:ここがないのでエラーが出ている
            end_walk = received_data.get("end_walk", {})  # デフォルトで空の辞書
            all_paths = received_data.get("all_paths", [])  # デフォルトで空のリスト

            for node_id, val in end_walk.items():
                # dict.get(引数, デフォルト値) で引数が存在すればdict[引数]それ以外はデフォルト値を返す
                end_count[node_id] = end_count.get(node_id, 0) + val
                count += val
                print("count: ", count)
        print("Query solved: ", end_count)
        print("All paths: ", all_paths)
        socket.close()
        context.destroy()

    def create_message(self, source_id, count, GM):
        return Message(source_id, count, GM, self.ip_addr)


if __name__ == "__main__":
    user = User(sys.argv[1])
