import os
import re
import matplotlib.pyplot as plt
import numpy as np


def extract_execution_time(file_path):
    """
    指定されたファイルから実行時間データを抽出
    """
    execution_times = []
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(r"Program execution time: ([\d,]+)", line)
            if match:
                # 数字を整数に変換
                execution_times.append(int(match.group(1).replace(",", "")))
    return execution_times


def process_additional_files(default_file, access_file, label_default, label_access):
    """
    default.txt と access.txt を処理し、それぞれのデータを指定されたラベルに割り当てる
    """
    data = {}

    # default.txt のデータを収集
    if os.path.exists(default_file):
        default_times = extract_execution_time(default_file)
        data[label_default] = default_times

    # access.txt のデータを収集
    if os.path.exists(access_file):
        access_times = extract_execution_time(access_file)
        data[label_access] = access_times

    return data


# def plot_bar_chart(data):
#     """
#     実行時間データを棒グラフでプロット (X軸を文字列で表示)
#     """
#     if not data:
#         print("データが見つかりませんでした。")
#         return

#     # データを分解
#     x_labels = list(data.keys())  # X軸のラベル (文字列)
#     mean_times = [np.mean(data[label]) for label in x_labels]  # 平均値

#     x_positions = np.arange(len(x_labels))  # X軸位置

#     # 二つの差分をいかの比率で分割して、色を変えてヒョジして、つまり、右おAccessのグラフは3色になる
#     # 約37.96%

#     plt.figure(figsize=(10, 6))
#     plt.bar(
#         x_positions,
#         mean_times,
#         color=["grey", "green"],  # 各カテゴリの色
#         alpha=0.7,
#         edgecolor="black",
#     )

#     # 軸設定
#     plt.xlabel("Categories")
#     plt.ylabel("Average Execution Time (nanoseconds)")
#     plt.title("Average Execution Time by Category")
#     plt.xticks(x_positions, x_labels)  # X軸に文字列ラベルを割り当て
#     plt.grid(axis="y", linestyle="--", alpha=0.7)
#     plt.savefig("1-bar_chart.png")
#     plt.show()


##TODO:ここまでじは普通のグラフ
def plot_bar_chart(data):
    """
    実行時間データを棒グラフでプロット (X軸を文字列で表示し、右側は3色で分割)
    """
    if not data:
        print("データが見つかりませんでした。")
        return

    # データを分解
    x_labels = list(data.keys())  # X軸のラベル (文字列)
    mean_times = [np.mean(data[label]) for label in x_labels]  # 平均値
    # 配列の各要素を1000000000で割る
    mean_times = [x / 1000000000 for x in mean_times]
    x_positions = np.arange(len(x_labels))  # X軸位置

    print(mean_times)

    # 比率に基づく棒グラフの分割 (37.96%)
    split_ratio = 0.3796
    plt.figure(figsize=(5, 6))

    # for i, mean_time in enumerate(mean_times):
    #     if i == len(mean_times) - 1:  # 最後の棒だけ3色で分割.ここはそれぞれの色の高さなので全体からみた高さではない
    top_height = (mean_times[1] - mean_times[0]) * (1 - split_ratio)
    mid_height = (mean_times[1] - mean_times[0]) * split_ratio
    bottom_height = 0.67582696
    # ここから追加する
    print("top_height", top_height)
    print("mid_height", mid_height)
    bottom_height_2 = 0.67582696 * 0.841
    mid_height = 0.67582696 * 0.076
    top_height = 0.67582696 * 0.063
    # bottom_height 0.6101654625555556
    print("bottom_height", bottom_height)

    # 上部
    plt.bar(
        x_positions[1],
        top_height,
        bottom=bottom_height_2 + mid_height,
        color="#F9A8D4",
        edgecolor="black",
        label="token creation (6.3%)",
    )

    # # 中央
    plt.bar(
        x_positions[1],
        mid_height,
        bottom=bottom_height_2,
        color="#F8D0D0",
        edgecolor="black",
        label="token verification (7.6%)",
    )

    # 下部
    plt.bar(
        x_positions[1],
        bottom_height_2,
        bottom=0,
        color="#FBB6B6",
        edgecolor="black",
        label="communication time (84.1%)",
    )
    #  カスタム判例を追加
    # else:
    plt.bar(
        x_positions[0],
        0.67582696,
        bottom=0,
        color="#F87171",
        edgecolor="black",
        # label="Other Categories" if i == 0 else "",
    )

    # 軸設定
    plt.xlabel("Categories")
    plt.ylabel("Average Execution Time (nanoseconds)")
    # plt.title("Average Execution Time by Category")
    plt.xticks(x_positions, x_labels)  # X軸に文字列ラベルを割り当て
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(loc="upper left")
    # plt.savefig("1-bar_chart_split.png")
    plt.savefig("1-bar_chart_split-0124.pdf")
    plt.show()


# 実行部分
default_file = "./ng_0.05/METIS-ca/default.txt"  # 指定された default.txt ファイル
access_file = "./ng_0.05/METIS-ca/access.txt"  # 指定された access.txt ファイル

# ユーザーが指定する X 軸のラベル
label_default = ""
label_access = "add authentication"

# データ収集
data = process_additional_files(default_file, access_file, label_default, label_access)

# プロット (棒グラフ)
plot_bar_chart(data)
