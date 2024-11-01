"""
すべての方法に関するファイルを実行して、図まで出してくれたら天才

python3 
"""

import subprocess

# 実行するファイルのリスト
files_to_run = [
    "file1.py",
    "file2.py",
    "file3.py",
]  # 実行したいファイル名を追加してください

# それぞれのファイルを5回実行
for file in files_to_run:
    for i in range(5):
        print(f"Executing {file}, Attempt {i+1}")
        result = subprocess.run(["python3", file], capture_output=True, text=True)
        print(result.stdout)  # 実行結果の標準出力を表示
        if result.stderr:
            print(f"Error in {file}: {result.stderr}")  # エラーがあれば表示

# # 最後に test.py を実行
# print("Executing ple-hige.py")
# test_result = subprocess.run(["python3", "plt-hige.py"], capture_output=True, text=True)
# print(test_result.stdout)
# if test_result.stderr:
#     print(f"Error in test.py: {test_result.stderr}")
