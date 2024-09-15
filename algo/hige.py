import glob
import numpy as np
import os

# 基本ディレクトリのパス
base_path = "./nojwt/result/"

# 各フォルダを探索
folders = glob.glob(base_path + "*/")

# 結果を保存するファイルをオープン
with open(base_path + "folder_stats.txt", "w") as outfile:
    
    # 各フォルダ内のファイルを探索してデータを収集
    for folder in folders:
        outfile.write(f"Processing folder: {folder}\n")
        
        # 各フォルダごとにデータのリストを初期化
        average_lengths = []
        total_lengths = []
        total_moves = []
        execution_times = []
        
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

                # 各データをリストに追加
                average_lengths.append(avg_len)
                total_lengths.append(total_len)
                total_moves.append(total_moves_count)
                execution_times.append(exec_time)

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

        # 結果をテキストファイルに書き込む
        outfile.write(f"--- Stats for folder: {folder} ---\n")
        outfile.write(f"Average Length Stats: {average_lengths_stats}\n")
        outfile.write(f"Total Length Stats: {total_lengths_stats}\n")
        outfile.write(f"Total Moves Stats: {total_moves_stats}\n")
        outfile.write(f"Execution Time Stats: {execution_times_stats}\n")
        outfile.write("\n")

print("Folder statistics saved to folder_stats.txt")
