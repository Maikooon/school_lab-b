"""
グループになっていないNGリストを作成するプログラム

コミュニティ 1:
    NG for Group 1:
    NG for Group 2:
    最低限グループ名だけはエラーになるので足すこと
これ終わったら数字の羅列にすること

また、できたファイルにおいて、[]を取り除くこと
"""

import glob
import os

# 　ここはファイルの情報のみでおk
GRAPH = os.getenv("GRAPH", "")
print(GRAPH)


def read_community_file(filename):
    community_groups = {}
    with open(filename, "r") as file:
        lines = file.readlines()
        current_community = None

        for line in lines:
            line = line.strip()
            if line.startswith("Community"):
                # 新しいコミュニティを開始
                current_community = line.split()[1]
                community_groups[current_community] = {}
            elif line.startswith("Group"):
                # グループの行から数字を抽出
                group_number = line.split(":")[0].split()[1]
                numbers = line.split(":")[-1].strip()
                # 数字をセットに追加
                print(current_community)
                print(group_number)
                community_groups[current_community][group_number] = set(
                    map(int, numbers.split(","))
                )
    # print("community_groups:", community_groups)  # デバッグ用の出力
    return community_groups


def read_ng_info(filename):
    ng_info = {}
    with open(filename, "r") as file:
        lines = file.readlines()
        # print(lines)
        current_community = None

        for line in lines:
            line = line.strip()
            if line.startswith("コミュニティ"):
                current_community = line.split()[1].strip(":")  # コミュニティ番号を取得
                ng_info[current_community] = {}  # 新しいコミュニティ用の辞書を初期化
            elif line.startswith("NG for"):
                group_number = line.split()[3]  # "Group"の後の数字を取得
                ng_values = line.split(":")[-1].strip()  # カンマ区切りの文字列を取得

                # 空の項目を無視して、カンマ区切りの文字列を整数のリストに変換
                ng_value_list = [
                    int(x.strip()) for x in ng_values.split(",") if x.strip()
                ]

                group_number = group_number.split(":")[0]

                # 辞書にリストを格納
                ng_info[current_community][group_number] = ng_value_list

    # print("ng_info:", ng_info)  # デバッグ用の出力
    return ng_info


# 読み込むデータファイルのパターンを指定（例：server_*.txt）
# The line `# data_file_pattern = f"./result/{GRAPH}/node_community.txt"` is a commented-out line in
# the code. It is used to define a pattern for the data file that the program should read. The
# `f-string` is used to dynamically insert the value of the `GRAPH` variable into the file path.
data_file_pattern = f"./result/{GRAPH}/node_community.txt"
# TODO: Loucainのときはここを変更
# data_file_pattern = f"./../../Louvain/community/{GRAPH}.cm"
# 　ここにコミュニティ情報を入れる
data = []
# コミュニティファイルからコミュニティとグループの情報を取得
community_groups = read_community_file(f"./result/{GRAPH}/dynamic_groups.txt")
# NG情報を取得
ng_info = read_ng_info(f"./result/{GRAPH}/ng_nodes.txt")


# 複数のデータファイルを読み込む
print("data_file_pattern:", data_file_pattern)
for filename in glob.glob(data_file_pattern):
    with open(filename, "r") as file:
        print("filename:", filename)
        for line in file:
            # 各行を分割してタプルに変換
            parts = line.split()
            # 数字を整数に変換してタプルに追加
            data.append((int(parts[0]), int(parts[1])))

# 各コミュニティとグループごとに結果をフィルタリング
# print(community_groups)
for community, groups in community_groups.items():
    # print(f"コミュニティ {community}")
    # print("groups:", groups)
    for group_number, target_values in groups.items():
        group_number = int(group_number)
        # target-valuesは元々のコミュニティの番号
        print(
            f"  Group {group_number}: {target_values}　元々コミュニティ{target_values}に属する"
        )
        # 右側が対象の数字であるペアの左側の数字を抽出
        # 多分ここのResukltの部分がうまくいっていない
        # データが取れていない
        # print("ここででデータ", data)
        result = [left for left, right in data if right in target_values]
        # NG情報を取得

        community = str(community)[0]
        ng_value_2 = ng_info.get(str(community), {}).get(
            str(group_number), 0
        )  # NG値を取得

        print(f"  NG for Group {group_number}: {ng_value_2}, Result: {result}")

        print(ng_value_2)
        if ng_value_2 is not []:
            for node in ng_value_2:
                print(node)
                print(result)
        else:
            print("skip")

        with open(f"./result/{GRAPH}/non-group-ng-nodes.txt", "a") as file:
            for node in ng_value_2:
                file.write(f"{node}:{result}\n")
            # file.write(f"{ng_value_2}:{result}\n")
