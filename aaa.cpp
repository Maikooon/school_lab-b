#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>

using namespace std;

// データ構造の定義
using NodeMap = std::unordered_map<int, std::vector<int>>;
NodeMap ng_table;

// NGノードテーブルの読み込み関数
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

}

int main() {
    load_ng_table("./a.txt");


    int current_node = 31;
    int START_NODE = 1;

    // current_nodeに基づいて出力を確認
std:string a;
    auto it = ng_table.find(current_node);
    if (it != ng_table.end()) {
        std::cout << "NG nodes for community " << current_node << ": ";
        for (int num : it->second) {
            std::cout << num << " ";
            a += std::to_string(num) + " "; // ノードを文字列に追加
        }
        std::cout << std::endl;
    }

    // START_NODEが文字列aに含まれているか確認
    if (a.find(std::to_string(START_NODE)) != std::string::npos) {
        std::cout << "Node " << START_NODE << " is in the NG nodes for community " << current_node << std::endl;
    }
    else {
        std::cout << "Node " << START_NODE << " is not in the NG nodes for community " << current_node << std::endl;
    }

    return 0;
}
