import os

# ベースディレクトリとファイルのテンプレートを指定
base_dir = "./result/ng_0.05/METIS-ca"
sub_dirs = [3, 10, 20, 30, 40, 50, 60, 70]  # 対象ディレクトリ番号
file_names = ["dynamic_groups.txt", "node_community.txt"]
num_for_graph = []
total_for_graph = []

# サブディレクトリごとに合計を計算
for sub_dir in sub_dirs:
    total_size = 0  # このサブディレクトリでの合計サイズ
    print(f"サブディレクトリ: {base_dir}/{sub_dir}")

    for file_name in file_names:
        file_path = f"{base_dir}/{sub_dir}/{file_name}"
        try:
            file_size = os.path.getsize(file_path)
            total_size += file_size
            print(f"  {file_name}: {file_size} バイト")
        except FileNotFoundError:
            print(f"  {file_name}: ファイルが見つかりません")

    print(f"合計サイズ: {total_size} バイト\n")
    total_for_graph.append(total_size)
    num_for_graph.append(sub_dir)
num_for_graph.append(90)
total_for_graph.append(3274880)

# ここから棒グラフをかく
print(num_for_graph, total_for_graph)

# 　棒グラフをかく
import matplotlib.pyplot as plt
import numpy as np

x = np.array(num_for_graph)
width = 3
plt.xlabel("Number of communities")
plt.ylabel("Total size (bytes)")
plt.ylim(0, 100000)
plt.subplots_adjust(left=0.15)  # 左余白を15%に設定


plt.bar(
    x,
    total_for_graph,
    color="green",
    width=width,
)
plt.savefig("result.pdf")
plt.show()
