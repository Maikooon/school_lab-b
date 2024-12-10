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
    total_moves = []
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(r"Program execution time: (\d+)", line)
            if match:
                if int(match.group(1)) < 1400000000:
                    execution_times.append(
                        int(match.group(1))
                    )  # 実行時間をナノ秒で取得
            # 移動回数もカウントして、２で割る
            match2 = re.search(r"Total moves across communities: (\d+)", line)
            if match2:
                # 実行方法を途中で変更したので揃える
                # もひし50000 以上ならば、わる、以下ならばそのまま
                if int(match2.group(1)) > 50000:
                    half_moves = float(match2.group(1)) / 2

                half_moves = float(match2.group(1)) / 2  # Divide by 2
                # print(half_moves)
                total_moves.append(half_moves)
    # print(execution_times)
    return execution_times, total_moves


# 直感のファイルを見て、defaultの時間はx=0に、access.txtの時間はx=100にプロットする


def process_additional_files(default_file, access_file):
    """
    default.txt と access.txt を処理し、それぞれ x=0 と x=100 のデータとして追加
    """
    data = []
    count_data = []

    # default.txt の時間を x=0 として追加
    if os.path.exists(default_file):
        default_times, default_count = extract_execution_time(default_file)
        data.extend([(-1, time) for time in default_times])  # x=0
        count_data.extend([(-1, count) for count in default_count])

    # access.txt の時間を x=100 として追加
    if os.path.exists(access_file):
        access_times, access_count = extract_execution_time(access_file)
        data.extend([(-2, time) for time in access_times])  # x=100
        count_data.extend([(-2, count) for count in access_count])
    return data, count_data


def process_additional_files(default_file, access_file):
    """
    default.txt と access.txt を処理し、x軸に沿った水平線データとして追加
    """
    lines = []

    # default.txt のデータを x = 0 の範囲で追加
    if os.path.exists(default_file):
        default_times, _ = extract_execution_time(default_file)
        if default_times:
            avg_time = sum(default_times) / len(default_times)
            lines.append({"x_range": (0.5, 10.5), "y": avg_time, "label": "Default"})

    # access.txt のデータを x = 100 の範囲で追加
    if os.path.exists(access_file):
        access_times, _ = extract_execution_time(access_file)
        if access_times:
            avg_time = sum(access_times) / len(access_times)
            lines.append({"x_range": (0.5, 10.5), "y": avg_time, "label": "Access"})

    return lines


def process_folders(base_dir):
    """
    METIS-ca以下のフォルダを順番に見ていき、データを収集
    """
    data = []  # ノード数と実行時間を格納
    move_data = []  # ノード数とまたぎ回数を格納
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
                times, counts = extract_execution_time(group_access_path)
                # 時間とグループ数
                data.extend([(node_count, time) for time in times])
                #  またぎ回数とグループ数
                move_data.extend([(node_count, count) for count in counts])
    # (10, [879531417, 1107503292, 943199291, 862074542, 874861291, 822483709, 872804708, 862436334]),
    # print(move_data)
    return sorted(data), sorted(move_data)  # ノード数でソート


# 横たてのペアがセットになった配列を格納する
def plot_execution_times(data, additional_data):
    """
    実行時間データをプロット
    """


#     if not data:
#         print("データが見つかりませんでした。")
#         return

#     node_counts = [item[0] for item in data]
#     execution_times = [item[1] for item in data]

#     # 追加データ (default と access)
#     x_values_additional = [item[0] for item in additional_data]
#     y_values_additional = [item[1] for item in additional_data]

#     plt.figure(figsize=(10, 6))
#     plt.scatter(
#         node_counts, execution_times, marker="o", color="blue", label="Execution Time"
#     )
#     # 追加データの散布図
#     plt.scatter(
#         x_values_additional,
#         y_values_additional,
#         marker="x",
#         color="red",
#         label="Default/Access Time",
#     )

#     plt.xlim(-3, 80)
#     plt.ylim(500000000, 1500000000)
#     # plt.ylim(22000, 32000)
#     plt.xlabel("Number of community groups")
#     plt.ylabel("Execution Time (nanoseconds)")
#     plt.title("Execution Time vs Number of Nodes")
#     plt.grid(True)
#     plt.legend()
#     plt.savefig("ca-scatter_plot.png")
#     plt.show()


# # METIS - com - amazon - connected
# # base_dir = "./ng_0.05/METIS-com-amazon-connected"
# # default_file = "./ng_0.05/METIS-com-amazon-connected/default.txt"  # 指定された default.txt ファイル
# # access_file = (
# #     "./ng_0.05/METIS-com-amazon-connected/access.txt"  # 指定された access.txt ファイル
# # )

# # 実行
# base_dir = "./ng_0.05/METIS-ca"
# default_file = "./ng_0.05/METIS-ca/default.txt"  # 指定された default.txt ファイル
# access_file = "./ng_0.05/METIS-ca/access.txt"  # 指定された access.txt ファイル

# # base_dir = "./ng_0.05/test"
# # default_file = "./ng_0.05/test/default.txt"  # 指定された default.txt ファイル
# # access_file = "./ng_0.05/test/access.txt"  # 指定された access.txt ファイル

# data, count = process_folders(base_dir)
# additional_data, additional_count = process_additional_files(default_file, access_file)

# plot_execution_times(data, additional_data)
# # plot_execution_times(count, additional_count)


import matplotlib.pyplot as plt
import os
import re


def extract_execution_time(file_path):
    """
    group-access.txt から実行時間データを抽出
    """
    execution_times = []
    total_moves = []
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(r"Program execution time: (\d+)", line)
            if match:
                if int(match.group(1)) < 1400000000:
                    execution_times.append(
                        int(match.group(1))
                    )  # 実行時間をナノ秒で取得
            match2 = re.search(r"Total moves across communities: (\d+)", line)
            if match2:
                half_moves = (
                    float(match2.group(1)) / 2
                    if int(match2.group(1)) > 50000
                    else float(match2.group(1))
                )
                total_moves.append(half_moves)
    return execution_times, total_moves


def process_additional_files(default_file, access_file):
    """
    default.txt と access.txt を処理し、x軸に沿った水平線データとして追加
    """
    lines = []

    # default.txt のデータを x = 0 の範囲で追加
    if os.path.exists(default_file):
        default_times, _ = extract_execution_time(default_file)
        if default_times:
            avg_time = sum(default_times) / len(default_times)
            lines.append({"x_range": (0, 80), "y": avg_time, "label": "Default"})

    # access.txt のデータを x = 100 の範囲で追加
    if os.path.exists(access_file):
        access_times, _ = extract_execution_time(access_file)
        if access_times:
            avg_time = sum(access_times) / len(access_times)
            lines.append({"x_range": (0, 80), "y": avg_time, "label": "Access"})

    return lines


def process_folders(base_dir):
    """
    METIS-ca以下のフォルダを順番に見ていき、データを収集
    """
    data = []  # ノード数と実行時間を格納
    move_data = []  # ノード数とまたぎ回数を格納
    for root, dirs, files in os.walk(base_dir):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            group_access_path = os.path.join(dir_path, "group-access.txt")
            if os.path.exists(group_access_path):
                try:
                    node_count = int(directory)  # フォルダ名がノード数と仮定
                except ValueError:
                    continue
                times, counts = extract_execution_time(group_access_path)
                data.extend([(node_count, time) for time in times])
                move_data.extend([(node_count, count) for count in counts])
    return sorted(data), sorted(move_data)


# 一つのデータのみ表示したい時
# def plot_execution_times(data, lines):
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

#     # 水平線データ
#     for line in lines:
#         x_range = line["x_range"]
#         y = line["y"]
#         label = line["label"]
#         plt.hlines(
#             y, x_range[0], x_range[1], colors="red", label=label, linestyles="--"
#         )

#     plt.xlim(0, 80)
#     plt.ylim(500000000, 1500000000)
#     plt.xlabel("Number of community groups")
#     plt.ylabel("Execution Time (nanoseconds)")
#     plt.title("Execution Time vs Number of Nodes")
#     plt.grid(True)
#     plt.legend()
#     plt.savefig("ca-scatter_plot_with_lines.png")
#     plt.show()


# # 実行
# base_dir = "./ng_0.05/METIS-ca"
# default_file = "./ng_0.05/METIS-ca/default.txt"
# access_file = "./ng_0.05/METIS-ca/access.txt"

# data, _ = process_folders(base_dir)
# lines = process_additional_files(default_file, access_file)


# plot_execution_times(data, lines)
def plot_execution_times_multiple(data_sets, line_sets):
    """
    複数の実行時間データセットとそれぞれの水平線をプロット
    """
    if not any(data_sets):
        print("データが見つかりませんでした。")
        return

    plt.figure(figsize=(12, 8))

    # 散布図データ
    colors = ["blue", "red"]
    labels = ["CA Dataset", "Amazon Dataset"]
    for i, data in enumerate(data_sets):
        if not data:
            continue
        node_counts = [item[0] for item in data]
        execution_times = [item[1] for item in data]
        plt.scatter(
            node_counts,
            execution_times,
            marker="o",
            color=colors[i],
            label=labels[i],
        )

    # 各データセットに対応する水平線をプロット
    for i, lines in enumerate(line_sets):
        for line in lines:
            x_range = line["x_range"]
            y = line["y"]
            label = f"{labels[i]} - {line['label']}"
            plt.hlines(
                y,
                x_range[0],
                x_range[1],
                colors=colors[i],
                label=label,
                linestyles="--",
            )

    plt.xlim(0, 50)
    plt.ylim(500000000, 1300000000)
    plt.xlabel("Number of community groups")
    plt.ylabel("Execution Time (nanoseconds)")
    plt.title("Execution Time Comparison: CA vs Amazon")
    plt.grid(True)
    plt.legend()
    plt.savefig("ca_amazon_scatter_plot.png")
    plt.show()


# 実行
ca_base_dir = "./ng_0.05/METIS-ca"
ca_default_file = "./ng_0.05/METIS-ca/default.txt"
ca_access_file = "./ng_0.05/METIS-ca/access.txt"

amazon_base_dir = "./ng_0.05/METIS-com-amazon-connected"
amazon_default_file = "./ng_0.05/METIS-com-amazon-connected/default.txt"
amazon_access_file = "./ng_0.05/METIS-com-amazon-connected/access.txt"


# CAとAmazonのデータをそれぞれ取得
ca_data, _ = process_folders(ca_base_dir)
amazon_data, _ = process_folders(amazon_base_dir)

# DefaultとAccessの水平線をそれぞれ取得
ca_lines = process_additional_files(ca_default_file, ca_access_file)
amazon_lines = process_additional_files(amazon_default_file, amazon_access_file)

# プロット
plot_execution_times_multiple([ca_data, amazon_data], [ca_lines, amazon_lines])
