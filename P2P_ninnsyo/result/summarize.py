import re

# データファイルを読み込み
with open("./combined_logs.txt", "r") as file:
    lines = file.readlines()

# 初期化
total_execution_time = 0.0
token_generation_time = 0.0
token_verification_time = 0.0
server_connection_time = 0.0
determinate_node_access_time = 0.0

# 各項目のパターン
execution_time_pattern = re.compile(r"Execution time:\s+([0-9.]+) seconds")
token_generation_time_pattern = re.compile(r"Time taken generate:\s+([0-9.]+) seconds")
token_verification_time_pattern = re.compile(r"Total JWT Verify Time:\s+([0-9.]+)")
server_connection_time_pattern = re.compile(r"Total JWT Connected:\s+([0-9.]+)")
determinate_node_access_time_pattern = re.compile(
    r"total_determinate_ng_nodes:\s+([0-9.]+)"
)

move_server_count = 0

# 各行を解析
for line in lines:
    # 条件に合う行を探索
    execution_time_match = execution_time_pattern.search(line)
    token_generation_time_match = token_generation_time_pattern.search(line)
    token_verification_time_match = token_verification_time_pattern.search(line)
    server_connection_time_match = server_connection_time_pattern.search(line)
    determinate_node_access_time_match = determinate_node_access_time_pattern.search(
        line
    )
    # 　合計値を加算していく
    if execution_time_match:
        total_execution_time += float(execution_time_match.group(1))
    if token_generation_time_match:
        token_generation_time += float(token_generation_time_match.group(1))
    if token_verification_time_match:
        token_verification_time += float(token_verification_time_match.group(1))
    if server_connection_time_match:
        move_server_count += 1
        server_connection_time += float(server_connection_time_match.group(1))
    if determinate_node_access_time_match:
        determinate_node_access_time += float(
            determinate_node_access_time_match.group(1)
        )

# 平均値を計算
# if try_count > 0:
#     total_execution_time /= try_count
#     token_generation_time /= try_count
#     token_verification_time /= try_count
#     server_connection_time /= try_count
#     determinate_node_access_time /= try_count

determinate_node_access_time *= 0.001

# 結果を表示
print(f"Total Execution Time: {total_execution_time} seconds")
print(f"Token Generation Time: {token_generation_time} seconds")
print(f"Token Verification Time: {token_verification_time} seconds")
print(f"Server Connection Time: {server_connection_time} seconds")
print(f"Determinate Node Access Time: {determinate_node_access_time} seconds")
print(f"Move Server Count: {move_server_count} times")
