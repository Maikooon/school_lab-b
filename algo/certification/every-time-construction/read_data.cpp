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

// 特定のファイルのデータを参照して、ノードが許可されているかを確認
bool isNodeAllowed(int current_node, int next_node, int next_community, const std::map<std::string, std::map<int, std::vector<int>>>& all_node_maps) {
    std::string filename = "community_" + std::to_string(next_community) + "_result.txt";
    //ファイルのコミュニテイxを指定する
    auto file_it = all_node_maps.find(filename);
    if (file_it != all_node_maps.end()) {
        const std::map<int, std::vector<int>>& node_map = file_it->second;
        auto it = node_map.find(next_node);
        if (it != node_map.end()) {
            std::vector<int>& allowed_nodes = it->second;
            if (std::find(allowed_nodes.begin(), allowed_nodes.end(), current_node) != allowed_nodes.end()) {
                std::cout << "数字 " << current_node << " はリストに存在します。\n";
                return true;
            }
            else {
                std::cout << "数字 " << current_node << " はリストに存在しません。\n";
                return false;
            }
        }
        else {
            std::cerr << "ノードが見つかりませんでした: " << next_node << std::endl;
            return false;
        }
    }
    else {
        std::cerr << "ファイルが見つかりませんでした: " << filename << std::endl;
        return false;
    }
}
