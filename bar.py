"""
これは、棒グラフでNGノードの増加率を示すグラフ
"""

import matplotlib.pyplot as plt
import numpy as np

# グラフのデータ
labels = ["fb 0.02    0.17", "ca 0.06   0.113", "fb-pages 0.0002   0.002"]

# 1.増加率を示すデータはこちら
# increase_5 = [110.76, 677.94, 4622.04]
# increase_10 = [264.61, 760.52, 12910.22]

# 2. グループ化による増加率を示すデータはこちら
# increase_5 = [20.78, 18.87, 10.51, 8.68]
# increase_10 = [18.7, 5.1, 2.61, 2.6]


# 3.抑制率を示すデータ
# グループ化による増加率を示すデータはこちら
# increase_5 = [0.829631636, 0.9844971531, 0.9981220413]
# increase_10 = [0.980726352, 0.9965681376, 0.9997986092]

# 　モジュラリティの大きさと抑制率の影響
increase_5 = [0.829631636, 0.9844971531, 0.9981220413]
increase_10 = [0.9636877399, 0.9904237245, 0.9967245042]

# 棒グラフの設定
x = np.arange(len(labels))  # X 軸の位置
width = 0.35  # 棒の幅

# プロット作成
fig, ax = plt.subplots(figsize=(10, 6))
bars_5 = ax.bar(x - width / 2, increase_5, width, label="ng-nodes rate:5%")
bars_10 = ax.bar(x + width / 2, increase_10, width, label="ng-nodes rate:10%")

# ラベルの設定
ax.set_xlabel("kind of graph")
ax.set_ylabel("increasing rate")
ax.set_ylim(0.6, 1.1)
ax.set_title("increasing rate by ng nodes rate")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# 棒の上に値を表示
for bar in bars_5 + bars_10:
    height = bar.get_height()
    ax.annotate(
        f"{height:.2f}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),  # 3ポイント上にオフセット
        textcoords="offset points",
        ha="center",
        va="bottom",
    )

# グリッドの表示
plt.grid(axis="y", linestyle="--", alpha=0.7)

# グラフの表示
plt.tight_layout()
# plt.savefig("increasing-rate-compared-by-ng-nodes.png")
# plt.savefig("[group-access]increasing-rate-compared-by-ng-nodes.png")
plt.savefig("modularity.png")
plt.show()
