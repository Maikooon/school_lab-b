import os


def get_file_size(file_path):
    """指定されたファイルのサイズをバイト単位で取得"""
    return os.path.getsize(file_path)


# 使用例: 複数のファイルのサイズを計算
file_paths = ["./path/to/file1.txt", "./path/to/file2.txt", "./path/to/file3.txt"]

for file_path in file_paths:
    try:
        file_size = get_file_size(file_path)
        print(f"ファイル {file_path} のサイズ: {file_size} バイト")
    except FileNotFoundError:
        print(f"ファイル {file_path} が見つかりませんでした。")
