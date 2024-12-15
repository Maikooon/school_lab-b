"""
簡易的な実験を行うために、それぞれのサーバへの留まり確立を計算します
留まり確立により、簡易的な実験が可能になります

テスト２で重複ありで実験済みなので、正当性は保証

実行前に変更すること
以下を一致させること
・読み込むファイル
・サーバアドレスの変更

出力
・最終的な出力は一つの表にまとめて格納されます
"""

import os

# ファイルの読み込み
# input_file = "./test2/abilene03.txt"
input_file = "./fb-caltech-connected/abilene11.txt"
# 自分のサーバアドレス
current_server = "10.58.60.11"

# データの読み込みと解析
edges = []
with open(input_file, "r") as file:
    for line in file:
        src, dest, server = line.strip().split(",")
        edges.append((int(src), int(dest), server))

# 各ノードごとにサーバ留まり確率とサーバ間移動確率を計算
node_stats = {}

for src, dest, server in edges:
    if src not in node_stats:
        node_stats[src] = {"stay": 0, "move": {}, "total": 0}

    # 自分のサーバに留まる場合
    if server == current_server:
        node_stats[src]["stay"] += 1
    else:
        # 移動先のサーバを記録
        if server not in node_stats[src]["move"]:
            node_stats[src]["move"][server] = 0
        node_stats[src]["move"][server] += 1
    node_stats[src]["total"] += 1

# 確率の計算
results = {}
for node, stats in node_stats.items():
    stay_prob = stats["stay"] / stats["total"] if stats["total"] > 0 else 0
    move_probs = {
        server: count / stats["total"] for server, count in stats["move"].items()
    }
    results[node] = {"stay_prob": stay_prob, "move_probs": move_probs}

# 結果を表示
for node, probabilities in results.items():
    print(f"ノード {node}:")
    print(f"  サーバに留まる確率: {probabilities['stay_prob']:.2f}")
    for server, move_prob in probabilities["move_probs"].items():
        print(f"  サーバ {server} への移動確率: {move_prob:.2f}")
    print()

# サーバ全体の移動率をまとめて出力
server_total_moves = {}
for probabilities in results.values():
    for server, move_prob in probabilities["move_probs"].items():
        if server not in server_total_moves:
            server_total_moves[server] = 0
        server_total_moves[server] += move_prob

# 全体の留まり確率と各サーバへの移動率
total_stay_prob = sum(probabilities["stay_prob"] for probabilities in results.values())
per_total_stay_prob = total_stay_prob / len(results)

print(f"全体の留まり確率: {total_stay_prob:.2f}")
print(f"平均の留まり確率: {per_total_stay_prob:.2f}")
print("サーバごとの全体移動確率:")
for server, total_move_prob in server_total_moves.items():
    ave_total_move_prob = total_move_prob / len(results)
    print(f"  サーバ {server}: {ave_total_move_prob:.2f}")

# ファイルに結果を書き込む
output_file = "./detailed-move-prob.txt"
with open(output_file, "a") as file:  # 追記モード
    file.write(f"file {input_file}:\n")
    file.write(f"サーバ {current_server}:\n")
    file.write(f"平均の留まり確率: {per_total_stay_prob:.4f}\n")
    file.write("サーバごとの全体移動確率:\n")
    for server, total_move_prob in server_total_moves.items():
        ave_total_move_prob = total_move_prob / len(results)
        file.write(f"  サーバ {server}: {ave_total_move_prob:.4f}\n")
