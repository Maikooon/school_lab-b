# """
# 横軸: ノード数
# 縦軸: 実行時間
# のグラフを作成する

# 描画するフォルダ: new-algo/result-1207/ng_0.05/METIS-ca/ノード数
# このフォルダ下にあるgroup-access.txtのファイルを読み込む
# Average path length: 6.732800
# Total moves across communities: 51360
# Program execution time: 1267790417 nanoseconds
# Program execution time: 1,267,790,417 nanoseconds......が繰り返される

# 同じグループ数のフォルダ下にあるものは同じx軸上に描画

# つまり、フォルダの数がけX軸のメモリの数になる


# コミュニティ数を変えた時に、時間がどのように変化したのかを見るため

# """

# import matplotlib.pyplot as plt
# import os
# import re
# import matplotlib.pyplot as plt


# def extract_execution_time(file_path):
#     """
#     group-access.txt から実行時間データを抽出
#     """
#     execution_times = []
#     total_moves = []
#     with open(file_path, "r") as file:
#         for line in file:
#             match = re.search(r"Program execution time: (\d+)", line)
#             if match:
#                 # if int(match.group(1)) < 1400000000:
#                 execution_times.append(int(match.group(1)))  # 実行時間をナノ秒で取得
#     return execution_times, total_moves


# # 直感のファイルを見て、defaultの時間はx=0に、access.txtの時間はx=100にプロットする
# def process_additional_files(default_file, access_file):
#     """
#     default.txt と access.txt を処理し、x軸に沿った水平線データとして追加
#     """
#     lines = []

#     # default.txt のデータを x = 0 の範囲で追加
#     if os.path.exists(default_file):
#         default_times, _ = extract_execution_time(default_file)
#         if default_times:
#             avg_time = sum(default_times) / len(default_times)
#             lines.append({"x_range": (0, 0.1), "y": avg_time, "label": "Default"})

#     # access.txt のデータを x = 100 の範囲で追加
#     if os.path.exists(access_file):
#         access_times, _ = extract_execution_time(access_file)
#         if access_times:
#             avg_time = sum(access_times) / len(access_times)
#             lines.append({"x_range": (0, 0.1), "y": avg_time, "label": "Access"})

#     return lines


# def process_folders(base_dir):
#     """
#     METIS-ca以下のフォルダを順番に見ていき、データを収集
#     """
#     data = []  # ノード数と実行時間を格納
#     data2 = []
#     move_data = []  # ノード数とまたぎ回数を格納\
#     move_data2 = []
#     for root, dirs, files in os.walk(base_dir):
#         for directory in dirs:
#             print(directory)
#             dir_path = os.path.join(root, directory)
#             group_access_path = os.path.join(dir_path, "group-access.txt")
#             not_group_access_path = os.path.join(dir_path, "access.txt")

#             if os.path.exists(group_access_path):
#                 try:
#                     node_count = float(directory)  # フォルダ名がノード数と仮定
#                     print("ノード数はこチア", node_count)
#                 except ValueError:
#                     continue
#                 times, counts = extract_execution_time(group_access_path)
#                 data.extend([(node_count, time) for time in times])
#                 move_data.extend([(node_count, count) for count in counts])
#             if os.path.exists(not_group_access_path):
#                 try:
#                     node_count = float(directory)  # フォルダ名がノード数と仮定
#                     print("ノード数はこチア", node_count)
#                 except ValueError:
#                     continue
#                 times2, counts2 = extract_execution_time(not_group_access_path)
#                 data2.extend([(node_count, time2) for time2 in times2])
#                 move_data2.extend([(node_count, count2) for count2 in counts2])
#     print(data)
#     print(data2)
#     return sorted(data), sorted(move_data), sorted(data2), sorted(move_data2)


# # 一つのデータのみ表示したい時
# def plot_execution_times(data, data2):
#     """
#     実行時間データと水平線をプロット
#     """
#     if not data:
#         print("データが見つかりませんでした。")
#         return

#     # 散布図データ
#     node_counts = [item[0] for item in data]
#     execution_times = [item[1] for item in data]

#     plt.figure(figsize=(10, 6))
#     plt.scatter(
#         node_counts, execution_times, marker="o", color="blue", label="Execution Time"
#     )

#     # plt.xlim(0, 80)
#     plt.ylim(500000000, 2000000000)
#     plt.xlabel("Number of community groups")
#     plt.ylabel("Execution Time (nanoseconds)")
#     plt.title("Execution Time vs Number of Nodes")
#     plt.grid(True)
#     plt.legend()
#     plt.savefig("ca-scatter_plot_with_lines.png")
#     plt.show()


# # 実行
# base_dir = "./ng_0.05/METIS-ca-ngrate"

# data, _, data2, _ = process_folders(base_dir)
# plot_execution_times(data, data2)
import matplotlib.pyplot as plt
import os
import re


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
    return execution_times


def process_folders(base_dir):
    """
    METIS-ca以下のフォルダを順番に見ていき、データを収集
    """
    data = []  # group-access.txt のノード数と実行時間を格納
    data2 = []  # access.txt のノード数と実行時間を格納
    for root, dirs, files in os.walk(base_dir):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            group_access_path = os.path.join(dir_path, "group-access.txt")
            access_path = os.path.join(dir_path, "access.txt")

            try:
                node_count = float(directory)  # フォルダ名をノード数として取得
            except ValueError:
                continue

            if os.path.exists(group_access_path):
                times = extract_execution_time(group_access_path)
                data.extend([(node_count, time) for time in times])

            if os.path.exists(access_path):
                times2 = extract_execution_time(access_path)
                data2.extend([(node_count, time2) for time2 in times2])

    return sorted(data), sorted(data2)


def plot_execution_times(data, data2):
    """
    実行時間データを別々の色でプロット
    """
    if not data and not data2:
        print("データが見つかりませんでした。")
        return

    plt.figure(figsize=(10, 6))

    # group-access.txt のデータを青でプロット
    if data:
        node_counts = [item[0] for item in data]
        execution_times = [item[1] for item in data]
        plt.scatter(
            node_counts, execution_times, marker="o", color="blue", label="Group Access"
        )

    # access.txt のデータを緑でプロット
    if data2:
        node_counts2 = [item[0] for item in data2]
        execution_times2 = [item[1] for item in data2]
        plt.scatter(
            node_counts2,
            execution_times2,
            marker="x",
            color="green",
            label="Access",
        )

    # plt.ylim(500000000, 5000000000)
    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (nanoseconds)")
    plt.title("Execution Time vs Number of Nodes")
    plt.grid(True)
    plt.legend()
    plt.savefig("execution_time_comparison.png")
    plt.show()


# 実行
base_dir = "./ng_0.05/METIS-ca-ngrate"

data, data2 = process_folders(base_dir)
plot_execution_times(data, data2)
