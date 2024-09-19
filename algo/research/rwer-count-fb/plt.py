import re
import matplotlib.pyplot as plt


# ファイルの読み込みを行う
def read_file(path):
    with open("./" + path + "/overall_average_results.txt", "r") as f:
        data = f.read()
    node = 762

    folders = re.findall(r"Folder: (.+)", data)
    moves = re.findall(r"Total moves across communities: (\d+)", data)
    execution_time = re.findall(r"Execution time: (\d+)", data)

    for i in range(len(moves)):
        moves[i] = int(moves[i]) / node
        execution_time[i] = int(execution_time[i]) / node
    print(moves)
    print(execution_time)
    return folders, moves, execution_time


way1, x1, y1 = read_file("every")
way2, x2, y2 = read_file("once")


# グラフの出力
plt.scatter(x1, y1, label=way1)
plt.scatter(x2, y2, label=way2)
# plt.show()
plt.savefig("every.png")
# # 　ファイルへの書き込みを行う
# with open("./every.txt", "w") as f:
#     for graph, move_count, time in zip(folders, moves, execution_time):
#         f.write(f"Folder: {graph}\n")
#         f.write(f"Total moves across communities: {move_count}\n")
#         f.write(f"Execution time: {time}\n")
#         f.write("\n")
