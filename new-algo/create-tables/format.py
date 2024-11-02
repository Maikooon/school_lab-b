"""
実行してできたのファイルにおい、いらない文字列を削除するプログラムを生成する
dynamic.community

"""

# データの読み込み


# Community という文字列があったら
# そこのCommunity番号を取得
# その次の行からGroupという文字列があるので、Groupを削除したのちに、Comumuinity番号：Group番号　その後；；；という形にする

GRAPH = "fb-pages-company"


def process_community_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    result = []

    current_community = None

    for line in lines:
        stripped_line = line.strip()

        # Communityという文字列があったら
        if "Community" in stripped_line:
            # Community番号を取得
            current_community = stripped_line.split()[1][:-1]  # 'Community 0:' -> '0'
        elif "Group" in stripped_line and current_community is not None:
            # Groupという文字列があったら
            group_number = stripped_line.split()[1][:-1]  # 'Group 1:' -> '1'
            # ノードのリストを取得
            nodes = stripped_line.split(":")[1].strip()  # '9, 28, ...'の部分
            # フォーマットを作成
            result.append(f"{current_community} {group_number} {nodes}")

    # # 結果をファイルに保存
    output_filename = f"./result/{GRAPH}/dynamic_groups.txt"
    with open(output_filename, "w") as output_file:
        output_file.write("\n".join(result))

    # 結果を出力
    return "\n".join(result)


# nng_nodesの書き方を修正する
def process_ng_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    result = []

    current_community = None

    for line in lines:
        stripped_line = line.strip()

        # Communityという文字列があったら
        if "コミュニティ" in stripped_line:
            # Community番号を取得
            current_community = stripped_line.split()[1][:-1]  # 'Community 0:' -> '0'
        elif "NG for Group" in stripped_line and current_community is not None:
            # Groupという文字列があったら
            group_number = stripped_line.split()[3][:-1]  # 'Group 1:' -> '1'
            # ノードのリストを取得
            nodes = stripped_line.split(":")[1].strip()  # '9, 28, ...'の部分
            # フォーマットを作成
            result.append(f"{current_community} {group_number} {nodes}")

    # # 結果をファイルに保存
    output_filename = f"./result/{GRAPH}/ng_nodes.txt"
    with open(output_filename, "w") as output_file:
        output_file.write("\n".join(result))

    # 結果を出力
    return "\n".join(result)


# 使用例
filename1 = f"./result/{GRAPH}/dynamic_groups.txt"
result_string = process_community_file(filename1)

filename2 = f"./result/{GRAPH}/ng_nodes.txt"
result_string = process_ng_file(filename2)

print(result_string)
