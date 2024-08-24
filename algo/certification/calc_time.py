def read_data(file_path):
    """指定されたファイルからデータを読み込む。"""
    data = {}
    with open(file_path, 'r') as file:
        entry = {}
        for line in file:
            line = line.strip()
            if line.startswith('Folder:'):
                entry['Folder'] = line.split(': ')[1]
            elif line.startswith('Execution time:'):
                entry['Execution time'] = int(line.split(': ')[1])
            elif line.startswith('Nodes:'):
                nodes = int(line.split(': ')[1].split(',')[0])
                entry['Nodes'] = nodes
            elif line == '-----------------------------':
                if 'Nodes' in entry:
                    data[entry['Nodes']] = entry['Execution time']
                entry = {}
    return data

def calculate_increase_percentage(data1, data2):
    """2つのデータからノード数ごとの実行時間増加割合を計算する。"""
    increase_percentages = {}
    for nodes, time1 in data1.items():
        if nodes in data2:
            time2 = data2[nodes]
            increase_percentage = ((time2 - time1) / time1) * 100
            increase_percentages[nodes] = increase_percentage
    return increase_percentages

def display_results(increase_percentages):
    """結果を表形式で表示する。ノード数を横軸、増加割合を縦軸とする。"""
    nodes = sorted(increase_percentages.keys())
    
    # ヘッダー行の作成
    header = " " * 10
    header += " ".join(f"{node:>10}" for node in nodes)
    print(header)
    
    # 増加割合の行を作成
    line = "Increase  "
    line += " ".join(f"{increase_percentages[node]:>10.2f}" for node in nodes)
    print(line)

def main():
    file_name_1 = "nojwt-result"
    file_name_2 = "jwt-result"
    file_path_1 = './construction/' + file_name_1 + '/overall_average_results.txt'
    file_path_2 = './every-time-construction/' + file_name_2 + '/overall_average_results.txt'

    # データ読み込み
    data1 = read_data(file_path_1)
    data2 = read_data(file_path_2)

    # 増加割合を計算
    increase_percentages = calculate_increase_percentage(data1, data2)

    # 結果を表示
    display_results(increase_percentages)

    
if __name__ == "__main__":
    main()
