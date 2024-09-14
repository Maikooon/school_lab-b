import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os
import re

# データを格納するリスト
total_moves = []
execution_times = []

# データが保存されているフォルダのパス


# ca-grqc-connected

folder_path = "./nojwt/result/cmu/"  # 実際のフォルダパスに置き換えてください

# フォルダ内のすべてのファイルを処理
for filename in os.listdir(folder_path):
    if filename.endswith(""):  # ファイルの拡張子に応じて変更する
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r") as file:
            contents = file.read()
            # 正規表現で必要なデータを抽出
            total_moves_match = re.search(
                r"Total moves across communities:\s*(\d+)", contents
            )
            execution_time_match = re.search(r"Execution time:\s*(\d+)", contents)

            if total_moves_match and execution_time_match:
                total_moves.append(int(total_moves_match.group(1)))
                execution_times.append(int(execution_time_match.group(1)))

# numpy 配列に変換
total_moves = np.array(total_moves)
execution_times = np.array(execution_times)

# データが取得できたことを確認
print("Total moves:", total_moves)
print("Execution times:", execution_times)

# 線形回帰分析
X = total_moves.reshape(-1, 1)  # 1列の2D配列に変換
y = execution_times
# データを整形
X = total_moves.reshape(-1, 1)  # 1列の2D配列に変換
y = execution_times

# 線形回帰モデルの作成
model = LinearRegression()
model.fit(X, y)

# 回帰直線の予測値を計算
y_pred = model.predict(X)

# プロット
plt.scatter(total_moves, execution_times, color="blue", label="Data points")
plt.plot(total_moves, y_pred, color="red", label="Fitted line")
plt.xlabel("Total moves across communities")
plt.ylabel("Execution time(nano sec)")
plt.title("Scatter plot and linear regression line")
plt.legend()
plt.savefig("./nojwt/figure/cmu.png")  # 保存先のパスを適宜変更

# 回帰係数と決定係数を表示
print(f"回帰係数: {model.coef_[0]}")
print(f"切片: {model.intercept_}")
print(f"決定係数 (R^2): {model.score(X, y)}")
