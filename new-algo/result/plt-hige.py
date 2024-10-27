import matplotlib.pyplot as plt

# ファイル名
# file1 = "./karate/default.txt"  # 最初のファイル
# file2 = "./karate/access.txt"  # 2番目のファイル
GRAPH = "METIS-fb-pages"
file1 = f"./{GRAPH}/default.txt"
file2 = f"./{GRAPH}/access.txt"
file3 = f"./{GRAPH}/group-access.txt"


# ファイルからデータを読み込む
def read_execution_times(filename):
    count = 0
    execution_times = []
    with open(filename, "r") as file:
        for line in file:
            if "Average path length" in line:
                average_count = float(line.split()[-1])
                count += average_count
            if "Program execution time" in line:
                time_in_ns = int(line.split()[-2])  # ナノ秒を取得
                time_in_ms = time_in_ns / 1e6  # ミリ秒に変換
                execution_times.append(time_in_ms)
    average_count = count / len(execution_times)
    print(average_count)
    print(execution_times)
    return average_count, execution_times


# 補正を行う
def correct_execution_times(count1, count2, count3, time1, time2, time3):
    # どのぐらい補正を行うのかを決める
    print(count1)
    print(count2)
    print(count3)
    alpha2 = 1
    alpha3 = count1 / count3

    print(f"alpha2: {alpha2}")
    print(f"alpha3: {alpha3}")

    time2 = [t * alpha2 for t in time2]
    time3 = [t * alpha3 for t in time3]

    print(time2)
    print(time3)

    # 増加分が元に対して何％なのかを調べる
    average1 = sum(time1) / len(time1)
    average2 = sum(time2) / len(time2)
    average3 = sum(time3) / len(time3)
    diff12 = (average2 - average1) / average1
    diff13 = (average3 - average1) / average1

    # print(f"diff12: {diff12}")
    # print(f"diff13: {diff13}")
    # 小数第三桁で丸める
    diff12 = round(diff12 * 100, 2)
    diff13 = round(diff13 * 100, 2)
    return time2, time3, diff12, diff13


if __name__ == "__main__":
    # 実行時間のリスト
    count1, time1 = read_execution_times(file1)
    count2, time2 = read_execution_times(file2)
    count3, time3 = read_execution_times(file3)

    time2, time3, diff12, diff13 = correct_execution_times(
        count1, count2, count3, time1, time2, time3
    )
    print(time2, time3)

    # 箱ひげ図を描く
    plt.figure(figsize=(10, 6))
    plt.boxplot(
        [time1, time2, time3],
        labels=["non-access-limit", "access", "grouped access"],
    )

    # グラフのタイトルやラベル
    plt.title(f"Comparison of RW Execution Times {GRAPH}")
    plt.ylabel("Execution Time (ms)")
    plt.grid(True)
    plt.text(
        0.9,
        0.9,
        f"access:{diff12}%up, grouped-access:{diff13}%up",
        ha="center",
        transform=plt.gca().transAxes,
    )
    plt.savefig(f"./{GRAPH}/hige.png")
    # グラフを表示
    plt.show()
