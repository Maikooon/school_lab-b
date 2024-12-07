/*
いじらない
何も汚染されていないRWのアルゴリズム
g++ -std=c++11 rw.cpp -o rw
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include "config.h"

using namespace std;

// g++ -std=c++11 main.cpp -o main


unordered_map<int, unordered_set<int>> graph;
unordered_map<int, int> node_communities;

// ファイルを読み込んでグラフを構築
void load_graph(const std::string& file_path) {
    ifstream edges_file(file_path);
    if (!edges_file.is_open()) {
        cerr << "Failed to open edges file: " << file_path << endl;
        exit(1);
    }

    string line;
    while (getline(edges_file, line)) {
        if (line.empty()) continue;
        istringstream iss(line);
        int node1, node2;
        if (!(iss >> node1 >> node2)) {
            cerr << "Error reading edge data." << endl;
            exit(1);
        }
        graph[node1].insert(node2);
        graph[node2].insert(node1);
    }
    edges_file.close();

    // load_graph 関数内でのデバッグ
    // for (const auto& node : graph) {
    //     std::cout << "Node " << node.first << " has neighbors: ";
    //     for (const auto& neighbor : node.second) {
    //         std::cout << neighbor << " ";
    //     }
    //     std::cout << std::endl;
    // }

}

// コミュニティファイルを読み込んでノードのコミュニティを登録
void load_communities(const std::string& file_path) {
    ifstream communities_file(file_path);
    if (!communities_file.is_open()) {
        cerr << "Failed to open communities file: " << file_path << endl;
        exit(1);
    }

    string line;
    while (getline(communities_file, line)) {
        if (line.empty()) continue;
        istringstream iss(line);
        int node, community;
        if (!(iss >> node >> community)) {
            cerr << "Error reading community data." << endl;
            exit(1);
        }
        node_communities[node] = community;
    }
    communities_file.close();
}

// ランダムウォークを実行
vector<int> random_walk(int& total_move, int START_NODE) {
    int move_count = 0;
    vector<int> path;
    int current_node = START_NODE;
    path.push_back(current_node);

    while ((double)rand() / RAND_MAX > ALPHA) {
        printf("current_node: %d\n", current_node);
        auto neighbors = graph[current_node];
        printf("neighbors: %d\n", neighbors.size());
        if (neighbors.empty()) {
            break;
        }

        // 隣接ノードからランダムに次のノードを選択
        int next_node = *next(neighbors.begin(), rand() % neighbors.size());
        path.push_back(next_node);

        // コミュニティが異なる場合
        if (node_communities[current_node] != node_communities[next_node]) {
            // cout << "Node " << next_node << " (Community " << node_communities[next_node] << ") is in a different community from Node " << current_node << " (Community " << node_communities[current_node] << ")" << endl;
            move_count++;
        }

        current_node = next_node;
    }
    //コミュニティが異なるときの移動回数
    total_move += move_count;
    return path;
}


// void saveResultsToFile(const std::string& filePath, const std::string& results) {
//     // std::ofstreamを使用してファイルを開く。ios::truncを指定して上書き。
//     std::ofstream outputFile(filePath, std::ios::out | std::ios::app);

//     // ファイルが正常に開けたかを確認
//     if (!outputFile) {
//         std::cerr << "ファイルを開くことができませんでした: " << filePath << std::endl;
//         return;
//     }

//     // 結果をファイルに書き込む
//     outputFile << results;

//     // ファイルを閉じる
//     outputFile.close();
// }
void saveResultsToFile(const std::string& filePath, const std::string& results) {
    std::__fs::filesystem::path dirPath = std::__fs::filesystem::path(filePath).parent_path();

    // ディレクトリが存在しない場合、作成する
    if (!std::__fs::filesystem::exists(dirPath)) {
        try {
            std::__fs::filesystem::create_directories(dirPath);
        }
        catch (const std::__fs::filesystem::filesystem_error& e) {
            std::cerr << "ディレクトリの作成に失敗しました: " << e.what() << std::endl;
            return;
        }
    }
    std::ofstream outputFile(filePath, std::ios::out | std::ios::app);
    if (!outputFile) {
        std::cerr << "ファイルを開くことができませんでした: " << filePath << std::endl;
        return;
    }
    outputFile << results;
    outputFile.close();
}

// 千位区切りを追加する関数
string addThousandSeparator(long long number) {
    stringstream ss;
    ss.imbue(locale("en_US.UTF-8"));  // ロケールを指定（US英語のスタイル）
    ss << fixed << number;
    return ss.str();
}


/*------------------------------------------------------------------------------------------------------------------------*/

// プログラムの実行
int main() {
    // 時間計測を開始（ナノ秒）


    srand(time(nullptr));  // ランダムシードの初期化

    // グラフとコミュニティのロード
    load_graph(GRAPH_FILE);
    load_communities(COMMUNITY_FILE);

    int total_move = 0;
    int total_length = 0;
    auto start_time = chrono::high_resolution_clock::now();


    // vector<int> start_nodes(ALLNODE);  // 1〜32までのノードをスタートノードとして設定

    // // 1〜32までのノードを start_nodes 配列に代入
    // for (int i = 0; i < ALLNODE; ++i) {
    //     start_nodes[i] = i + 1;  // ノード番号を1からスタートさせる
    // }
    vector<int> start_nodes(1);  // 1つのスタートノードを設定
    start_nodes[0] = START_NODE;

    // 複数のスタートノードに対してランダムウォークを実行
    for (int start_node : start_nodes) {
        int start_community = node_communities[start_node];

        // ランダムウォークを複数回実行
        for (int i = 0; i < RW_COUNT; ++i) {
            vector<int> path = random_walk(total_move, start_node);
            total_length += path.size();

            // パスを出力
            cout << "Random walk " << i + 1 << " path:";
            for (int node : path) {
                cout << " " << node;
            }
            cout << endl;
        }
    }

    // 平均経路長を計算して出力
    double average_length = static_cast<double>(total_length) / RW_COUNT;
    cout << "Average path length: " << average_length << endl;
    cout << "Total moves by nodes: " << total_length << endl;
    cout << "Total moves across communities: " << total_move << endl;

    // 時間計測を終了して結果を表示（ナノ秒）
    auto end_time = chrono::high_resolution_clock::now();
    // printf("Program execution time: %ld nanoseconds\n", chrono::duration_cast<chrono::nanoseconds>(end_time - start_time).count());
    auto duration = chrono::duration_cast<chrono::nanoseconds>(end_time - start_time).count();
    cout << "Program execution time: " << duration << " nanoseconds" << endl;
    cout << "Program execution time: " << addThousandSeparator(duration) << " nanoseconds" << endl;


    //結果を出力する
   // 保存したい結果
    std::string results = "Average path length: " + std::to_string(average_length) + "\n";
    results += "Total moves by nodes: " + std::to_string(total_length) + "\n";
    results += "Total moves across communities: " + std::to_string(total_move) + "\n";
    results += "Program execution time: " + std::to_string(duration) + " nanoseconds\n";
    results += "Program execution time: " + addThousandSeparator(duration) + " nanoseconds\n";

    // ファイルパス
    std::string filePath = "./../result-1207/" + GRAPH + "/default.txt";

    // 結果をファイルに保存
    saveResultsToFile(filePath, results);

    std::cout << "結果をファイルに保存しました。" << std::endl;
    return 0;
}