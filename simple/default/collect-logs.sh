# サーバに保存されたログを集めるスクリプトです。ログは /var/log に保存されていると仮定しています。

# 実行時間  .results/message.txt
# またぎ回数　　./logs/count.txt

#!/bin/bash

# 1. 各サーバからファイルをコピー
scp kate@giji4:./simple/results/message.txt ./message.txt
ssh kate@giji4 "rm ./simple/results/message.txt"  # リモートのファイルを削除

scp kate@ab03:./simple/logs/count.txt ./across_server_count03.txt
ssh kate@ab03 "rm ./simple/logs/count.txt"  # リモートのファイルを削除

scp kate@ab06:./simple/logs/count.txt ./across_server_count06.txt
ssh kate@ab06 "rm ./simple/logs/count.txt"  # リモートのファイルを削除

# 2. ファイルを1つにまとめる
# ファイルがすでに存在したら、そのファイルを上書きする
cat ./message.txt ./across_server_count03.txt ./across_server_count03.txt >> ./combined_logs.txt

# 4. 不要なファイルを削除する
rm ./message.txt ./across_server_count03.txt ./across_server_count06.txt

# 5. 完了メッセージ
echo "すべてのファイルがコピーされ、combined_logs.txtにまとめられ、ジャンルごとに整理されました。不要なファイルは削除されました。"
