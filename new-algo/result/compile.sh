#!/bin/bash

# グローバル変数を環境変数として設定
export GRAPH="METIS-ca"
export GRAPH_NAME="ca-grqc-connected"
export ALLNODE=14113

# C++ソースファイルと出力ファイルの対応をリストで定義（key:source_fileの形式）
cpp_files=("main:./../algo/main.cpp" "nogroup:./../algo/nogroup-main.cpp" "rw:./../default-algo/rw.cpp")

# コンパイル処理
for entry in "${cpp_files[@]}"; do
    # entryをキーとソースファイルパスに分割
    key="${entry%%:*}"
    source_file="${entry#*:}"
    
    # 出力ファイルのディレクトリとファイル名を指定
    if [[ "$key" == "rw" ]]; then
        output_dir="./../default-algo"
    else
        output_dir="./../algo"
    fi
    
    # 出力フォルダが存在しない場合は作成
    mkdir -p "$output_dir"
    
    # 出力ファイルのフルパス
    output_file="$output_dir/$key"
    
    echo "Compiling $source_file to $output_file..."
    
    # コンパイル実行
    g++ -std=c++11 -o "$output_file" "$source_file"
    
    # コンパイル結果の確認
    if [[ $? -eq 0 ]]; then
        echo "$source_file compiled successfully to $output_file."
    else
        echo "Error compiling $source_file."
    fi
done
