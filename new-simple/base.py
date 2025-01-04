"""
基礎評価となるデフォルトと毎回認証のグラフを描画
そもそも。毎回やるのでは時間がかかりすぎるので削減が必要だねよね、という主張に繋げる

"""

"""

every-time
total execution time: 2.724355593 seconds,
サーバのまたぎ回数: 5

default
total execution time: 0.577433061 seconds
サーバのまたぎ回数: 5

total execution time: 0.483004510 seconds
サーバのまたぎ回数: 5

total execution time: 0.494555179 seconds
サーバのまたぎ回数: 5

total execution time: 0.434693161 seconds
サーバのまたぎ回数: 5

total execution time: 0.611061960 seconds
サーバのまたぎ回数: 5

total execution time: 0.485163044 seconds
サーバのまたぎ回数: 5
"""

import matplotlib.pyplot as plt

# Data
categories = [
    "default",
    "every-time",
]
execution_times = [
    (0.577433061 + 0.483004510 + 0.494555179 + 0.434693161 + 0.611061960 + 0.485163044)
    / 6,
    2.724355593,
]
colors = ["grey", "green"]

# Bar Graph
x = range(len(categories))

fig, ax1 = plt.subplots(figsize=(8, 5))

# Bar for Execution Time
ax1.bar(x, execution_times, color=colors, alpha=0.7, label="Execution Time (seconds)")
ax1.set_ylabel("100RW Execution Time (seconds)")
ax1.tick_params(axis="y")
ax1.set_xticks(x)
ax1.set_xticklabels(categories)
ax1.set_xlabel("Category")
ax1.legend(loc="upper left")

# Line Graph for Server Crossings
# ax2 = ax1.twinx()
# ax2.plot(x, server_crossings, color='red', marker='o', label='Server Crossings')
# ax2.set_ylabel('Server Crossings', color='red')
# ax2.tick_params(axis='y', labelcolor='red')
# ax2.legend(loc='upper right')

plt.title("Execution Time and Server Crossings by Category")
plt.tight_layout()
plt.savefig("basic.png")
plt.show()
