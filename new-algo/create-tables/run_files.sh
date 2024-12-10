#!/bin/bash

### このファイルの実行前に以下のファイルのグラフ名を変えておくこと
# 実行すれば、すべてのNGファイルが生成される
# []を消すのを忘れずに


# 変数をエクスポート
# export GRAPH="ng_0.05/METIS-com-amazon-connected/200"  # グラフを格納するファイルの名前
# export GRAPH="ng_0.05/METIS-ca/100{<_COM_NUM}"  # グラフを格納するファイルの名前
# export GRAPH_NAME="ca-grqc-connected"  # 正規のグラフの名前
# export GRAPH_COMMUNITY="ng_0.05/METIS-ca"  # NGノードを含むグラフの名前
# export NG_RATE=0.05  # NGノードの割合
# export COM_NUM=100

# 定義された環境変数
# export COM_NUM=100
# export NG_RATE=0.05
# export GRAPH_COMMUNITY="ng_${NG_RATE}/METIS-ca"
# export GRAPH_NAME="ca-grqc-connected"

# # COM_NUMを使用してGRAPHを定義
# export GRAPH="${GRAPH_COMMUNITY}/${COM_NUM}"

# # 1. 各Pythonスクリプトを実行する
# # dynamic とngが生成される
# python create-table.py


# # 2. file1 の特定の文字列削除と整形
# # ここからは自分で行う
# # python create-non-group-table.py
# python format.py
# # format.pyの実行でdynamic_groupsの整形は完了

# echo "Processing complete."

# コミュニテcいの数で実験----------------------------------------------------------------------
#!/bin/bash

# # 定義された環境変数
# export NG_RATE=(0.05 0.1)
# export GRAPH_COMMUNITY="ng_0.05/METIS-com-amazon-connected"
# export GRAPH_NAME="com-amazon-connected"    

# # COM_NUMの値を配列で指定
# COM_NUM_ARRAY=(3)


# # 配列の値でループ処理
# for COM_NUM in "${COM_NUM_ARRAY[@]}"; do
#     export COM_NUM  # 環境変数に設定
#     export GRAPH="${GRAPH_COMMUNITY}/${COM_NUM}"  # GRAPHを再定義

#     echo "Processing for COM_NUM=${COM_NUM}..."

#     # 1. 各Pythonスクリプトを実行
#     python create-table.py

#     # 2. 必要な整形処理
#     python format.py

#     echo "Processing for COM_NUM=${COM_NUM} complete."
# done

# echo "All processes complete."



# NGノードの割合で実験----------------------------------------------------------------------
#!/bin/bash

# 定義された環境変数   %単位　　最大１
export NG_RATES=(0.1)  # NGレートを変更  100分の１、1000分の１
# export NG_RATES=( 0.1 )
export GRAPH_COMMUNITY="ng_0.05/METIS-ca-ngrate"  # NGノードを含むグラフの名前
export GRAPH_NAME="ca-grqc-connected"    

# COM_NUMの値を指定
COM_NUM=3


# NG_RATE別でループ処理
for NG_RATE in "${NG_RATES[@]}"; do
    export NG_RATE  # NG_RATEを環境変数に設定
    export GRAPH="${GRAPH_COMMUNITY}/${NG_RATE}"  # GRAPHを再定義
    echo "Processing for NG_RATE=${NG_RATE}..."


    # 1. 各Pythonスクリプトを実行
    python create-table.py

    # 2. 必要な整形処理
    python create-non-group-table.py
    python format.py

    echo "Processing for NG_RATE=${NG_RATE} complete."
done

echo "All processes complete."
