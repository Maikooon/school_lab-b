import zmq
import time
import os
import logging
import ast
from queue import Queue


# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("./results/communication.log"),
        logging.StreamHandler(),
    ],
)


class Message:
    def __init__(
        self, source_id, count, transition_prob, next_server_ip, current_server_ip
    ):
        self.source_id = source_id
        self.count = count
        self.transition_prob = transition_prob
        self.next_server_ip = next_server_ip
        self.current_server_ip = current_server_ip

    def to_dict(self):
        return {
            "source_id": self.source_id,
            "count": self.count,
            "transition_prob": self.transition_prob,
            "next_server_ip": self.next_server_ip,
            "current_server_ip": self.current_server_ip,
        }

    def to_bytes(self):
        return str(self.to_dict()).encode("utf-8")


class User:
    def __init__(self, ip_addr, port=10026):
        self.response_queue = Queue()
        self.ip_addr = ip_addr
        self.port = port

    def save_to_file(self, end_count, elapsed_time, average_hops):
        # 保存先ディレクトリとファイルパス
        directory = "./results"
        file_path = os.path.join(directory, "message.txt")

        if not os.path.exists(directory):
            os.makedirs(directory)

        # ファイルに追記
        with open(file_path, "a") as file:
            file.write(f"Query solved: {end_count}\n")
            file.write(f"Execution time: {elapsed_time:.4f} seconds\n")
            file.write(f"Average Hops: {average_hops:.2f}\n")
            file.write("\n")

        logging.info("Results saved to file.")

    def send_query(self, source_id, count, transition_prob, next_server_ip):
        # 実行時間計測開始
        start_time = time.perf_counter()

        # メッセージ作成
        message = Message(
            source_id=source_id,
            count=count,
            transition_prob=transition_prob,
            next_server_ip=next_server_ip,
            current_server_ip=self.ip_addr,
        )

        # メッセージ送信
        context = zmq.Context()
        try:
            socket = context.socket(zmq.PUSH)
            socket.connect(f"tcp://{message.next_server_ip}:{self.port}")
            socket.send(message.to_bytes())
            logging.info(
                f"Sent message to {message.next_server_ip}: {message.to_dict()}"
            )
        except zmq.ZMQError as e:
            logging.error(f"Failed to send message: {e}")
        finally:
            socket.close()
            context.destroy()

        # メッセージ受信
        end_count, hops = self.receive_response(message.count)

        # 実行時間計測終了
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        # 結果保存
        average_hops = hops / message.count if message.count > 0 else 0
        self.save_to_file(end_count, elapsed_time, average_hops)

        return end_count

    def receive_response(self, expected_count):
        end_count = {}
        hops = 0
        received_count = 0

        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.bind(f"tcp://{self.ip_addr}:{self.port}")

        try:
            while received_count < expected_count:
                rtn_bytes = socket.recv()
                response = ast.literal_eval(rtn_bytes.decode("utf-8"))

                for node_id, val in response.items():
                    end_count[node_id] = end_count.get(node_id, 0) + val
                    received_count += val
                    hops += val  # 各メッセージでHop数をカウント

                logging.info(f"Received response: {response}")
        except zmq.ZMQError as e:
            logging.error(f"Failed to receive message: {e}")
        finally:
            socket.close()
            context.destroy()

        return end_count, hops


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 5:
        print(
            "Usage: python script.py <ip_addr> <source_id> <count> <transition_prob> <next_server_ip>"
        )
        sys.exit(1)

    ip_addr = sys.argv[1]
    source_id = int(sys.argv[2])
    count = int(sys.argv[3])
    transition_prob = float(sys.argv[4])
    next_server_ip = sys.argv[5]

    user = User(ip_addr)
    user.send_query(source_id, count, transition_prob, next_server_ip)
