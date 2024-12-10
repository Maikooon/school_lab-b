import matplotlib.pyplot as plt
import os
import re
from collections import defaultdict


def extract_execution_time(file_path):
    """
    group-access.txt から実行時間データを抽出
    """
    execution_times = []
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(r"Program execution time: (\d+)", line)
            if match:
                if int(match.group(1)) < 1400000000:
                    execution_times.append(int(match.group(1)))
    return execution_times


def process_additional_files(default_file, access_file):
    """
    default.txt と access.txt を処理し、それぞれのデータを返す
    """
    additional_data = defaultdict(list)

    if os.path.exists(default_file):
        default_times = extract_execution_time(default_file)
        additional_data[-1].extend(default_times)  # x=0

    if os.path.exists(access_file):
        access_times = extract_execution_time(access_file)
        additional_data[-2].extend(access_times)  # x=100

    return additional_data


def process_folders(base_dir):
    """
    METIS-ca以下のフォルダを順番に見ていき、データを収集
    """
    data = defaultdict(list)  # ノード数ごとに実行時間を格納
    for root, dirs, files in os.walk(base_dir):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            group_access_path = os.path.join(dir_path, "group-access.txt")
            if os.path.exists(group_access_path):
                try:
                    node_count = int(directory)  # フォルダ名がノード数と仮定
                except ValueError:
                    continue
                times = extract_execution_time(group_access_path)
                data[node_count].extend(times)
    return data


def plot_multiple_boxplots(data1, data2):
    """
    2つの異なるデータセットを同じグラフ上にプロット
    """
    if not data1 or not data2:
        print("いずれかのデータが見つかりませんでした。")
        return

    # データのソート
    sorted_keys1 = sorted(data1.keys())
    sorted_keys2 = sorted(data2.keys())

    # 箱ひげ図用データ準備
    boxplot_data1 = [data1[key] for key in sorted_keys1]
    boxplot_data2 = [data2[key] for key in sorted_keys2]

    # オフセットを用いて位置を調整
    offset = 2
    positions1 = [x - offset for x in sorted_keys1]
    positions2 = [x + offset for x in sorted_keys2]

    plt.figure(figsize=(14, 7))
    # 一つ目のデータセット（例: ca）
    plt.boxplot(
        boxplot_data1,
        positions=positions1,
        widths=3,
        patch_artist=True,
        boxprops=dict(facecolor="lightblue"),
        label="METIS-ca",
    )

    # 二つ目のデータセット（例: amazon）
    plt.boxplot(
        boxplot_data2,
        positions=positions2,
        widths=3,
        patch_artist=True,
        boxprops=dict(facecolor="lightgreen"),
        label="METIS-amazon",
    )

    # グラフ設定
    plt.xlabel("Number of community groups (Node Count)")
    plt.ylabel("Execution Time (nanoseconds)")
    plt.title("Execution Time Distribution by Node Count")
    plt.grid(axis="y")
    plt.xticks(sorted_keys1, rotation=45)  # X軸の値をノード数に合わせて表示
    plt.legend(["METIS-ca", "METIS-amazon"], loc="upper left")
    plt.savefig("multiple-boxplots.png")
    plt.show()


# caとamazonのデータを取得（同様の方法で処理）
base_dir_ca = "./ng_0.05/METIS-ca"
default_file_ca = "./ng_0.05/METIS-ca/default.txt"
access_file_ca = "./ng_0.05/METIS-ca/access.txt"

base_dir_amazon = "./ng_0.05/METIS-com-amazon-connected"
default_file_amazon = "./ng_0.05/METIS-com-amazon-connected/default.txt"
access_file_amazon = "./ng_0.05/METIS-com-amazon-connected/access.txt"

data_ca = process_folders(base_dir_ca)
additional_data_ca = process_additional_files(default_file_ca, access_file_ca)
data_ca.update(additional_data_ca)

data_amazon = process_folders(base_dir_amazon)
additional_data_amazon = process_additional_files(
    default_file_amazon, access_file_amazon
)
data_amazon.update(additional_data_amazon)

# 箱ひげ図のプロット
plot_multiple_boxplots(data_ca, data_amazon)


# def plot_boxplot(data, additional_data):
#     """
#     実行時間データを箱ひげ図としてプロット
#     """
#     if not data:
#         print("データが見つかりませんでした。")
#         return

#     # データのマージ
#     merged_data = data.copy()
#     for key, values in additional_data.items():
#         merged_data[key].extend(values)

#     # X軸の値をソートして取得
#     sorted_keys = sorted(merged_data.keys())

#     # 箱ひげ図用データ準備
#     boxplot_data = [merged_data[key] for key in sorted_keys]

#     plt.figure(figsize=(12, 6))
#     # 一つ目のデータ
#     plt.boxplot(boxplot_data, positions=sorted_keys, widths=4)
#     # 二つ目のデータ
#     plt.boxplot()

#     plt.xlabel("Number of community groups (Node Count)")
#     plt.ylabel("Execution Time (nanoseconds)")
#     plt.title("Execution Time Distribution by Node Count")
#     plt.grid(axis="y")
#     plt.xticks(sorted_keys)  # X軸の値を明示的に指定
#     plt.savefig("caa-boxplot.png")
#     plt.show()


# フォルダとファイルの指定
# base_dir = "./ng_0.05/METIS-com-amazon-connected"
# default_file = "./ng_0.05/METIS-com-amazon-connected/default.txt"
# access_file = "./ng_0.05/METIS-com-amazon-connected/access.txt"

# # METIS - com - amazon - connected
# base_dir = "./ng_0.05/METIS-ca"
# default_file = "./ng_0.05/METIS-ca/default.txt"  # 指定された default.txt ファイル
# access_file = "./ng_0.05/METIS-ca/access.txt"  # 指定された access.txt ファイル


# # データ収集
# data = process_folders(base_dir)
# additional_data = process_additional_files(default_file, access_file)

# # 箱ひげ図のプロット
# plot_boxplot(data, additional_data)
