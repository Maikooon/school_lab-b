#!/bin/bash

### このファイルの実行前に以下のファイルのグラフ名を変えておくこと
# 実行すれば、すべてのNGファイルが生成される
# []を消すのを忘れずに
# 1. 各Pythonスクリプトを実行する
python create-table.py
python create-non-group-table.py

# 2. file1 の特定の文字列削除と整形
# ここからは自分で行う
python format.py
# format.pyの実行でdynamic_groupsの整形は完了

echo "Processing complete."
