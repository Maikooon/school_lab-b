/*
    エッジの権限を確認して、始点が移動の権限があるものをリストとして返す
    g++ -std=c++11 -o read read.cpp
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm> // std::find

// std::string file_path = "./allow-table/cmu.txt";

//行全体を読み込む
std::vector<std::string> read_file_lines(const std::string& file_path) {
    std::ifstream file(file_path);
    std::vector<std::string> lines;
    std::string line;

    // 行を1行ずつ読み込む
    while (std::getline(file, line)) {
        lines.push_back(line); // 読み込んだ行をベクトルに追加
    }
    return lines; // 読み込んだ行のベクトルを返す
}

std::vector<int> search_now_node_is_allowed(const std::vector<std::string>& lines, int now_node, int start_node) {
    std::vector<int> allow_table; // 許可されたノードを格納するベクトル

    // 3行ごとに処理するためにループ
    for (size_t i = 0; i < lines.size(); i += 3) {
        std::string column_line = lines[i];
        column_line.erase(std::remove(column_line.begin(), column_line.end(), ':'), column_line.end()); // ":" を除去

        // 列番号を取得するために整数に変換
        std::istringstream ss(column_line);
        std::vector<int> columns;
        int number;
        while (ss >> number) {
            columns.push_back(number);
        }

        // now_nodeが列番号の中に含まれているか確認
        if (std::find(columns.begin(), columns.end(), now_node) != columns.end()) {
            int opposite_node;
            std::string data_row;

            // 左側か右側かを判定
            if (columns[0] == now_node) {
                data_row = lines[i + 1]; // 左側のデータ行を取得
                opposite_node = columns[1];
            }
            else {
                data_row = lines[i + 2]; // 右側のデータ行を取得
                opposite_node = columns[0];
            }
            //debug 
            // std::cout << "node appear" << data_row << std::endl;
            // std::cout << "opposite_node: " << opposite_node << std::endl;

            // データ行から数字の部分をリストに変換
            std::istringstream data_ss(data_row);
            std::vector<int> row_values;

            // ":"の後の部分を抽出
            std::string line;
            std::getline(data_ss, line); // データ行を取得
            std::size_t colonPos = line.find(':');
            if (colonPos != std::string::npos) {
                std::string numberPart = line.substr(colonPos + 1);
                std::istringstream iss(numberPart);
                std::string number;

                // 空白で分割してベクターに格納
                while (iss >> number) {
                    row_values.push_back(std::stoi(number)); // 文字列を整数に変換して追加
                }
            }

            // 特定の数字を探す
            if (std::find(row_values.begin(), row_values.end(), start_node) != row_values.end()) {
                // std::cout << "Found: " << start_node << std::endl;
                //始点が許可されていたら、通れるエッジ先のノードを返す
                if (std::find(allow_table.begin(), allow_table.end(), opposite_node) == allow_table.end()) {
                    allow_table.push_back(opposite_node);
                }
            }
            else {
                std::cout << "Not Found: " << start_node << std::endl;
            }
        }
    }

    // この中から次の遷移先を決定する
    return allow_table; // 許可されたノードを返す
}


// int main() {
//     std::string file_path = "./allow-table/cmu.txt"; // 読み込むファイルのパス
//     int now_node = 1; // 探したいノード番号
//     int start_node = 1; // 始点ノード番号

//     // ファイルから行を読み込む
//     std::vector<std::string> table = read_file_lines(file_path);
//     // 読み込んだ行を使って許可されたノードを検索
//     std::vector<int> allowed_nodes = search_now_node_is_allowed(table, now_node, start_node);

//     // 許可されたノードを表示
//     std::cout << "許可されたノード: ";
//     for (int node : allowed_nodes) {
//         std::cout << node << " ";
//     }
//     std::cout << std::endl;

//     return 0;
// }