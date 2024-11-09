#!/bin/bash
# 分散環境での実験に必要なファイルをすべて作成するスクリプト
# ただ、すべてのコミュニティに少なくとも一つのノードがあることを確認すること


# GRAPHの値を定義
GRAPH="ca-grqc-connected"

# PythonスクリプトにGRAPH変数を環境変数として渡す
export GRAPH=$GRAPH

# # Step 1: Execute the Python scripts in sequence
# python3 1-my-one-division.py
# python3 2-add-IP.py

# # Step 1-2: Rename the output files
# mv ./by-my-own-division/$GRAPH/community_0.txt ./by-my-own-division/$GRAPH/abilene03.txt
# mv ./by-my-own-division/$GRAPH/community_1.txt ./by-my-own-division/$GRAPH/abilene06.txt
# mv ./by-my-own-division/$GRAPH/community_2.txt ./by-my-own-division/$GRAPH/abilene11.txt

# Step 2: Run the third Python script
python3 3-sub-edge.py 

# Step 2-1: Consolidate community files into server-specific files
cat ./by-METIS/$GRAPH/community_A.txt ./by-METIS/$GRAPH/community_B.txt > ./by-METIS/$GRAPH/server_abilene03_edges_community.txt
cat ./by-METIS/$GRAPH/community_C.txt ./by-METIS/$GRAPH/community_D.txt > ./by-METIS/$GRAPH/server_abilene06_edges_community.txt
cat ./by-METIS/$GRAPH/community_E.txt ./by-METIS/$GRAPH/community_F.txt > ./by-METIS/$GRAPH/server_abilene11_edges_community.txt

# Step 2-3: Remove the no longer needed community files
rm ./by-METIS/$GRAPH/community_A.txt
rm ./by-METIS/$GRAPH/community_B.txt
rm ./by-METIS/$GRAPH/community_C.txt
rm ./by-METIS/$GRAPH/community_D.txt
rm ./by-METIS/$GRAPH/community_E.txt
rm ./by-METIS/$GRAPH/community_F.txt

# Step 3: Run the third Python script
python3 5-create-role-group.py 

echo "Scripts executed, files renamed, and server-specific files created successfully."
