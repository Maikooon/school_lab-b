"""
分散での実行時間を比較する箱ひげ図をかく

"""

import matplotlib.pyplot as plt

# ファイル名
# file1 = "./karate/default.txt"  # 最初のファイル
# file2 = "./karate/access.txt"  # 2番目のファイル
GRAPH = "fb"
file1 = f"./{GRAPH}/default.txt"
file2 = f"./{GRAPH}/access.txt"
file3 = f"./{GRAPH}/group-access.txt"


# ファイルからデータを読み込む
def read_execution_times(filename):
    count = 0
    execution_times = []
    with open(filename, "r") as file:
        for line in file:
            # if "Average path length" in line:
            #     average_count = float(line.split()[-1])
            #     count += average_count
            if "Elapsed time " in line:
                time_in = float(line.split()[-1])  # 秒を取得
                execution_times.append(time_in)
    # average_count = count / len(execution_times)
    return count, execution_times


if __name__ == "__main__":
    # 実行時間のリスト
    count1, time1 = read_execution_times(file1)
    count2, time2 = read_execution_times(file2)
    count3, time3 = read_execution_times(file3)

    # time2, time3, diff12, diff13 = correct_execution_times(
    #     count1, count2, count3, time1, time2, time3
    # )
    print(time2, time3)

    # # 箱ひげ図を描く
    plt.figure(figsize=(10, 7))
    plt.boxplot(
        [time1, time2, time3],
        labels=["non-access-limit", "access", "grouped access"],
    )

    # グラフのタイトルやラベル
    plt.title(f"Comparison of RW Execution Times {GRAPH}")
    plt.ylabel("Execution Time (ms)")
    plt.grid(True)
    # plt.text(
    #     0.9,
    #     0.9,
    #     f"access:{diff12}%up, grouped-access:{diff13}%up",
    #     ha="center",
    #     transform=plt.gca().transAxes,
    # )
    plt.savefig(f"./{GRAPH}/hige.png")
    # グラフを表示
    plt.show()
