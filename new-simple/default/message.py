import ast


class Message:
    def __init__(
        self,
        ip,
        next_id,  # Use next_id here
        path,
        public_key,
        jwt=None,
        start_time=None,
    ):
        self.ip = ip
        self.next_id = next_id  # Set next_id properly
        self.path = path
        self.public_key = public_key
        self.jwt = jwt
        self.start_time = start_time

    def __bytes__(self):
        dict_rep = {
            "ip": self.ip,
            "next_id": self.next_id,  # Use next_id here
            "path": self.path,
            "public_key": self.public_key,
            "jwt": self.jwt,
            "start_time": self.start_time,
        }
        return str(dict_rep).encode("utf-8")

    @classmethod
    def from_bytes(cls, b):
        str_rep = b.decode("utf-8")
        dic = ast.literal_eval(str_rep)
        return Message(
            dic["ip"],
            dic["next_id"],  # Use next_id here
            dic["path"],
            dic["public_key"],
            dic["jwt"],
            dic["start_time"],
        )
