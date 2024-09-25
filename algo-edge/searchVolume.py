import os


def get_file_sizes_in_directory(directory):
    """
    指定したディレクトリ内のすべてのファイルのサイズを表示する関数

    Args:
        directory (str): 対象ディレクトリのパス
    """
    total_size = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            total_size += size
            print(f"ファイル: {file}, サイズ: {size:,} バイト")

    print(f"総ファイルサイズ: {total_size:,} バイト")


if __name__ == "__main__":
    target_directory = "./new-table/"
    # target_directory = "./../create_table/table/fb-caltech-connected/"
    get_file_sizes_in_directory(target_directory)
