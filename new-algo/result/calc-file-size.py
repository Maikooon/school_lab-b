import os
import matplotlib.pyplot as plt


# 指定するファイルとパス
GRAPH = "METIS-karate"  # グラフ名の指定
files = {
    "non-group-ng-nodes.txt": f"./../create-tables/result/{GRAPH}/non-group-ng-nodes.txt",
    "dynamic_groups.txt": f"./../create-tables/result/{GRAPH}/dynamic_groups.txt",
    "ng_nodes.txt": f"./../create-tables/result/{GRAPH}/ng_nodes.txt",
}


def get_file_size(file_path):
    try:
        # ファイルサイズをバイト単位で取得
        size = os.path.getsize(file_path)
        return size
    except FileNotFoundError:
        return None


# ファイルサイズを取得
file_sizes = {file_name: get_file_size(path) for file_name, path in files.items()}

# ファイルサイズの取得結果
for file_name, size in file_sizes.items():
    if size is not None:
        print(f"{file_name} size: {size / 1024:.2f} KB")  # KB単位で表示
    else:
        print(f"{file_name}: File not found.")

# グラフを描画
labels = list(file_sizes.keys())

# ファイルサイズを取得
file_sizes = [get_file_size(path) for path in files.values()]

# sizes = [
#     size / 1024 for size in file_sizes.values() if size is not None
# ]  # KB単位に変換
sizes = [
    round(file_sizes[0] / 1024, 2),
    round((file_sizes[1] + file_sizes[2]) / 1024, 2),
]

sizes_labels = ["access", "group-access"]  # 存在するファイルのみのラベル
loc = ["access:" + str(sizes[0]), "group-access:" + str(sizes[1])]
print(loc)
rate = round(sizes[0] / sizes[1], 2)

plt.figure(figsize=(6, 5))
plt.bar(sizes_labels, sizes, label=loc, color=["#000080", "#808080"])
plt.xlabel(f"access =  group-access*{rate}")
plt.ylabel("File Size (KB)")
plt.legend(loc, loc="upper right")
plt.title(f"{GRAPH} File Size Comparison")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"./../create-tables/result/{GRAPH}/file-size.png")
plt.show()
