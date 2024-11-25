import ast


class Message:
    def __init__(self, source_id, count, GM, user, alpha=0.1, jwt=None):
        self.source_id = source_id
        self.count = count
        self.GM = GM  # IP e.g., 127.0.0.1
        self.user = user  # IP e.g., 127.0.0.1
        self.alpha = alpha
        self.jwt = jwt

    def __repr__(self):
        return "from: {}, count: {}, user: {}".format(
            self.source_id, self.count, self.user
        )

    def __str__(self):
        return self.__repr__()

    def __bytes__(self):
        dict = {
            "source_id": self.source_id,
            "count": self.count,
            "GM": self.GM,
            "user": self.user,
            "alpha": self.alpha,
            "jwt": self.jwt,
        }
        return str(dict).encode("utf-8")

    @classmethod
    def from_bytes(cls, b):
        str = b.decode("utf-8")
        dic = ast.literal_eval(str)
        return Message(
            dic["source_id"],
            dic["count"],
            dic["GM"],
            dic["user"],
            dic["alpha"],
            dic["jwt"],
        )
