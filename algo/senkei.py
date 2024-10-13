import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import LinearRegression
import os
import re

# データを格納するリスト
total_moves = []
execution_times = []

# データが保存されているフォルダのパス
# フォルダーパスを設定
# every-time-construction  default-jwt
FOLDER = "every-time-construction"
path = "./" + FOLDER + "/result/"

file_list = [
    "ca-grqc-connected",
    "cmu",
    "com-amazon-connected",
    "email-enron-connected",
    "fb-caltech-connected",
    "fb-pages-company",
    "karate-graph",
    "karate",
    "rt-retweet",
    "simple_graph",
    "soc-slashdot",
    "tmp",
]


# グラフ名を番号で選択する関数
def select_graph_file():
    print("利用可能なグラフファイル:")
    for idx, filename in enumerate(file_list):
        print(f"{idx}: {filename}")

    while True:
        try:
            selection = int(input("ファイル番号を選択してください: "))
            if 0 <= selection < len(file_list):
                return file_list[selection]
            else:
                print("無効な番号です。もう一度試してください。")
        except ValueError:
            print("無効な入力です。数字を入力してください。")


# 選択したグラフファイル名を取得
selected_file = select_graph_file()
folder_path = os.path.join(path, selected_file)

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
# MSE と MAE の計算
mse = mean_squared_error(y, y_pred)
mae = mean_absolute_error(y, y_pred)

# 標準化誤差の計算
nmae = mae / (np.max(y) - np.min(y))
nmse = mse / ((np.max(y) - np.min(y)) ** 2)

# 相対誤差の計算
relative_error = np.abs((y - y_pred) / y)
mean_relative_error = np.mean(relative_error)

# プロット
plt.scatter(total_moves, execution_times, color="blue", label="Data points")
plt.plot(total_moves, y_pred, color="red", label="Fitted line")
plt.xlabel("Total moves across communities")
plt.ylabel("Execution time(nano sec)")
plt.title("Scatter plot and linear regression line")
plt.legend()
# output_path = "./" + FOLDER + "/figure/" + selected_file + ".png"
output_path = "./test.png"
plt.savefig(output_path)  # 保存先のパスを適宜変更

# 回帰係数と決定係数を表示
print(f"決定係数 (R^2): {model.score(X, y)}")
print(f"標準化平均二乗誤差 (NMSE): {nmse}")
print(f"標準化平均絶対誤差 (NMAE): {nmae}")
print(f"平均相対誤差: {mean_relative_error}")
