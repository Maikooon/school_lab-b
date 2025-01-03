# import matplotlib.pyplot as plt


# def read_data(file_path):
#     x_list = []
#     y_list = []
#     # ファイルを開いてデータをリストに格納
#     with open(file_path, "r") as file:
#         for line in file:
#             if "サーバのまたぎ回数" in line:
#                 x = int(line.split(":")[1])
#                 x_list.append(x)
#             if "total execution time" in line:
#                 y = float(line.split(":")[1].split(" ")[1])
#                 y_list.append(y)
#     return x_list, y_list


# # 各データセットの読み込み
# """
# ここを変更することにより異なるグラフが書ける
# 初めの３つ
# ・デフォルトの時との比較

# 次の３つ
# ・親Tokenを導入した時の比較

# """
# data_files = {
#     "default": "./default/1-log.txt",
#     "every-time": "./every-time/1-log.txt",
#     "first-time": "./first-time/1-log.txt",
#     # "default": "./default/100-log.txt",
#     # "first-time": "./first-time/100-log.txt",
#     # "parent-token": "./parent-token/100-log.txt",
# }

# colors = [
#     "red",
#     "green",
#     "purple",
# ]
# plt.figure(figsize=(8, 6))
# # ux軸の範囲を決めたい
# # plt.xlim(10, 380)

# # 各データセットをプロット
# for label, (color, file_path) in zip(
#     data_files.keys(), zip(colors, data_files.values())
# ):
#     x_list, y_list = read_data(file_path)
#     ## ここまで100回分の平均であるので、すべてを/100して考える
#     # x_list = [x / 100 for x in x_list]
#     # y_list = [y / 100 for y in y_list]
#     plt.scatter(x_list, y_list, label=label, color=color)

# # 軸ラベルと凡例を設定
# plt.xlabel("server across time (times)")
# plt.ylabel("total execution time (s)")
# plt.legend()
# plt.grid(True)

# # グラフを保存および表示
# plt.savefig("[100-time]comparison_plot-2.png")
# plt.show()


"""
基礎評価となるデフォルトと毎回認証のグラフを描画

every-time
total execution time: 2.724355593 seconds, 
サーバのまたぎ回数: 5

default
total execution time: 0.577433061 seconds
サーバのまたぎ回数: 5

total execution time: 0.483004510 seconds
サーバのまたぎ回数: 5

total execution time: 0.494555179 seconds
サーバのまたぎ回数: 5

total execution time: 0.434693161 seconds
サーバのまたぎ回数: 5

total execution time: 0.611061960 seconds
サーバのまたぎ回数: 5

total execution time: 0.485163044 seconds
サーバのまたぎ回数: 5
"""
import matplotlib.pyplot as plt

# Data
categories = [
    "default",
    "every-time",
]
execution_times = [
    (0.577433061 + 0.483004510 + 0.494555179 + 0.434693161 + 0.611061960 + 0.485163044)
    / 6,
    2.724355593,
]
colors = ["grey", "green"]

# Bar Graph
x = range(len(categories))

fig, ax1 = plt.subplots(figsize=(8, 5))

# Bar for Execution Time
ax1.bar(x, execution_times, color=colors, alpha=0.7, label="Execution Time (seconds)")
ax1.set_ylabel("100RW Execution Time (seconds)")
ax1.tick_params(axis="y")
ax1.set_xticks(x)
ax1.set_xticklabels(categories)
ax1.set_xlabel("Category")
ax1.legend(loc="upper left")

# Line Graph for Server Crossings
# ax2 = ax1.twinx()
# ax2.plot(x, server_crossings, color='red', marker='o', label='Server Crossings')
# ax2.set_ylabel('Server Crossings', color='red')
# ax2.tick_params(axis='y', labelcolor='red')
# ax2.legend(loc='upper right')

plt.title("Execution Time and Server Crossings by Category")
plt.tight_layout()
plt.savefig("basic.png")
plt.show()
