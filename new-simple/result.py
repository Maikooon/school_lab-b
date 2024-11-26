import matplotlib.pyplot as plt
import numpy as np


x_list = []
y_list = []
# データをリストに格納
file = open("./first-time/log.txt", "r")
# 一行づつ読み込んんで、x、yに入れる,空行が車で続ける


for line in file:
    if "サーバのまたぎ回数" in line:
        x = int(line.split(":")[1])
        x_list.append(x)
    if "total execution time" in line:
        y = float(line.split(":")[1].split(" ")[1])
        y_list.append(y)
file.close()

# 散布図を描画
plt.scatter(x_list, y_list)

# 軸ラベルを設定
plt.xlabel("サーバのまたぎ回数")
plt.ylabel("total execution time (秒)")

# グラフを表示
plt.savefig("result-evenry.png")
plt.show()
