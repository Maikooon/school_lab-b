import matplotlib.pyplot as plt

# プロットするデータを指定
x1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # 1本目の横軸の値
y1 = [
    0.042,
    0.040264,
    0.037765,
    0.031658,
    0.029843,
    0.027962,
    0.027856,
    0.026943,
    0.026484,
    0.026182,
    0.025781,
    0.025732,
    0.025601,
]


x2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
y2 = [
    0.0418,
    0.0418,
    0.0418,
    0.0418,
    0.0418,
    0.0418,
    0.0418,
    0.0418,
    0.0418,
    0.0418,
    0.0418,
    0.0418,
    0.0418,
]
# 全てのYの要素に0.99を掛ける
y1 = [yi + 0.95 for yi in y1]
y2 = [yi + 0.95 for yi in y2]

# グラフの作成
plt.figure(figsize=(8, 5))

# 1本目のグラフ
plt.plot(
    x1,
    y1,
    linestyle="-",
    color="#DC2626",
    marker="o",
    markersize=10,
    label="use cache",
)

# 2本目のグラフ
plt.plot(
    x2,
    y2,
    linestyle="-",
    color="grey",
    marker="s",
    markersize=10,
    label="no cache",
)

# 軸ラベルの設定
plt.xlabel("hop count", fontsize=14)
plt.ylabel("verification time", fontsize=14)

# 軸の目盛をカスタマイズ
plt.xticks(x1, [f"{xi}" for xi in x1], fontsize=12)
plt.yticks(fontsize=12)

# 凡例を表示
plt.legend(fontsize=12)

# グリッド線（必要であれば追加）
plt.grid(visible=True, linestyle="--", alpha=0.5)
plt.savefig("plt0121-cache.pdf")
# グラフの表示
plt.show()

# ここでJWTの検証を行う
# import jwt
# import time

# # 秘密鍵とサンプルJWT
# SECRET_KEY = "your_secret_key"  # 実際には安全な場所で管理する
# algorithm = "HS256"

# # サンプルのペイロード
# payload = {
#     "user_id": 123,
#     "username": "example_user",
#     "exp": int(time.time()) + 60,  # 有効期限は60秒後
# }

# # JWTの生成
# token = jwt.encode(payload, SECRET_KEY, algorithm=algorithm)
# print(f"Generated JWT: {token}")


# # JWT検証関数
# def verify_jwt(token: str, secret: str, algorithm: str):
#     try:
#         decoded = jwt.decode(token, secret, algorithms=[algorithm])
#         return decoded
#     except jwt.ExpiredSignatureError:
#         print("Token has expired.")
#         return None
#     except jwt.InvalidTokenError:
#         print("Invalid token.")
#         return None


# # 検証と時間計測
# start_time = time.time()
# decoded_payload = verify_jwt(token, SECRET_KEY, algorithm)
# end_time = time.time()

# if decoded_payload:
#     print(f"Decoded Payload: {decoded_payload}")
# else:
#     print("Failed to verify the token.")

# print(f"Verification Time: {end_time - start_time:.10f} seconds")
