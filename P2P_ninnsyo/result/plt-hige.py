# import matplotlib.pyplot as plt

# # グラフ名のリスト
# GRAPH = ["fb-caltech-connected"]


# # ファイルから実行時間を読み込む関数
# def read_execution_times(filename):
#     default_time = []
#     every_time = []
#     one_time = []
#     with open(filename, "r") as file:
#         current_section = None
#         for line in file:
#             if "default" in line:
#                 current_section = "default"
#             elif "everyTime" in line:
#                 current_section = "every_time"
#             elif "oneTime" in line:
#                 current_section = "one_time"
#             elif (
#                 "Execution time:" in line
#                 or "Total Execution Time:" in line
#                 or "Elapsed time: " in line
#             ):
#                 time_str = (
#                     line.split()[-2]
#                     if line.split()[-1] == "seconds"
#                     else line.split()[-1]
#                 )
#                 time = float(time_str)
#                 if current_section == "default":
#                     default_time.append(time / 10)
#                 elif current_section == "every_time":
#                     every_time.append(time / 10)
#                 elif current_section == "one_time":
#                     one_time.append(time)
#     return default_time, every_time, one_time


# # ファイルから移動回数を読み込む関数
# def read_move_server_count(filename):
#     move_server_count = []
#     with open(filename, "r") as file:
#         for line in file:
#             if "Move Server Count:" in line:
#                 count = int(line.split()[-2])
#                 move_server_count.append(count)
#     return move_server_count


# # メイン処理
# if __name__ == "__main__":
#     for graph in GRAPH:
#         filename = "./../result_experiment_1.txt"

#         # 実行時間と移動回数を読み込む
#         default, every_time, one_time = read_execution_times(filename)
#         move_server_count = read_move_server_count(filename)

#         # 移動回数の平均を計算
#         if move_server_count:
#             ave_move_server_count = (
#                 sum(move_server_count) / len(move_server_count) / 100
#             )
#         else:
#             ave_move_server_count = 0

#         # 実行時間の平均と増加率を計算
#         ave_default = sum(default) / len(default) if default else 0
#         ave_every_time = sum(every_time) / len(every_time) if every_time else 0
#         ave_one_time = sum(one_time) / len(one_time) if one_time else 0

#         diff12 = (
#             (ave_every_time - ave_default) / ave_default * 100 if ave_default else 0
#         )
#         diff13 = (ave_one_time - ave_default) / ave_default * 100 if ave_default else 0

#         # ボックスプロットを作成
#         plt.figure(figsize=(10, 6))
#         plt.boxplot(
#             [default, every_time, one_time],
#             labels=["default", "every_time", "one_time"],
#         )
#         plt.text(
#             0.9,
#             0.9,
#             f"every time: {diff12:.2f}% up, one time: {diff13:.2f}% up",
#             ha="center",
#             transform=plt.gca().transAxes,
#         )

#         # グラフのタイトルとラベル
#         plt.title(
#             # f"Comparison of RW Execution Times for {graph} -- Move server count: {ave_move_server_count:.2f}"
#             f"Comparison of RW Execution Times for {graph}"
#         )
#         plt.ylabel("Execution Time (s)")
#         plt.grid(True)

#         # グラフの保存
#         plt.savefig(f"./[experiment1]1Rwerあたりの実行時間.png")
#         plt.show()


# それぞれの内訳を示すグラフを作成す
# 各セクションのデータ

import matplotlib.pyplot as plt
import numpy as np

every_time_data = [
    {
        "total": 6.687,
        "token_gen": 0.0023,
        "token_ver": 0.0046,
        "server_conn": 8.418961692601442,
        "node_access": 0.0117,
    },
    {
        "total": 10.6106,
        "token_gen": 0.0034,
        "token_ver": 0.0039,
        "server_conn": 7.829825356602669,
        "node_access": 0.0299,
    },
    {
        "total": 10.1551,
        "token_gen": 0.0033,
        "token_ver": 0.0042,
        "server_conn": 8.432891368865967,
        "node_access": 0.0214,
    },
    {
        "total": 9.8572,
        "token_gen": 0.0048,
        "token_ver": 0.0108,
        "server_conn": 34.30619567260146,
        "node_access": 0.0337,
    },
    {
        "total": 9.5572,
        "token_gen": 0.0048,
        "token_ver": 0.0108,
        "server_conn": 34.30619567260146,
        "node_access": 0.0337,
    },
]

one_time_data = [
    {
        "total": 0.7569,
        "token_gen": 0.0001,
        "token_ver": 0.00016988441348075867,
        "server_conn": 0.0,
        "node_access": 0.00002699717879295349,
    },
    {
        "total": 0.3543,
        "token_gen": 0.0,
        "token_ver": 0.0003601983189582825,
        "server_conn": 0.0,
        "node_access": 0.0,
    },
    {
        "total": 0.8131,
        "token_gen": 0.0002,
        "token_ver": 0.00025809556245803833,
        "server_conn": 0.4011971466243267,
        "node_access": 0.0009567,
    },
    {
        "total": 1.0609,
        "token_gen": 0.0001,
        "token_ver": 0.00023922696709632874,
        "server_conn": 0.401103962212801,
        "node_access": 0.0006289,
    },
    {
        "total": 0.7564,
        "token_gen": 0.0001,
        "token_ver": 0.0001578,
        "server_conn": 0.0,
        "node_access": 0.00003524,
    },
]

default_data = [
    {
        "total": 3.4723,
        "token_gen": 0.0,
        "token_ver": 0.0,
        "server_conn": 0.0,
        "node_access": 0.0016,
    },
    {
        "total": 3.4723,
        "token_gen": 0.0,
        "token_ver": 0.0,
        "server_conn": 0.0,
        "node_access": 0.0016,
    },
    {
        "total": 2.7219,
        "token_gen": 0.0,
        "token_ver": 0.0,
        "server_conn": 0.0,
        "node_access": 0.0123,
    },
    {
        "total": 4.1803,
        "token_gen": 0.0,
        "token_ver": 0.0,
        "server_conn": 0.0,
        "node_access": 0.0206,
    },
    {
        "total": 2.0157,
        "token_gen": 0.0,
        "token_ver": 0.0,
        "server_conn": 0.0,
        "node_access": 0.0014,
    },
]


# 平均値を計算する関数
def calculate_averages(data):
    keys = ["total", "token_gen", "token_ver", "server_conn", "node_access"]
    averages = {key: sum(d[key] for d in data) / len(data) for key in keys}
    arrays = {key: [d[key] for d in data] for key in keys}
    return arrays, averages


# 各セクションの計算
every_time_arrays, every_time_averages = calculate_averages(every_time_data)
one_time_arrays, one_time_averages = calculate_averages(one_time_data)
default_arrays, default_averages = calculate_averages(default_data)

# 結果を出力
print("Every Time:")
print("Arrays:", every_time_arrays)
print("Averages:", every_time_averages)

print("\nOne Time:")
print("Arrays:", one_time_arrays)
print("Averages:", one_time_averages)

print("\nDefault:")
print("Arrays:", default_arrays)
print("Averages:", default_averages)

# 各カテゴリのデータ
# every_time_totals = every_time_arrays["total"]
# one_time_totals = one_time_arrays["total"]
# default_totals = default_arrays["total"]

# # データとカテゴリを定義
# data1 = [default_totals, every_time_totals, one_time_totals]
# categories1 = ["Default", "Every Time", "One Time"]  # 必ず `data` と同じ数の要素にする

# # 箱ひげ図の描画
# plt.figure(figsize=(10, 6))
# plt.boxplot(
#     data1, tick_labels=categories1
# )  # Matplotlib 3.9以降では `tick_labels` を使う
# plt.title("Distribution of Total Execution Times")
# plt.ylabel("Total Execution Time (seconds)")
# plt.grid(axis="y")
# plt.savefig(f"./[experiment1]1Rwerあたりの実行時間.png")
# # plt.show()

###################################################################


default_arrays_total = default_arrays["total"]
# 各カテゴリのデータ
every_time_total = every_time_arrays["total"]
every_time_token_gen = every_time_arrays["token_gen"]
every_time_token_ver = every_time_arrays["token_ver"]
every_time_node_access = every_time_arrays["node_access"]
every_time_server_con = [
    total - (token_gen + token_ver + node_access) - default
    for total, token_gen, token_ver, node_access, default in zip(
        every_time_total,
        every_time_token_gen,
        every_time_token_ver,
        every_time_node_access,
        default_arrays_total,
    )
]
every_time_total = [value / 10 for value in every_time_total]
every_time_token_gen = [value / 10 for value in every_time_token_gen]
every_time_token_ver = [value / 10 for value in every_time_token_ver]
every_time_node_access = [value / 10 for value in every_time_node_access]
every_time_server_con = [value / 10 for value in every_time_server_con]

data2 = [
    every_time_token_gen,
    every_time_token_ver,
    every_time_node_access,
    # every_time_server_con,
]

categories2 = ["token_gen", "token_ver", "node_access"]
plt.figure(figsize=(10, 6))
plt.boxplot(
    data2, tick_labels=categories2
)  # Matplotlib 3.9以降では `tick_labels` を使う
plt.title("Distribution of Total Execution Times")
plt.ylabel("Total Execution Time (seconds)")
plt.grid(axis="y")
plt.savefig(f"./[experiment1]1Rwerあたりの実行時間内訳.png")
plt.show()
############################################################################

# # # グラフ名のリスト
# default_arrays_total = default_arrays["total"]
# # これは10回分なのでわる
# default_arrays_total = [value / 10 for value in default_arrays_total]


# one_time_total = one_time_arrays["total"]
# one_time_token_gen = one_time_arrays["token_gen"]
# one_time_token_ver = one_time_arrays["token_ver"]
# one_time_node_access = one_time_arrays["node_access"]
# one_time_server_con = [
#     total - (token_gen + token_ver + node_access) - default
#     for total, token_gen, token_ver, node_access, default in zip(
#         one_time_total,
#         one_time_token_gen,
#         one_time_token_ver,
#         one_time_node_access,
#         default_arrays_total,
#     )
# ]

# data3 = [
#     one_time_token_gen,
#     one_time_token_ver,
#     one_time_node_access,
#     # one_time_server_con,
# ]

# categories3 = [
#     "token_gen",
#     "token_ver",
#     "node_access",
#     # "server_conn",
# ]

# print(one_time_server_con)
# plt.figure(figsize=(10, 6))
# plt.boxplot(
#     data3, tick_labels=categories3
# )  # Matplotlib 3.9以降では `tick_labels` を使う
# plt.title("Distribution of Total Execution Times")
# plt.ylabel("Total Execution Time (seconds)")
# plt.grid(axis="y")
# plt.savefig(f"./[experiment1]1Rwerあたりの実行時間内訳-一回.png")
plt.show()
