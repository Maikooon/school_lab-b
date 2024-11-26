import jwt
import zmq
import datetime

SECRET_KEY = "your_secret_key"  # 自サーバーで管理する秘密鍵


# JWTを生成
def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=30),  # 30分の有効期限
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
