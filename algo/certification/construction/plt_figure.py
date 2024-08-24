import matplotlib.pyplot as plt
import os 

# データファイルのパス
file_name_1 = "nojwt-result"
file_name_2 = "result"
output_folder = './figure'

file_path_1 = './' + file_name_1+ '/overall_average_results.txt'
file_path_2 = './' + file_name_2 + '/overall_average_results.txt'


# ファイルからデータを読み取る関数
def read_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        entry = {}
        for line in file:
            line = line.strip()
            if line.startswith('Folder:'):
                entry['Folder'] = line.split(': ')[1]
            elif line.startswith('Execution time:'):
                entry['Execution time'] = int(line.split(': ')[1])
            elif line.startswith('Nodes:'):
                entry['Nodes'] = int(line.split(': ')[1].split(',')[0])
            elif line == '-----------------------------':
                data.append(entry)
                entry = {}
    return data



data1 = read_data(file_path_1)
data2 = read_data(file_path_2)

# プロット用データの抽出
nodes1 = [entry['Nodes'] for entry in data1]
times1 = [entry['Execution time'] for entry in data1]

nodes2 = [entry['Nodes'] for entry in data2]
times2 = [entry['Execution time'] for entry in data2]

# プロットの作成
# plt.figure(figsize=(10, 6))\
plt.figure()

# 入力で幅を指定
xlim_max = int(input("Enter the maximum x limit (e.g., 1000): "))
ylim_max = int(input("Enter the maximum y limit (e.g., 200): "))

plt.xlim(0, xlim_max)
plt.ylim(0, ylim_max)
plt.scatter(nodes1, times1, color='blue', label=file_name_1)
plt.scatter(nodes2, times2, color='red', label=file_name_2)



# ラベル設定
plt.xlabel('Number of Nodes')
plt.ylabel('Execution Time')
plt.title('Execution Time vs Number of Nodes')
plt.legend()

# グリッドを追加
plt.grid(True)

# プロットをファイルに保存ー幅がわかるように変更
output_path = os.path.join(output_folder, file_name_1 + "&" + file_name_2 + "-" + str(xlim_max) + "-"+ str(ylim_max) + '.png')
plt.savefig(output_path)

# 終了メッセージを表示
print(f'Scatter plot saved to: {output_path}')
