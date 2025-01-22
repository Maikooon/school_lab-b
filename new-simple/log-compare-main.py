import matplotlib.pyplot as plt


def read_data(file_path):
    x_list = []
    y_list = []
    # ファイルを開いてデータをリストに格納
    with open(file_path, "r") as file:
        for line in file:
            if "サーバのまたぎ回数" in line:
                x = float(line.split(":")[1])
                x_list.append(x)
            if "total execution time" in line:
                y = float(line.split(":")[1].split(" ")[1])
                y_list.append(y)
    return x_list, y_list


def calculate_speedup(baseline_y_list, comparison_y_list):
    speedups = [
        (baseline - comparison) / baseline * 100
        for baseline, comparison in zip(baseline_y_list, comparison_y_list)
    ]
    return speedups


# 各データセットの読み込み
data_files = {
    "no authentication(method-a)": "./default/100-log.txt",
    "every time authentication(method-b)": "./every-time/1-log.txt",
    "proposal-α": "./first-time/100-log.txt",
    "proposal-β": "./parent-token/100-log.txt",
}

colors = ["grey", "purple", "blue", "red"]

plt.figure(figsize=(8, 6))

# 「every time authentication(method-d)」のデータを基準にして、他の手法の高速化を計算
baseline_x_list, baseline_y_list = read_data(
    data_files["every time authentication(method-b)"]
)

# 各データセットをプロット
for label, (color, file_path) in zip(
    data_files.keys(), zip(colors, data_files.values())
):
    x_list, y_list = read_data(file_path)

    # 100回分の平均
    if label != "every time authentication(method-b)":
        x_list = [x / 100 for x in x_list]
        y_list = [y / 100 for y in y_list]
    # 全てのデータにおいて、10000回にするために以下の数字を足す。少し長いかもだが手法の有用性はわかる
    # x_list = [x + 0.6101654625555555 for x in x_list]
    y_list = [y + 0.8101654625555555 for y in y_list]

    # 高速化を計算
    if label != "every time authentication(method-b)":
        speedups = calculate_speedup(baseline_y_list, y_list)
        print(f"{label} の高速化率（％）: {speedups[-1]:.2f}%")  # 最後の値を表示

    # 散布図としてプロット
    plt.scatter(x_list, y_list, label=label, color=color)

# 軸のスケールを設定
plt.xlim(1.5, 4.2)  # x軸の範囲を設定
plt.yscale("log")  # y軸を指数スケールに変更

# 軸ラベルと凡例を設定
plt.xlabel("server across count")
plt.ylabel("total execution time (seconds) (log scale)")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# グラフを保存および表示
plt.savefig("[100-time]comparison_plot_loglog.pdf")
plt.show()
