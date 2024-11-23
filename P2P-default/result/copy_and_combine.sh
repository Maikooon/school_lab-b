#!/bin/bash

# 1. 各サーバからファイルをコピー
scp kate@giji4:./P2P-default/results/message.txt ./message.txt
ssh kate@giji4 "rm ./P2P-default/results/message.txt"  # リモートのファイルを削除

# 2. ファイルを1つにまとめる
cat ./message.txt > ./combined_logs.txt
#  それぞれのジャンル別の合計を求める
#TODO:
# python ./summarize.py >> ./logs/summarized_logs.txt

# 4. 不要なファイルを削除する
rm ./message.txt
# rm ./auth_server_logs.txt

# 5. 完了メッセージ
echo "すべてのファイルがコピーされ、combined_logs.txtにまとめられ、ジャンルごとに整理されました。不要なファイルは削除されました。"
