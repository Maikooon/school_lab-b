import ast
from Jwt import *


class Message:
    def __init__(
        self,
        source_id,
        count,
        GM,
        user,
        alpha=0.2,
        # all_paths=None,
        jwt=None,
        start_node_id=None,
        start_node_community=None,
    ):
        self.source_id = source_id
        self.count = count
        self.GM = GM  # IP e.g., 127.0.0.1
        self.user = user  # IP e.g., 127.0.0.1
        self.alpha = alpha
        # self.all_paths = all_paths if all_paths is not None else []
        self.jwt = generate_jwt(source_id) if jwt is None else jwt
        self.start_node_id = start_node_id
        self.start_node_community = start_node_community

    def __repr__(self):
        return "from: {}, count: {}, user: {}, start_Node: {}".format(
            self.source_id, self.count, self.user, self.start_node_id
        )

    def __str__(self):
        return self.__repr__()

    def __bytes__(self):
        dict_rep = {
            "source_id": self.source_id,
            "count": self.count,
            "GM": self.GM,
            "user": self.user,
            "alpha": self.alpha,
            "all_paths": self.all_paths,
            "jwt": self.jwt,
            "start_node_id": self.start_node_id,
            "start_node_community": self.start_node_community,
        }
        return str(dict_rep).encode("utf-8")

    @classmethod
    def from_bytes(cls, b):
        str_rep = b.decode("utf-8")
        dic = ast.literal_eval(str_rep)
        return Message(
            dic["source_id"],
            dic["count"],
            dic["GM"],
            dic["user"],
            dic["alpha"],
            # dic.get("all_paths", []),
            dic.get("jwt", None),
            dic.get("start_node_id", None),
            dic.get("start_node_community", None),
        )
