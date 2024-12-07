import matplotlib.pyplot as plt


def read_data(file_path):
    x_list = []
    y_list = []
    # ファイルを開いてデータをリストに格納
    with open(file_path, "r") as file:
        for line in file:
            if "サーバのまたぎ回数" in line:
                x = int(line.split(":")[1])
                x_list.append(x)
            if "total execution time" in line:
                y = float(line.split(":")[1].split(" ")[1])
                y_list.append(y)
    return x_list, y_list


# 各データセットの読み込み
data_files = {
    # "default": "./default/1-log.txt",
    # "every-time": "./every-time/1-log.txt",
    # "first-time": "./first-time/1-log.txt",
    "default": "./default/100-log.txt",
    "first-time": "./first-time/100-log.txt",
    "parent-token": "./parent-token/100-log.txt",
}

colors = [
    "red",
    "green",
    "purple",
]
plt.figure(figsize=(8, 6))
# ux軸の範囲を決めたい
# plt.xlim(10, 380)

# 各データセットをプロット
for label, (color, file_path) in zip(
    data_files.keys(), zip(colors, data_files.values())
):
    x_list, y_list = read_data(file_path)
    ## ここまで100回分の平均であるので、すべてを/100して考える
    x_list = [x / 100 for x in x_list]
    y_list = [y / 100 for y in y_list]
    plt.scatter(x_list, y_list, label=label, color=color)

# 軸ラベルと凡例を設定
plt.xlabel("server across time (times)")
plt.ylabel("total execution time (s)")
plt.legend()
plt.grid(True)

# グラフを保存および表示
plt.savefig("[100-time]comparison_plot-2.png")
plt.show()
