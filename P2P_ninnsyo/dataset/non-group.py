'''
コミュニティ 1:
  NG for Group 1:
  NG for Group 2:
  最低限グループ名だけはエラーになるので足すことll


'''
import glob
import os

GRAPH = "fb-pages-company"


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
                community_groups[current_community][group_number] = set(
                    map(int, numbers.split(","))
                )

    return community_groups


def read_ng_info(filename):
    ng_info = {}
    with open(filename, "r") as file:
        lines = file.readlines()
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
data_file_pattern = f"./{GRAPH}/server_*.txt"
data = []

# コミュニティファイルからコミュニティとグループの情報を取得
community_groups = read_community_file(f"./{GRAPH}/all_dynamic_groups.txt")
# NG情報を取得
ng_info = read_ng_info(f"./{GRAPH}/ng_nodes.txt")
# print("NG情報:", ng_info)
# 複数のデータファイルを読み込む
for filename in glob.glob(data_file_pattern):
    with open(filename, "r") as file:
        for line in file:
            # 各行を分割してタプルに変換
            parts = line.split()
            # 数字を整数に変換してタプルに追加
            data.append((int(parts[0]), int(parts[1])))

# 各コミュニティとグループごとに結果をフィルタリング
for community, groups in community_groups.items():
    # print(f"コミュニティ {community}")
    # print("groups:", groups)
    for group_number, target_values in groups.items():
        group_number = int(group_number)
        # 右側が対象の数字であるペアの左側の数字を抽出
        result = [left for left, right in data if right in target_values]
        # NG情報を取得

        community = str(community)[0]
        ng_value_2 = ng_info.get(str(community), {}).get(
            str(group_number), 0
        )  # NG値を取得

        # print(f"  NG for Group {group_number}: {ng_value_2}, Result: {result}")

        print(ng_value_2)
        if ng_value_2 is not []:
            for node in ng_value_2:
                print(node)
                print(result)
        else:
        print("skip")

        with open(f"./{GRAPH}/non_group-ng_nodes.txt", "a") as file:
            for node in ng_value_2:
                file.write(f"{node}:{result}\n")
            # file.write(f"{ng_value_2}:{result}\n")
