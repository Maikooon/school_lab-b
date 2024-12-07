import jwt
import zmq
import datetime

SECRET_KEY = "your_secret_key"  # 自サーバーで管理する秘密鍵


# JWTを生成
def generate_jwt(user_id):
    # TODO:ここで有効期限を明記
    validity_seconds = 100  # 有効期限は1時間
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(seconds=validity_seconds),
        "iat": datetime.datetime.utcnow(),  # 発行時刻
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print("Generated Token:", token)
    return token


# JWTを検証
def verify_jwt(token):
    try:
        # JWTのデコードと有効性検証
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        # 有効期限切れのエラー
        current_time = datetime.datetime.utcnow()
        print(f"Token has expired at {current_time}.")
        print("The token's expiration time has passed.")
        return None
    except jwt.InvalidTokenError:
        # その他のトークンエラー
        print("Invalid token")
        return None


# 子Tokenを検証
def validate_child_token(token):
    """
    子トークンが有効かどうかを検証する関数。

    Parameters:
        child_token (str): 検証対象のトークン
        parent_token (str): 元となる親トークン
        rw_id (str): 対象のRandomWalker ID

    Returns:
        bool: トークンが有効ならTrue、無効ならFalse
    """
    try:
        # JWTのデコードと有効性検証
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        # 有効期限切れのエラー
        current_time = datetime.datetime.utcnow()
        print(f"Token has expired at {current_time}.")
        print("The token's expiration time has passed.")
        return None
    except jwt.InvalidTokenError:
        # その他のトークンエラー
        print("Invalid token")
        return None