import matplotlib.pyplot as plt

# データの準備
x = [0.76, 2.545, 3.12, 3.99]
y1 = [12.88, 28.2]  # 速度の改善率
y2 = [0, 7.75]  # 改善率

# グラフの作成
plt.plot(x, y1, label="速度の改善率", marker="o", color="blue")
plt.plot(x, y2, label="改善率", marker="x", color="red")

# グラフのタイトルと軸ラベルの設定
plt.title("回数と改善率の関係")
plt.xlabel("回数")
plt.ylabel("改善率(%)")

# 凡例を表示
plt.legend()

# グリッド線を表示
plt.grid(True)

# グラフを表示
plt.show()
