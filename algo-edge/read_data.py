"""
  渡すもの；
    入力するファイル名
    Start - node
    Now_node
"""

# now_nodeとして検索したいノード番号を指定
now_node = int(input("探したいnow_nodeの数字を入力してください: "))
start_node = int(input("探したいstart_nodeの数字を入力してください: "))

# テーブルのデータを含むファイルを読み込む
file_path = "./allow-table/cmu.txt"  # データが入ったファイルを指定
allow_table = []


def read_file_lines(file_path):
    with open(file_path, "r") as file:
        return file.readlines()


# ファイルから行を3行ごとに解析し、now_nodeに一致する列を探す関数
def search_now_node_is_allowed(file_path, now_node, start_node):
    with open(file_path, "r") as file:
        lines = file.readlines()

    # 3行ごとに処理するためにループ
    for i in range(0, len(lines), 3):
        column_line = lines[i].strip()

        # ":" を除いた部分をリスト化し、整数に変換して列番号を取得
        columns = list(map(int, column_line.replace(":", "").split()))

        # now_nodeが列番号の中に含まれているか確認
        if now_node in columns:
            # 左側か右側かを判定
            if columns.index(now_node) == 0:
                data_row = lines[i + 1].strip()
                opposite_node = columns[1]
            else:
                data_row = lines[i + 2].strip()
                opposite_node = columns[0]

            # データ行から数字の部分をリストに変換
            row_values = list(map(int, data_row.split()[1:]))

            # 参照した行の値を表示
            # print(f"参照した行の値: {columns.index(now_node)}行を参照 {row_values}")

            """
            row - Values には、許可されているノードが格納されている
            ここで、始点によりアクセスを制限したいので、始点ノードがここに含まれているのかを確認する
            """

            if start_node in row_values:
                # print(
                #     f"start_node {start_node} が許可されているノードに含まれています。"
                # )
                # 　自分の始点が許可されていたら、エッジの連携先のNodeを取得する
                allow_table.append(opposite_node)
            # else:
            # print(
            #     f"start_node {start_node} が許可されているノードに含まれていません。"
            # )

    # この中から次の遷移先を決定する
    print(allow_table)
    return allow_table


search_now_node_is_allowed(file_path, now_node, start_node)
