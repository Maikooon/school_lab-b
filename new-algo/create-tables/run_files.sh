#!/bin/bash

### このファイルの実行前に以下のファイルのグラフ名を変えておくこと
# 実行すれば、すべてのNGファイルが生成される
# []を消すのを忘れずに


# 変数をエクスポート
export GRAPH="ng_0.05/METIS-com-amazon-connected/200"  # グラフを格納するファイルの名前
export GRAPH_NAME="com-amazon-connected"  # 正規のグラフの名前
export GRAPH_COMMUNITY="ng_0.05/METIS-com-amazon-connected"  # NGノードを含むグラフの名前
export NG_RATE=0.05  # NGノードの割合
export COM_NUM=200

# 1. 各Pythonスクリプトを実行する
# dynamic とngが生成される
python create-table.py


# 2. file1 の特定の文字列削除と整形
# ここからは自分で行う
# python create-non-group-table.py
python format.py
# format.pyの実行でdynamic_groupsの整形は完了

echo "Processing complete."
