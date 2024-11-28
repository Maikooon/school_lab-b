total_time = []
across_server_list = []

# ファイルを読み込む
with open("./first-time/100-log.txt", "r", encoding="utf-8") as file:
    for line in file:
        # 'across_server' を含む行を探す
        if "total execution time" in line:
            # 値を抽出する
            total_time.append(line)
        if "'across_server':" in line:
            # 値を抽出する
            start = line.find("'across_server':") + len("'across_server':")
            end = line.find(",", start)  # 値の区切りを探す
            across_server_value = line[start:end].strip()  # 値を抽出してトリムする
            across_server_list.append(across_server_value)

            # 結果を出力
            print("Across Server Value:", across_server_value)

# ファイルに書き込む
with open("./first-time/100-log-mo.txt", "w", encoding="utf-8") as file:
    for i in range(len(across_server_list)):
        file.write(f"{total_time[i]}サーバのまたぎ回数: {across_server_list[i]}\n")
