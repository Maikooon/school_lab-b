/*
エッジ権限のテーブルを作成するプログラム
 g++ -std=c++11 -o table table.cpp
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <vector>
#include <string>


std::vector<std::string>graph_file_list = {
        "ca-grqc-connected.gr", //0
        "cmu.gr", //1
        "com-amazon-connected.gr", //2
        "fb-caltech-connected.gr", //3
        "karate-graph.gr",   //4
        "karate.gr", //5
        "rt-retweet.gr", //6
        "simple_graph.gr", //7
        "soc-slashdot.gr", //8
        "tmp.gr", //9
};

std::string GRAPH = graph_file_list[3];
std::string modified_GRAPH = GRAPH.substr(0, GRAPH.size() - 3);
std::string filename = "./../Louvain/graph/" + GRAPH;  // 入力ファイルパス
std::string OUTPUT = "./new-table/" + modified_GRAPH + ".txt";  // 出力ファイルパス
// ファイルからグラフデータを読み取り、ノードの接続関係をマップに格納する関数
std::map<std::string, std::map<int, std::vector<int>>> create_map_from_file(const std::string& filename) {
    std::set<int> all_nodes;
    std::map<int, std::set<int>> neighbors;

    std::ifstream infile(filename);
    if (!infile) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return {};
    }

    int node1, node2;
    while (infile >> node1 >> node2) {
        all_nodes.insert(node1);
        all_nodes.insert(node2);
        neighbors[node1].insert(node2);
        neighbors[node2].insert(node1);
    }

    std::map<std::string, std::map<int, std::vector<int>>> data;
    std::set<std::string> processed_pairs;  // 処理済みのペアを追跡するセット

    // ファイルから直接読み取った接続されているノードペアに対してのみマップを作成
    for (const auto& [node1, neighbor_set] : neighbors) {
        for (int node2 : neighbor_set) {
            // 小さい方を最初にしたペアをキーとして使う
            int min_node = std::min(node1, node2);
            int max_node = std::max(node1, node2);
            std::string key = std::to_string(min_node) + " " + std::to_string(max_node);

            // 既に処理されたペアならスキップ
            if (processed_pairs.count(key) > 0) {
                continue;
            }

            std::map<int, std::vector<int>> walker_map;
            // walker_map[0] = std::vector<int>(neighbors[node1].begin(), neighbors[node1].end());
            // walker_map[1] = std::vector<int>(neighbors[node2].begin(), neighbors[node2].end());
            walker_map[0] = std::vector<int>(all_nodes.begin(), all_nodes.end());
            walker_map[1] = std::vector<int>(all_nodes.begin(), all_nodes.end());

            // 相手のノードを除外する
            walker_map[0].erase(std::remove(walker_map[0].begin(), walker_map[0].end(), node2), walker_map[0].end());
            walker_map[1].erase(std::remove(walker_map[1].begin(), walker_map[1].end(), node1), walker_map[1].end());

            data[key] = walker_map;

            // ペアを処理済みとして登録
            processed_pairs.insert(key);
        }
    }

    return data;
}

void print_map(const std::map<std::string, std::map<int, std::vector<int>>>& data) {
    for (const auto& [key, walkers] : data) {
        std::cout << key << ":\n";
        for (const auto& [direction, nodes] : walkers) {
            std::cout << " " << direction << ": ";
            for (const int node : nodes) {
                std::cout << node << " ";
            }
            std::cout << std::endl;
        }
    }
}

int main() {
    auto data = create_map_from_file(filename);

    print_map(data);  // マップの内容を表示

    // 書き出し処理
    std::ofstream outfile(OUTPUT);
    std::cout << "Writing to " << OUTPUT << std::endl;
    if (!outfile) {
        std::cerr << "Error creating output file" << std::endl;
        return 1;
    }

    for (const auto& [key, walkers] : data) {
        outfile << key << ":\n";
        for (const auto& [direction, nodes] : walkers) {
            outfile << " " << direction << ": ";
            for (const int node : nodes) {
                outfile << node << " ";
            }
            outfile << "\n";
        }
    }
    return 0;
}
