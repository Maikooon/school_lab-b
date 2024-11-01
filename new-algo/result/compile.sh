#!/bin/bash

# C++ソースファイルと出力ファイルの対応を定義
declare -A cpp_files
cpp_files["main"]="./../algo/main.cpp"
cpp_files["nogroup"]="./../algo/nogroup.cpp"
cpp_files["rw"]="./../default-algo/rw.cpp"

# コンパイル処理
for key in "${!cpp_files[@]}"; do
    source_file=${cpp_files[$key]}
    
    # 出力ファイルのパスを指定
    if [[ $key == "rw" ]]; then
        output_file="./../default-algo/rw"  # default-algo用
    else
        output_file="./../algo/$key"  # algo用
    fi
    
    echo "Compiling $source_file to $output_file..."
    
    g++ -o "$output_file" "$source_file"
    g++ -std=c++11 $"" -o "$output_file"
    
    if [[ $? -eq 0 ]]; then
        echo "$source_file compiled successfully to $output_file."
    else
        echo "Error compiling $source_file."
    fi
done
