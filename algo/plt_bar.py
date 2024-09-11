"""
既存のファイルを指定すると、グラフごと、手法を比較する棒グラフを得ることができます

比較したい手法の結果のファイルを選択することで、すべてのグラフ取得可能
"""

import matplotlib.pyplot as plt
import re


def extract_data_from_file(file_path):
    folder_data = {}
    try:
        with open(file_path, "r") as file:
            content = file.read()
            folders = re.findall(r"Folder: ([\w\-]+)", content)
            times = re.findall(r"Execution time: (\d+)", content)

            for folder, time in zip(folders, times):
                folder_data[folder] = float(time)
    except FileNotFoundError:
        print(f"ファイルを開けません: {file_path}")
    # print(folder_data)
    print(folder_data)
    return folder_data


def plot_execution_times(data1, data2, data3, data4):
    # 要素の数分だけ図表を作成する
    count = len(data1)
    # 　これですべてのグラフ名の取得ができる
    keys = list(data1.keys())
    for i in range(count):
        times1 = data1.get(keys[i], 0)
        times2 = data2.get(keys[i], 0)
        times3 = data3.get(keys[i], 0)
        times4 = data4.get(keys[i], 0)
        # times2 = data2[keys[i]]
        # times3 = data3[keys[i]]
        # times4 = data4[keys[i]]
        graph_name = [keys[i]]
        fig, ax = plt.subplots()

        # 棒グラフの描画
        fig, ax = plt.subplots()
        ax.bar(
            [
                "default(no jwt)",
                "token with Rwer",
                "cache used list",
                "cache used hash",
            ],
            [
                times1,
                times2,
                times3,
                times4,
            ],
            color=["blue", "orange", "grey", "green"],
        )

        # グラフのタイトルと軸ラベルを設定
        ax.set_title(graph_name)
        ax.set_ylabel("Execution Time")

        # グラフを表示
        # plt.show()
        plt.savefig(f"./cache/bar-plt/list vs hash/{keys[i]}.png")


# 　ここで読み込むファイルを設定する
def main():
    file1_path = "./certification/construction/nojwt-result/nojwt-result-0.15/overall_average_results copy.txt"
    file2_path = "./certification/construction/all-jwt-result/jwt-result-new-community/overall_average_results.txt"
    file3_path = "./cache/bar-plt/list.txt"
    file4_path = "./cache/bar-plt/hash.txt"

    data1 = extract_data_from_file(file1_path)
    data2 = extract_data_from_file(file2_path)
    data3 = extract_data_from_file(file3_path)
    data4 = extract_data_from_file(file4_path)

    plot_execution_times(data1, data2, data3, data4)


if __name__ == "__main__":
    main()
