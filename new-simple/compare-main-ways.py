"""
認証の基礎評価を得るためのグラフ
毎回認証したとき及び親TOkenを導入したときのグラフを描画

ここを変更することにより異なるグラフが書ける
初めの３つ
・デフォルトの時との比較

次の３つ
・親Tokenを導入した時の比較

"""

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


# 各データセットの読み込み

data_files = {
    "default(method-c)": "./default/1-log.txt",
    "every-time(method-d)": "./every-time/1-log.txt",
    "proposal-α": "./first-time/1-log.txt",
    # "default(method-c)": "./default/100-log.txt",
    # "proposal-α": "./first-time/100-log.txt",
    # "proposal-β": "./parent-token/100-log.txt",
}

colors = [
    "red",
    # "green",
    "purple",
    "blue",
]
plt.figure(figsize=(8, 6))
# ux軸の範囲を決めたい
# plt.xlim(10, 380)

# 各データセットをプロット
for label, (color, file_path) in zip(
    data_files.keys(), zip(colors, data_files.values())
):
    x_list, y_list = read_data(file_path)
    ##TODO: ここまで100回分の平均であるので、すべてを/100して考える
    # x_list = [x / 100 for x in x_list]
    # y_list = [y / 100 for y in y_list]
    y_list = [y + 0.8101654625555555 for y in y_list]
    plt.scatter(x_list, y_list, label=label, color=color)

# 軸ラベルと凡例を設定
plt.xlabel("server across time")
plt.ylabel("total execution time (seconds)")
plt.legend()
plt.grid(True)

# グラフを保存および表示
plt.savefig("[100-time]comparison_plot-2.png")
plt.show()
