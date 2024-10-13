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
        print(folders[i])
        moves[i] = int(moves[i]) / node
        execution_time[i] = int(execution_time[i]) / node
    return folders, path, moves, execution_time


way1, path1, x1, y1 = read_file("every")
way2, path2, x2, y2 = read_file("once")
# way3, path3, x3, y3 = read_file("every+token")


# グラフの出力
plt.scatter(x1, y1, label=path1, color="blue")
plt.scatter(x2, y2, label=path2, color="orange")
# plt.scatter(x3, y3, label=path3, color="green")
plt.xlabel("Average moves count per Rwer")
plt.ylabel("Average execution time per Rwer")
plt.legend()


# plt.show()
plt.savefig("12.png")
