#!/bin/bash

# C++ソースファイルと出力ファイルの対応をリストで定義（key:source_fileの形式）
cpp_files=("main:./main.cpp" "nogroup:./nogroup-main.cpp" "rw:./rw.cpp")
# コンパイル処理
for entry in "${cpp_files[@]}"; do
    # entryをキーとソースファイルパスに分割
    key="${entry%%:*}"
    source_file="${entry#*:}"
    output_dir="./"
    
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
