import matplotlib.pyplot as plt

# データを辞書形式で準備
data = {
    "karate": {"nodes": 34, "cache_usage": 0.12750},
    "karate-graph": {"nodes": 34, "cache_usage": 0.09976},
    "cmu": {"nodes": 10, "cache_usage": 0.15616},
    "ca-grqc-connected": {"nodes": 4158, "cache_usage": 0.05800},
    # "com-amazon-connected": {"nodes": 334863, "cache_usage": 0.00023},
    "rt-retweet": {"nodes": 96, "cache_usage": 0.11585},
    "tmp": {"nodes": 22, "cache_usage": 0.05000},
    "fb-caltech-connected": {"nodes": 762, "cache_usage": 0.01397},
    "simple_graph": {"nodes": 9, "cache_usage": 0.21160},
}

# ノード数とキャッシュの利用率をリストに格納
nodes = [data[key]["nodes"] for key in data]
cache_usage = [data[key]["cache_usage"] for key in data]

# グラフをプロット
plt.figure(figsize=(10, 6))
plt.scatter(nodes, cache_usage, marker="o")

# グラフにタイトルとラベルを追加
plt.title("Cache Usage Percentage vs Number of Nodes")
plt.xlabel("Number of Nodes")
plt.ylabel("Cache Usage Percentage")

# 各点にラベルを付ける
for i, txt in enumerate(data.keys()):
    plt.annotate(
        txt,
        (nodes[i], cache_usage[i]),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
    )

# グリッドを追加
plt.grid(True)

# グラフを表示
plt.savefig("./../bar-plt/cache-usage-vs-nodes.png")
