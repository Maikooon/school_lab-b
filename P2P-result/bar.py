import matplotlib.pyplot as plt
import numpy as np

# データ設定
labels = ["First", "Second", "Third"]  # 各データセットに対応するラベル
average_times = [24.451633405685424, 26.420499999999997, 25.1554]
average_access_times = [0, 0.140183, 0.20345066666666667]
average_token_generate_times = [0, 0.087248, 0.06780466666666667]
average_token_verify_times = [0, 0.04991525, 0.021789]

# グラフのバー設定
x = np.arange(len(labels))  # バーの位置
width = 0.5  # バーの幅

# スタックバーグラフのプロット
fig, ax = plt.subplots()
ax.bar(x, average_times, width, label="Total Average Time")
ax.bar(
    x, average_access_times, width, bottom=average_times, label="Average Access Time"
)
ax.bar(
    x,
    average_token_generate_times,
    width,
    bottom=np.array(average_times) + np.array(average_access_times),
    label="Average Token Generate Time",
)
ax.bar(
    x,
    average_token_verify_times,
    width,
    bottom=np.array(average_times)
    + np.array(average_access_times)
    + np.array(average_token_generate_times),
    label="Average Token Verify Time",
)

# ラベルとタイトルの追加
ax.set_xlabel("Data Set")
ax.set_ylabel("Time (seconds)")
ax.set_title("Average Time Distribution")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

plt.show()
