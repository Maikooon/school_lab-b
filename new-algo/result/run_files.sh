#!/bin/bash

# 実行ファイルのリストを指定（ファイルパスをそれぞれ変更してください）
EXECUTABLES=("./../algo/main" "./../algo/nogroup" "./../default-algo/rw")


# EXECUTABLES=( "./../algo/nogroup")

# 実行回数
NUM_RUNS=5

# 各実行ファイルについてループ
for executable in "${EXECUTABLES[@]}"
do
    echo "Executing $executable"
    for ((i=1; i<=NUM_RUNS; i++))
    do
        echo "Run #$i for $executable"
        ./$executable

        # 各回の結果をファイルに保存する場合、以下の行を使用
        # $executable > "${executable}_output_$i.txt"
    done
    echo "$executable の実行が完了しました。"
done

echo "すべての実行ファイルの実行が完了しました。"

python plt-hige.py
