import jwt
import zmq
import datetime

SECRET_KEY = "your_secret_key"  # 自サーバーで管理する秘密鍵


# JWTを生成
def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow()
        # TODO: これを０にしたときにちゃんと失敗するのか確認したい
        + datetime.timedelta(minutes=0),  # 30分の有効期限
        "iat": datetime.datetime.utcnow(),  # 発行時刻
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


# JWTを検証
def verify_jwt(token):
    try:
        # JWTのデコードと有効性検証
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


# 子Tokenを検証
def validate_child_token(child_token, parent_token, rw_id):
    """
    子トークンが有効かどうかを検証する関数。

    Parameters:
        child_token (str): 検証対象のトークン
        parent_token (str): 元となる親トークン
        rw_id (str): 対象のRandomWalker ID

    Returns:
        bool: トークンが有効ならTrue、無効ならFalse
    """
    # 正しいトークンの期待値を生成
    expected_token = f"{parent_token}-{rw_id}"

    # 子トークンと期待されるトークンが一致するか検証
    return child_token == expected_token
