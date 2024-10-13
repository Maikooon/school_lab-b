#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <map>
#include <filesystem>  // C++17以降で利用可能

// 各ファイルのデータを保持するためのデータ構造
std::map<std::string, std::map<int, std::vector<int>>> loadAllowedNodesFromFiles(const std::string& base_dir) {
    std::map<std::string, std::map<int, std::vector<int>>> all_node_maps;

    // 指定されたディレクトリ内のすべてのファイルをループ処理
    for (const auto& entry : std::__fs::filesystem::directory_iterator(base_dir)) {
        std::string file_path = entry.path().string();
        std::string filename = entry.path().filename().string();
        std::map<int, std::vector<int>> node_map;

        // ファイルを開く
        std::ifstream file(file_path);
        if (!file.is_open()) {
            std::cerr << "ファイルを開けませんでした: " << file_path << std::endl;
            continue;  // ファイルを開けなかった場合、次のファイルに進む
        }
        std::cout << "ファイルを開けました: " << file_path << std::endl;

        std::string line;
        while (std::getline(file, line)) {
            std::istringstream iss(line);
            std::string key_part, values_part;

            if (std::getline(iss, key_part, ':') && std::getline(iss, values_part)) {
                int key = std::stoi(key_part);  // キーを整数として取得
                std::vector<int> allowed_nodes;
                std::istringstream values_stream(values_part);
                std::string value;

                while (std::getline(values_stream, value, ',')) {
                    if (!value.empty()) {
                        allowed_nodes.push_back(std::stoi(value));
                    }
                }

                node_map[key] = allowed_nodes;
            }
        }

        file.close();

        // ファイル名をキーとして、データを格納
        all_node_maps[filename] = node_map;
    }

    return all_node_maps;
}

