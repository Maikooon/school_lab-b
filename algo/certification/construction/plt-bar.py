import matplotlib.pyplot as plt

# データの設定
labels = ['not signed', 'signed']
values = [18192, 33553]

# カラーマッピングの設定
colors_map = ['Grey', 'orange', 'green'] 

# グラフの描画
fig, ax = plt.subplots()

# 左側の棒グラフ
ax.bar(labels[0], values[0], color=colors_map[0])

# 右側の棒グラフ
ax.bar(labels[1], values[0], color=colors_map[0], label='default')
ax.bar(labels[1], values[1] - 18192, bottom=18192, color=colors_map[1], label='token generate')
ax.bar(labels[1], values[1] - 19424, bottom=19424, color=colors_map[2], label='token verify') 

# 縦軸と横軸のラベル
ax.set_ylabel('Execution Time (msec)')
ax.set_xlabel('')
ax.set_ylim(15000,35000)

# 凡例の追加
ax.legend()

# グラフのタイトル
plt.title('Execution Time Comparison')


plt.savefig('./figure/time-detail.png')
# グラフの表示
plt.show()
