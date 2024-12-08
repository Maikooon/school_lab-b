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


def plot_bar_chart(data):
    """
    実行時間データを棒グラフでプロット (X軸を文字列で表示)
    """
    if not data:
        print("データが見つかりませんでした。")
        return

    # データを分解
    x_labels = list(data.keys())  # X軸のラベル (文字列)
    mean_times = [np.mean(data[label]) for label in x_labels]  # 平均値

    x_positions = np.arange(len(x_labels))  # X軸位置

    plt.figure(figsize=(10, 6))
    plt.bar(
        x_positions,
        mean_times,
        color=["grey", "blue"],  # 各カテゴリの色
        alpha=0.7,
        edgecolor="black",
    )

    # 軸設定
    plt.xlabel("Categories")
    plt.ylabel("Average Execution Time (nanoseconds)")
    plt.title("Average Execution Time by Category")
    plt.xticks(x_positions, x_labels)  # X軸に文字列ラベルを割り当て
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.savefig("1-bar_chart.png")
    plt.show()


# 実行部分
default_file = "./ng_0.05/METIS-ca/default.txt"  # 指定された default.txt ファイル
access_file = "./ng_0.05/METIS-ca/access.txt"  # 指定された access.txt ファイル

# ユーザーが指定する X 軸のラベル
label_default = "Default"
label_access = "Access"

# データ収集
data = process_additional_files(default_file, access_file, label_default, label_access)

# プロット (棒グラフ)
plot_bar_chart(data)
