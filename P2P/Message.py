import ast


class Message:
    def __init__(self, source_id, count, GM, user, alpha=0.2, all_paths=None):
        self.source_id = source_id
        self.count = count
        self.GM = GM  # IP e.g., 127.0.0.1
        self.user = user  # IP e.g., 127.0.0.1
        self.alpha = alpha
        self.all_paths = (
            all_paths if all_paths is not None else []
        )  # Ensure default empty list

    def __repr__(self):
        return "from: {}, count: {}, user: {}".format(
            self.source_id, self.count, self.user
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
            "all_paths": self.all_paths,  # Include all_paths in the byte conversion
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
            dic.get("all_paths", []),
        )