import zmq
import random
import time
import os
import ast
import logging


# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("./results/manager.log"), logging.StreamHandler()],
)


class Manager:
    def __init__(self, ip_addr, port=10026):
        self.ip_addr = ip_addr
        self.port = port

    def process_message(self, message):
        """
        メッセージを処理して結果を生成する。
        """
        response = {}
        source_id = message.get("source_id", -1)
        count = message.get("count", 1)
        transition_prob = message.get("transition_prob", 0.0)

        for i in range(count):
            transition_value = random.random()
            if transition_value < transition_prob:
                # 次のサーバに移動する場合
                response[source_id] = response.get(source_id, 0) + 1

        logging.info(f"Processed message from source_id={source_id}: {response}")
        return response

    def start(self):
        """
        サーバを起動し、メッセージを受信して処理を行う。
        """
        context = zmq.Context()
        socket_recv = context.socket(zmq.PULL)
        # ここで送られてきたメッセージを解読する
        socket_recv.bind(f"tcp://{self.ip_addr}:{self.port}")

        socket_send = context.socket(zmq.PUSH)

        try:
            while True:
                logging.info("Waiting for messages...")
                # メッセージを受信
                msg_bytes = socket_recv.recv()
                message = ast.literal_eval(msg_bytes.decode("utf-8"))
                logging.info(f"Received message: {message}")

                # メッセージを処理
                response = self.process_message(message)

                # 次のサーバIPアドレスを取得
                next_server_ip = message.get("next_server_ip")
                if next_server_ip:
                    # 次のサーバに送信
                    socket_send.connect(f"tcp://{next_server_ip}:{self.port}")
                    socket_send.send(str(response).encode("utf-8"))
                    logging.info(
                        f"Sent processed response to {next_server_ip}: {response}"
                    )
                else:
                    logging.warning(
                        "No next server IP specified, stopping message propagation."
                    )
        except Exception as e:
            logging.error(f"Error occurred: {e}")
        finally:
            socket_recv.close()
            socket_send.close()
            context.destroy()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python manager.py <ip_addr>")
        sys.exit(1)

    ip_addr = sys.argv[1]
    manager = Manager(ip_addr)
    manager.start()
