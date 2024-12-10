# #!/bin/bash

# # C++ソースファイルと出力ファイルの対応をリストで定義（key:source_fileの形式）
# cpp_files=("main:./main.cpp" "nogroup:./nogroup-main.cpp" "rw:./rw.cpp")
# # コンパイル処理
# for entry in "${cpp_files[@]}"; do
#     # entryをキーとソースファイルパスに分割
#     key="${entry%%:*}"
#     source_file="${entry#*:}"
#     output_dir="./"
    
#     # 出力フォルダが存在しない場合は作成
#     mkdir -p "$output_dir"
    
#     # 出力ファイルのフルパス
#     output_file="$output_dir/$key"
    
#     echo "Compiling $source_file to $output_file..."
    
#     # コンパイル実行
#     g++ -std=c++11 -o "$output_file" "$source_file"
    
#     # コンパイル結果の確認
#     if [[ $? -eq 0 ]]; then
#         echo "$source_file compiled successfully to $output_file."
#     else
#         echo "Error compiling $source_file."
#     fi
# done

#!/bin/bash

# GRAPH配列の定義
# # amaxon
# GRAPH_VALUES=("ng_0.05/METIS-ca/2")
#  "ng_0.05/METIS-com-amazon-connected/10"  "ng_0.05/METIS-com-amazon-connected/15"
#   "ng_0.05/METIS-com-amazon-connected/20"  "ng_0.05/METIS-com-amazon-connected/25" "ng_0.05/METIS-com-amazon-connected/30" "ng_0.05/METIS-com-amazon-connected/35" "ng_0.05/METIS-com-amazon-connected/40" 
#   "ng_0.05/METIS-com-amazon-connected/45" "ng_0.05/METIS-com-amazon-connected/50" "ng_0.05/METIS-com-amazon-connected/55" "ng_0.05/METIS-com-amazon-connected/60" "ng_0.05/METIS-com-amazon-connected/65" "ng_0.05/METIS-com-amazon-connected/70" )
#  "ng_0.05/METIS-com-amazon-connected/80" "ng_0.05/METIS-com-amazon-connected/85" "ng_0.05/METIS-com-amazon-connected/90")


# ca
GRAPH_VALUES=("ng_0.05/METIS-ca-ngrate/0.01" "ng_0.05/METIS-ca-ngrate/0.02"  "ng_0.05/METIS-ca-ngrate/0.03" "ng_0.05/METIS-ca-ngrate/0.04" "ng_0.05/METIS-ca-ngrate/0.05" "ng_0.05/METIS-ca-ngrate/0.06" "ng_0.05/METIS-ca-ngrate/0.07" "ng_0.05/METIS-ca-ngrate/0.08" "ng_0.05/METIS-ca-ngrate/0.09" "ng_0.05/METIS-ca-ngrate/0.005"
"ng_0.05/METIS-ca-ngrate/0.1" )
# "ng_0.05/METIS-ca-ngrate/0.01" "ng_0.05/METIS-cangrate/0.001")
# "ng_0.05/METIS-ca/20" "ng_0.05/METIS-ca/25" "ng_0.05/METIS-ca/30" "ng_0.05/METIS-ca/35" "ng_0.05/METIS-ca/40" "ng_0.05/METIS-ca/45" "ng_0.05/METIS-ca/50" "ng_0.05/METIS-ca/55"
# "ng_0.05/METIS-ca/60" "ng_0.05/METIS-ca/65" "ng_0.05/METIS-ca/70" )
# list  = (2 3 4)
# GRAPH_VALUES=("ng_0.05/METIS-com-amazon-connected/{list}")/

# コンパイル対象の C++ ソースファイルを選択
# cpp_files=("nogroup:./nogroup-main.cpp" )
cpp_files=("main:./main.cpp" "nogroup:./nogroup-main.cpp" "rw:./rw.cpp")
# cpp_files=("main:./main.cpp" "nogroup:./nogroup-main.cpp")
# cpp_files= ("nogroup:./nogroup-main.cpp")

# GRAPH配列ごとにコンパイルと実行
for GRAPH in "${GRAPH_VALUES[@]}"; do
    export GRAPH="$GRAPH"  # GRAPHを環境変数として設定
    
    echo "Processing with GRAPH=${GRAPH}..."
    
    # コンパイル処理
    for entry in "${cpp_files[@]}"; do
        echo "${entry}"
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
        if [[ $? -ne 0 ]]; then
            echo "Error compiling $source_file. Skipping..."
            continue
        fi
        echo "$source_file compiled successfully to $output_file."
        
        # 実行処理
        echo "Running $output_file with GRAPH=${GRAPH}..."
        
        # 実行
        "$output_file"
        
        # 実行結果の確認
        if [[ $? -eq 0 ]]; then
            echo "Execution with GRAPH=${GRAPH} completed successfully."
        else
            echo "Execution with GRAPH=${GRAPH} failed."
        fi
    done
done

echo "All processes complete."
