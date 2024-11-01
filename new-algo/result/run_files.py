# """
# すべての方法に関するファイルを実行して、図まで出してくれたら天才

# python3
# """

# import subprocess
# import os


# # シェルスクリプトを実行する関数
# def run_compile_script():
#     print("Running compile script...")
#     result = subprocess.run(["bash", "compile.sh"], capture_output=True, text=True)

#     print(result.stdout)  # 実行結果の標準出力を表示
#     if result.stderr:
#         print(f"Error in compile script: {result.stderr}")  # エラーがあれば表示


# # 実行する関数
# def run_executable(executable):
#     print(f"Executing {executable}...")
#     result = subprocess.run([executable], capture_output=True, text=True)

#     print(result.stdout)  # 実行結果の標準出力を表示
#     if result.stderr:
#         print(f"Error in {executable}: {result.stderr}")  # エラーがあれば表示


# # メインロジック
# run_compile_script()  # コンパイルスクリプトを実行

# # 実行するファイルのリスト
# # 実行するファイルのリスト
# executables = [
#     os.path.abspath("./../algo/main"),
#     os.path.abspath("./../algo/nogroup"),
#     os.path.abspath("./../algo/rw"),
# ]
# # それぞれのファイルを5回実行
# for file in executables:
#     for i in range(5):
#         print(f"Executing {file}, Attempt {i+1}")
#         # 実行ファイルを直接呼び出し
#         result = subprocess.run([file], capture_output=True, text=True)
#         print(result.stdout)  # 実行結果の標準出力を表示
#         if result.stderr:
#             print(f"Error in {file}: {result.stderr}")  # エラーがあれば表示

# # # 最後に test.py を実行
# # print("Executing ple-hige.py")
# # test_result = subprocess.run(["python3", "plt-hige.py"], capture_output=True, text=True)
# # print(test_result.stdout)
# # if test_result.stderr:
# #     print(f"Error in test.py: {test_result.stderr}")

import subprocess
import os

# コンパイルと実行を行うC++ファイルのリスト
cpp_files_to_compile = [
    "./../algo/main.cpp",
    "./../algo/nogroup-main.cpp",
    "./../default-algo/rw.cpp",
]  # ここにコンパイルしたいファイルを追加

# 各C++ファイルに対してコンパイルと実行
for cpp_file in cpp_files_to_compile:
    # 出力ファイル名をC++ファイル名から生成 (拡張子なしのファイル名)
    output_file = os.path.splitext(os.path.basename(cpp_file))[0]

    # コンパイルコマンド
    # compile_command = ["g++", "-o", output_file, cpp_file]
    compile_command = ["g++", "-std=c++11", cpp_file, "-o", output_file]
    compile_result = subprocess.run(compile_command, capture_output=True, text=True)

    # コンパイルエラーチェック
    if compile_result.returncode != 0:
        print(f"Compilation failed for {cpp_file}:\n{compile_result.stderr}")
        continue
    else:
        print(f"Compilation succeeded for {cpp_file} -> {output_file}")

    # コンパイル成功後、出力ファイルを5回実行
    for i in range(5):
        print(f"Executing {output_file}, Attempt {i+1}")
        result = subprocess.run([f"./{output_file}"], capture_output=True, text=True)
        print(result.stdout)  # 実行結果の標準出力を表示
        if result.stderr:
            print(
                f"Error during execution of {output_file}: {result.stderr}"
            )  # エラーがあれば表示
