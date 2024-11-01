#!/bin/bash

# 1. 各サーバからファイルをコピー
scp kate@giji4:./P2P_ninnsyo/results/message.txt ./message.txt
ssh kate@giji4 "rm ./P2P_ninnsyo/results/message.txt"  # リモートのファイルを削除

scp kate@ab05:./P2P_ninnsyo/auth_server_logs.txt ./auth_server_logs.txt
ssh kate@ab05 "rm ./P2P_ninnsyo/auth_server_logs.txt"  # リモートのファイルを削除

scp kate@ab03:./P2P_ninnsyo/local_server_logs.txt ./local_server_logs_ab03.txt
ssh kate@ab03 "rm ./P2P_ninnsyo/local_server_logs.txt"  # リモートのファイルを削除

scp kate@ab03:./P2P_ninnsyo/access_limit_time.txt ./access_limit_time_ab03.txt
ssh kate@ab03 "rm ./P2P_ninnsyo/access_limit_time.txt"  # リモートのファイルを削除

scp kate@ab06:./P2P_ninnsyo/local_server_logs.txt ./local_server_logs_ab06.txt
ssh kate@ab06 "rm ./P2P_ninnsyo/local_server_logs.txt"  # リモートのファイルを削除

scp kate@ab06:./P2P_ninnsyo/access_limit_time.txt ./access_limit_time_ab06.txt
ssh kate@ab06 "rm ./P2P_ninnsyo/access_limit_time.txt"  # リモートのファイルを削除

scp kate@ab11:./P2P_ninnsyo/local_server_logs.txt ./local_server_logs_ab11.txt
ssh kate@ab11 "rm ./P2P_ninnsyo/local_server_logs.txt"  # リモートのファイルを削除

scp kate@ab11:./P2P_ninnsyo/access_limit_time.txt ./access_limit_time_ab11.txt
ssh kate@ab11 "rm ./P2P_ninnsyo/access_limit_time.txt"  # リモートのファイルを削除

# 2. ファイルを1つにまとめる
cat ./message.txt ./auth_server_logs.txt ./local_server_logs_ab03.txt ./access_limit_time_ab03.txt ./local_server_logs_ab06.txt ./access_limit_time_ab06.txt ./local_server_logs_ab11.txt ./access_limit_time_ab11.txt > ./combined_logs.txt

# 3. ジャンルごとにファイルをまとめる
# (例: auth_server_logs, local_server_logs, access_limit_timeのカテゴリで分ける)

# auth_server_logsをまとめる
cat ./auth_server_logs.txt > ./logs/auth_server_logs_combined.txt

# local_server_logsをまとめる
cat ./local_server_logs_ab03.txt ./local_server_logs_ab06.txt ./local_server_logs_ab11.txt > ./logs/local_server_logs_combined.txt

# access_limit_timeをまとめる
cat ./access_limit_time_ab03.txt ./access_limit_time_ab06.txt ./access_limit_time_ab11.txt > ./logs/access_limit_time_combined.txt

#  それぞれのジャンル別の合計を求める
#TODO:
python ./summarize.py >> ./logs/summarized_logs.txt

# 4. 不要なファイルを削除する
rm ./message.txt
rm ./auth_server_logs.txt
rm ./local_server_logs_ab03.txt
rm ./access_limit_time_ab03.txt
rm ./local_server_logs_ab06.txt
rm ./access_limit_time_ab06.txt
rm ./local_server_logs_ab11.txt
rm ./access_limit_time_ab11.txt

# 5. 完了メッセージ
echo "すべてのファイルがコピーされ、combined_logs.txtにまとめられ、ジャンルごとに整理されました。不要なファイルは削除されました。"
