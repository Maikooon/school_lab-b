"""
横軸: ノード数
縦軸: 実行時間
のグラフを作成する

描画するフォルダ: new-algo/result-1207/ng_0.05/METIS-ca/ノード数
このフォルダ下にあるgroup-access.txtのファイルを読み込む
Average path length: 6.732800
Total moves across communities: 51360
Program execution time: 1267790417 nanoseconds
Program execution time: 1,267,790,417 nanoseconds......が繰り返される

同じグループ数のフォルダ下にあるものは同じx軸上に描画

つまり、フォルダの数がけX軸のメモリの数になる




"""

import matplotlib.pyplot as plt
import os
import re
import matplotlib.pyplot as plt


def extract_execution_time(file_path):
    """
    group-access.txt から実行時間データを抽出
    """
    execution_times = []
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(r"Program execution time: (\d+)", line)
            if match:
                execution_times.append(int(match.group(1)))  # 実行時間をナノ秒で取得
    print(execution_times)
    return execution_times


# 直感のファイルを見て、defaultの時間はx=0に、access.txtの時間はx=100にプロットする
def extract_execution_time(file_path):
    """
    group-access.txt または default.txt から実行時間データを抽出
    """
    execution_times = []
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(r"Program execution time: (\d+)", line)
            if match:
                execution_times.append(int(match.group(1)))  # 実行時間をナノ秒で取得
    return execution_times


def process_additional_files(default_file, access_file):
    """
    default.txt と access.txt を処理し、それぞれ x=0 と x=100 のデータとして追加
    """
    data = []

    # default.txt の時間を x=0 として追加
    if os.path.exists(default_file):
        default_times = extract_execution_time(default_file)
        data.extend([(0, time) for time in default_times])  # x=0

    # access.txt の時間を x=100 として追加
    if os.path.exists(access_file):
        access_times = extract_execution_time(access_file)
        data.extend([(100, time) for time in access_times])  # x=100

    print(data)
    print(data)
    return data


def process_folders(base_dir):
    """
    METIS-ca以下のフォルダを順番に見ていき、データを収集
    """
    data = []  # ノード数と実行時間を格納
    for root, dirs, files in os.walk(base_dir):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            group_access_path = os.path.join(dir_path, "group-access.txt")
            if os.path.exists(group_access_path):
                # ノード数をフォルダ名から取得
                try:
                    node_count = int(directory)  # フォルダ名がノード数と仮定
                except ValueError:
                    continue
                # 実行時間を抽出
                times = extract_execution_time(group_access_path)
                data.extend([(node_count, time) for time in times])
    # (10, [879531417, 1107503292, 943199291, 862074542, 874861291, 822483709, 872804708, 862436334]),
    return sorted(data)  # ノード数でソート


def plot_execution_times(data, additional_data):
    """
    実行時間データをプロット
    """
    if not data:
        print("データが見つかりませんでした。")
        return

    node_counts = [item[0] for item in data]
    execution_times = [item[1] for item in data]

    # 追加データ (default と access)
    x_values_additional = [item[0] for item in additional_data]
    y_values_additional = [item[1] for item in additional_data]

    plt.figure(figsize=(10, 6))
    plt.scatter(
        node_counts, execution_times, marker="o", color="blue", label="Execution Time"
    )
    # 追加データの散布図
    plt.scatter(
        x_values_additional,
        y_values_additional,
        marker="x",
        color="red",
        label="Default/Access Time",
    )
    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (nanoseconds)")
    plt.title("Execution Time vs Number of Nodes")
    plt.grid(True)
    plt.legend()
    plt.show()


# 実行
base_dir = "./ng_0.05/METIS-ca"
default_file = "./ng_0.05/METIS-ca/default.txt"  # 指定された default.txt ファイル
access_file = "./ng_0.05/METIS-ca/access.txt"  # 指定された access.txt ファイル

data = process_folders(base_dir)
additional_data = process_additional_files(default_file, access_file)

plot_execution_times(data, additional_data)
