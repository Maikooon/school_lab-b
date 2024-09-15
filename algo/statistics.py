# This Python script is reading statistical information from a file and creating box plots for
# different metrics. Here's a breakdown of what the script is doing:
# """
#     すでに統計情報が算出されたファイルを読み取ってグラフに描画する方法
#     統計情報を出すためのスクリプトは、algo/analyze.pyにある

# """

# import matplotlib.pyplot as plt
# import pandas as pd
# import re
# import os

# # データファイルのパス
# data_file = "./every-time-construction/result/statistics.txt"
# # 保存先のディレクトリを作成
# output_dir = "./figure"

# # データを格納する辞書
# data = {}

# # データをファイルから読み取る
# with open(data_file, "r") as file:
#     folder_name = None
#     for line in file:
#         # フォルダ名の行を処理
#         if line.startswith("Folder:"):
#             folder_name = line.split(":", 1)[1].strip()
#             data[folder_name] = {
#                 "Average length": [],
#                 "Total length": [],
#                 "Total moves across communities": [],
#                 "Execution time": [],
#                 "Token generate time": [],
#                 "Token authenticate time": [],
#             }
#         elif folder_name:
#             # 各メトリックの行を処理
#             for metric in data[folder_name]:
#                 if metric in line:
#                     values = re.findall(r"([\d\.]+)", line)
#                     if len(values) >= 1:  # 1つ以上の値が含まれていることを確認
#                         data[folder_name][metric] = [float(v) for v in values]

# os.makedirs(output_dir, exist_ok=True)

# # 各メトリックごとに箱ひげ図を描画し、個別のファイルに保存
# for metric in data[list(data.keys())[0]]:
#     fig, ax = plt.subplots(figsize=(10, 6))
#     metric_data = [data[folder][metric] for folder in data]

#     # 箱ひげ図を描く
#     ax.boxplot(metric_data, labels=list(data.keys()))
#     ax.set_title(metric)
#     ax.set_ylabel("Value")
#     ax.set_xlabel("Folder")

#     # プロットを保存
#     output_file = os.path.join(output_dir, f'{metric.replace(" ", "_")}_boxplot.png')
#     plt.savefig(output_file)
#     plt.close(fig)

# print(f"Boxplots saved in {output_dir}")
