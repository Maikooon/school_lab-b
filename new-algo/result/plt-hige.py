import matplotlib.pyplot as plt

# ファイル名
# file1 = "./karate/default.txt"  # 最初のファイル
# file2 = "./karate/access.txt"  # 2番目のファイル
file1 = "./fb-caltech-connected/default.txt"
file2 = "./fb-caltech-connected/access.txt"  # 2番目のファイル


# ファイルからデータを読み込む
def read_execution_times(filename):
    execution_times = []
    with open(filename, "r") as file:
        for line in file:
            if "Program execution time:" in line:
                time_in_ns = int(line.split()[-2])  # ナノ秒を取得
                time_in_ms = time_in_ns / 1e6  # ミリ秒に変換
                execution_times.append(time_in_ms)
    return execution_times


if __name__ == "__main__":
    # 実行時間のリスト
    execution_times_1 = read_execution_times(file1)
    execution_times_2 = read_execution_times(file2)

    # 箱ひげ図を描く
    plt.figure(figsize=(10, 6))
    plt.boxplot([execution_times_1, execution_times_2], labels=["default", "access"])

    # グラフのタイトルやラベル
    plt.title("Comparison of Program Execution Times")
    plt.ylabel("Execution Time (ms)")
    plt.grid(True)
    plt.savefig("./fb-caltech-connected/fb-caltech-connected.png")
    # グラフを表示
    plt.show()
