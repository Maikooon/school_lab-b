import glob
import numpy as np
import os

# グラフのノード数とエッジ数を定義
graph_info = {
    "ca-grqc-connected": 4158,
    "cmu": 10,
    "com-amazon-connected": 334863,
    "email-enron-connected": 33696,
    "fb-caltech-connected": 762,
    "fb-pages-company": 14113,
    "fb-pages-food": 620,
    "karate-graph": 34,
    "karate": 34,
    "modularity": 10,
    "ns": 9,
    "prefectures": 47,
    "rt-retweet": 96,
    "simple_graph": 9,
    "soc-slashdot": 70068,
    "tmp": 22,
}

# 基本ディレクトリのパス
# base_path = "./every-time-construction/result/"
base_path = "./default-jwt/result/"
# base_path = ".//result/"

# 各フォルダを探索
folders = glob.glob(base_path + "*/")


# 結果を保存するファイルをオープン
with open(base_path + "folder_stats.txt", "w") as outfile:

    # 各フォルダ内のファイルを探索してデータを収集
    # folders - karate
    for folder in folders:
        outfile.write(f"Processing folder: {folder}\n")
        name = os.path.basename(os.path.normpath(folder))
        node_count = graph_info.get(name, None)
        # print(folder)
        # print(f"Node count: {node_count}")

        # 各フォルダごとにデータのリストを初期化
        average_lengths = []
        total_lengths = []
        total_moves = []
        execution_times = []

        token_generate_times = []
        token_authenticate_times = []

        # ノード数で割った時の時間を求める
        average_times_per_node = []

        # フォルダ内のファイルを取得
        file_paths = glob.glob(folder + "*")

        # ファイルごとにデータを収集
        for file_path in file_paths:
            with open(file_path, "r") as file:
                lines = file.readlines()
                avg_len = float(lines[0].split(":")[1].strip())
                total_len = int(lines[1].split(":")[1].strip())
                total_moves_count = int(lines[2].split(":")[1].strip())
                exec_time = int(lines[3].split(":")[1].strip())

                generate_time = int(lines[4].split(":")[1].strip())
                authenticate_time = int(lines[5].split(":")[1].strip())

                # 各データをリストに追加
                average_lengths.append(avg_len)
                total_lengths.append(total_len)
                total_moves.append(total_moves_count)
                execution_times.append(exec_time)
                token_generate_times.append(generate_time)
                token_authenticate_times.append(authenticate_time)
                average_times_per_node.append(exec_time / node_count)

        # 各フォルダごとに箱ひげ図を描くために必要な統計情報を計算
        average_lengths_stats = {
            "min": np.min(average_lengths),
            "q1": np.percentile(average_lengths, 25),
            "median": np.median(average_lengths),
            "q3": np.percentile(average_lengths, 75),
            "max": np.max(average_lengths),
        }

        total_lengths_stats = {
            "min": np.min(total_lengths),
            "q1": np.percentile(total_lengths, 25),
            "median": np.median(total_lengths),
            "q3": np.percentile(total_lengths, 75),
            "max": np.max(total_lengths),
        }

        total_moves_stats = {
            "min": np.min(total_moves),
            "q1": np.percentile(total_moves, 25),
            "median": np.median(total_moves),
            "q3": np.percentile(total_moves, 75),
            "max": np.max(total_moves),
        }

        execution_times_stats = {
            "min": np.min(execution_times),
            "q1": np.percentile(execution_times, 25),
            "median": np.median(execution_times),
            "q3": np.percentile(execution_times, 75),
            "max": np.max(execution_times),
        }

        token_generate_times_stats = {
            "min": np.min(token_generate_times),
            "q1": np.percentile(token_generate_times, 25),
            "median": np.median(token_generate_times),
            "q3": np.percentile(token_generate_times, 75),
            "max": np.max(token_generate_times),
        }

        token_authenticate_times_stats = {
            "min": np.min(token_authenticate_times),
            "q1": np.percentile(token_authenticate_times, 25),
            "median": np.median(token_authenticate_times),
            "q3": np.percentile(token_authenticate_times, 75),
            "max": np.max(token_authenticate_times),
        }

        average_times_per_node = {
            "min": np.min(average_times_per_node),
            "q1": np.percentile(average_times_per_node, 25),
            "median": np.median(average_times_per_node),
            "q3": np.percentile(average_times_per_node, 75),
            "max": np.max(average_times_per_node),
        }

        # 結果をテキストファイルに書き込む
        outfile.write(f"--- Stats for folder: {folder} ---\n")
        outfile.write(f"Average Length Stats: {average_lengths_stats}\n")
        outfile.write(f"Total Length Stats: {total_lengths_stats}\n")
        outfile.write(f"Total Moves Stats: {total_moves_stats}\n")
        outfile.write(f"Execution Time Stats: {execution_times_stats}\n")
        outfile.write(f"Token Generate Time Stats: {token_generate_times_stats}\n")
        outfile.write(
            f"Token Authenticate Time Stats: {token_authenticate_times_stats}\n"
        )
        outfile.write(f"Average Time Per Node Stats: {average_times_per_node}\n")
        outfile.write("\n")

print("Folder statistics saved to folder_stats.txt")


# nojwtバージョンはこちら


# # 結果を保存するファイルをオープン
# with open(base_path + "folder_stats.txt", "w") as outfile:

#     # 各フォルダ内のファイルを探索してデータを収集
#     # folders - karate
#     for folder in folders:
#         outfile.write(f"Processing folder: {folder}\n")
#         name = os.path.basename(os.path.normpath(folder))
#         node_count = graph_info.get(name, None)
#         # print(folder)
#         # print(f"Node count: {node_count}")

#         # 各フォルダごとにデータのリストを初期化
#         average_lengths = []
#         total_lengths = []
#         total_moves = []
#         execution_times = []

#         # ノード数で割った時の時間を求める
#         average_times_per_node = []

#         # フォルダ内のファイルを取得
#         file_paths = glob.glob(folder + "*")

#         # ファイルごとにデータを収集
#         for file_path in file_paths:
#             with open(file_path, "r") as file:
#                 lines = file.readlines()
#                 avg_len = float(lines[0].split(":")[1].strip())
#                 total_len = int(lines[1].split(":")[1].strip())
#                 total_moves_count = int(lines[2].split(":")[1].strip())
#                 exec_time = int(lines[3].split(":")[1].strip())

#                 # 各データをリストに追加
#                 average_lengths.append(avg_len)
#                 total_lengths.append(total_len)
#                 total_moves.append(total_moves_count)
#                 execution_times.append(exec_time)
#                 average_times_per_node.append(exec_time / node_count)

#         # 各フォルダごとに箱ひげ図を描くために必要な統計情報を計算
#         average_lengths_stats = {
#             "min": np.min(average_lengths),
#             "q1": np.percentile(average_lengths, 25),
#             "median": np.median(average_lengths),
#             "q3": np.percentile(average_lengths, 75),
#             "max": np.max(average_lengths),
#         }

#         total_lengths_stats = {
#             "min": np.min(total_lengths),
#             "q1": np.percentile(total_lengths, 25),
#             "median": np.median(total_lengths),
#             "q3": np.percentile(total_lengths, 75),
#             "max": np.max(total_lengths),
#         }

#         total_moves_stats = {
#             "min": np.min(total_moves),
#             "q1": np.percentile(total_moves, 25),
#             "median": np.median(total_moves),
#             "q3": np.percentile(total_moves, 75),
#             "max": np.max(total_moves),
#         }

#         execution_times_stats = {
#             "min": np.min(execution_times),
#             "q1": np.percentile(execution_times, 25),
#             "median": np.median(execution_times),
#             "q3": np.percentile(execution_times, 75),
#             "max": np.max(execution_times),
#         }

#         average_times_per_node = {
#             "min": np.min(average_times_per_node),
#             "q1": np.percentile(average_times_per_node, 25),
#             "median": np.median(average_times_per_node),
#             "q3": np.percentile(average_times_per_node, 75),
#             "max": np.max(average_times_per_node),
#         }

#         # 結果をテキストファイルに書き込む
#         outfile.write(f"--- Stats for folder: {folder} ---\n")
#         outfile.write(f"Average Length Stats: {average_lengths_stats}\n")
#         outfile.write(f"Total Length Stats: {total_lengths_stats}\n")
#         outfile.write(f"Total Moves Stats: {total_moves_stats}\n")
#         outfile.write(f"Execution Time Stats: {execution_times_stats}\n")
#         outfile.write(f"Average Time Per Node Stats: {average_times_per_node}\n")
#         outfile.write("\n")

# print("Folder statistics saved to folder_stats.txt")
