# import matplotlib.pyplot as plt

# # ファイル名
# # 　ここに指定したファイル分だけの図を出力したい。つまりここに配列でしたい
# GRAPH = ["fb-cal", "fb-pages", "karate", "my-ca", "my-fb-cal", "my-karate"]

# file1 = f"./logs/{GRAPH}/log.txt"


# # ファイルからデータを読み込む
# def read_execution_times(filename):
#     default_time = []
#     every_time = []
#     one_time = []
#     # 移動回数との相関関係を考える
#     move_server_count = []
#     with open(filename, "r") as file:
#         current_section = None
#         for line in file:
#             if "default" in line:
#                 current_section = "default"
#             elif "everyTime" in line:
#                 current_section = "every_time"
#             elif "oneTime" in line:
#                 current_section = "one_time"
#             elif (
#                 "Execution time:" in line
#                 or "Total Execution Time:" in line
#                 or "Elapsed time: " in line
#             ):
#                 # 最後の要素が "seconds" の場合、数値部分のみを取得
#                 time_str = (
#                     line.split()[-2]
#                     if line.split()[-1] == "seconds"
#                     else line.split()[-1]
#                 )
#                 time = float(time_str)  # 数値部分を整数に変換
#                 if current_section == "default":
#                     default_time.append(time)
#                 elif current_section == "every_time":
#                     every_time.append(time)
#                 elif current_section == "one_time":
#                     one_time.append(time)
#     return default_time, every_time, one_time


# def read_move_server_count(filename):
#     move_server_count = []
#     with open(filename, "r") as file:
#         for line in file:
#             if "Move Server Count:" in line:
#                 count = int(line.split()[-2])
#                 move_server_count.append(count)
#     print(move_server_count)
#     return move_server_count


# if __name__ == "__main__":
#     ave_move_server_count = 0
#     # 実行時間のリスト
#     default, every_time, one_time = read_execution_times(file1)
#     move_server_count = read_move_server_count(file1)
#     print("Default:", default)
#     print("Every Time:", every_time)
#     print("One Time:", one_time)
#     print("Move Server Count:", move_server_count)
#     print(len(move_server_count))
#     print(sum(move_server_count))
#     move_server_count = sum(move_server_count) / len(move_server_count)
#     print("Move Server Count:", move_server_count)
#     ave_move_server_count = move_server_count / 100
#     print("Average Move Server Count:", ave_move_server_count)

#     # ここで平均増加率を計算する
#     ave_default = sum(default) / len(default)
#     ave_every_time = sum(every_time) / len(every_time)
#     ave_one_time = sum(one_time) / len(one_time)
#     diff12 = (ave_every_time - ave_default) / ave_default
#     diff13 = (ave_one_time - ave_default) / ave_default
#     # 割合になるように変換しておく
#     diff12 = round(diff12 * 100, 2)
#     diff13 = round(diff13 * 100, 2)

#     # 箱ひげ図を描く
#     plt.figure(figsize=(10, 6))
#     plt.boxplot(
#         [default, every_time, one_time],
#         labels=["default", "every_time", "one_time"],
#     )
#     plt.text(
#         0.9,
#         0.9,
#         f"every time:{diff12}%up, one time:{diff13}%up",
#         ha="center",
#         transform=plt.gca().transAxes,
#     )

#     # グラフのタイトルやラベル
#     plt.title(
#         f"Comparison of RW Execution Times {GRAPH} --Move server count:{ave_move_server_count}"
#     )
#     plt.ylabel("Execution Time (s)")
#     plt.grid(True)

#     # グラフを保存
#     plt.savefig(f"./logs/{GRAPH}/all.png")
#     plt.show()
# #
import matplotlib.pyplot as plt

# グラフ名のリスト
GRAPH = ["fb-cal", "fb-pages", "karate", "my-ca", "my-fb-cal", "my-karate"]


# ファイルから実行時間を読み込む関数
def read_execution_times(filename):
    default_time = []
    every_time = []
    one_time = []
    with open(filename, "r") as file:
        current_section = None
        for line in file:
            if "default" in line:
                current_section = "default"
            elif "everyTime" in line:
                current_section = "every_time"
            elif "oneTime" in line:
                current_section = "one_time"
            elif (
                "Execution time:" in line
                or "Total Execution Time:" in line
                or "Elapsed time: " in line
            ):
                time_str = (
                    line.split()[-2]
                    if line.split()[-1] == "seconds"
                    else line.split()[-1]
                )
                time = float(time_str)
                if current_section == "default":
                    default_time.append(time)
                elif current_section == "every_time":
                    every_time.append(time)
                elif current_section == "one_time":
                    one_time.append(time)
    return default_time, every_time, one_time


# ファイルから移動回数を読み込む関数
def read_move_server_count(filename):
    move_server_count = []
    with open(filename, "r") as file:
        for line in file:
            if "Move Server Count:" in line:
                count = int(line.split()[-2])
                move_server_count.append(count)
    return move_server_count


# メイン処理
if __name__ == "__main__":
    for graph in GRAPH:
        filename = f"./logs/{graph}/log.txt"

        # 実行時間と移動回数を読み込む
        default, every_time, one_time = read_execution_times(filename)
        move_server_count = read_move_server_count(filename)

        # 移動回数の平均を計算
        if move_server_count:
            ave_move_server_count = (
                sum(move_server_count) / len(move_server_count) / 100
            )
        else:
            ave_move_server_count = 0

        # 実行時間の平均と増加率を計算
        ave_default = sum(default) / len(default) if default else 0
        ave_every_time = sum(every_time) / len(every_time) if every_time else 0
        ave_one_time = sum(one_time) / len(one_time) if one_time else 0

        diff12 = (
            (ave_every_time - ave_default) / ave_default * 100 if ave_default else 0
        )
        diff13 = (ave_one_time - ave_default) / ave_default * 100 if ave_default else 0

        # ボックスプロットを作成
        plt.figure(figsize=(10, 6))
        plt.boxplot(
            [default, every_time, one_time],
            labels=["default", "every_time", "one_time"],
        )
        plt.text(
            0.9,
            0.9,
            f"every time: {diff12:.2f}% up, one time: {diff13:.2f}% up",
            ha="center",
            transform=plt.gca().transAxes,
        )

        # グラフのタイトルとラベル
        plt.title(
            f"Comparison of RW Execution Times for {graph} -- Move server count: {ave_move_server_count:.2f}"
        )
        plt.ylabel("Execution Time (s)")
        plt.grid(True)

        # グラフの保存
        plt.savefig(f"./logs/{graph}/all.png")
        plt.show()
