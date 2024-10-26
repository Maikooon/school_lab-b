// ファイルを読み込む関数



#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <set>
#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>

using namespace std;

// データ構造の定義
using NodeMap = std::unordered_map<int, std::vector<int>>;

NodeMap community_data;

// NGノードテーブルの読み込み関数
using NodeMap = std::unordered_map<int, std::vector<int>>;

NodeMap ng_table;

void load_ng_table(const std::string& filepath) {
    std::ifstream file(filepath);
    std::string line;

    if (!file.is_open()) {
        std::cerr << "Error: Could not open the file." << std::endl;
        return;
    }

    while (std::getline(file, line)) {
        std::istringstream iss(line);
        int community, node;

        // ':' を使ってコミュニティIDを分割する
        if (std::getline(iss, line, ':')) {
            community = std::stoi(line); // コミュニティIDを整数に変換
            while (iss >> node) {
                ng_table[community].push_back(node); // ノードをベクターに追加
            }
        }
    }
    file.close();
    // Output the loaded ng_table contents
    std::cout << "NG Table Contents:\n";
    for (const auto& [community, nodes] : ng_table) {
        std::cout << community;
        for (const int node : nodes) {
            std::cout << node << " ";
        }
        std::cout << std::endl;
    }
}

int main() {
    load_ng_table("./a.txt");

    return 0;
}
