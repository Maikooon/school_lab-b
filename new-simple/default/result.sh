# 命令サーバから実行時間をまたぎ回数を取得する
# 命令サーバは上書きされるので、複数回実行したあとに、こちらのシェルファイルを実行することで、行う

#!/bin/bash

# 1. 各サーバからファイルをコピー
scp kate@ab11:./new-simple/default/log.txt ./log.txt
ssh kate@ab11 "rm ./new-simple/default/log.txt"  # リモートのファイルを削除

# 5. 完了メッセージ
echo "すべてのファイルがコピーされ、combined_logs.txtにまとめられ、ジャンルごとに整理されました。不要なファイルは削除されました。"
