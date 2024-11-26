import ast
import datetime
import time


class Message:
    def __init__(
        self, ip, next_id, across_server, public_key, jwt=None, start_time=None
    ):
        self.ip = ip
        self.next_id = next_id
        self.across_server = across_server
        self.public_key = public_key
        self.jwt = jwt
        self.start_time = start_time or time.time()

    def __repr__(self):
        return f"Message(ip={self.ip}, next_id={self.next_id}, path={self.across_server}, public_key={self.public_key}, jwt={self.jwt}, start_time={self.start_time})"

    def to_string(self):
        # オブジェクトを文字列化
        return str(self.__dict__)

    @classmethod
    def from_string(cls, message_str):
        # 文字列からオブジェクトを復元
        message_dict = eval(
            message_str
        )  # JSONを使うのが安全だが、ここでは簡易的にevalを利用
        return cls(
            ip=message_dict["ip"],
            next_id=message_dict["next_id"],
            across_server=message_dict["across_server"],
            public_key=message_dict["public_key"],
            jwt=message_dict["jwt"],
            start_time=message_dict["start_time"],
        )
