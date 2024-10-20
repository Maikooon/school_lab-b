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

using namespace std;

// グローバル変数の定義
const std::string COMMUNITY_FILE = "./../../Louvain/community/karate.tcm";
const std::string GRAPH_FILE = "./../../Louvain/graph/karate.gr";
const double ALPHA = 0.15;
const int RW_COUNT = 1000;  // ランダムウォークの実行回数
int START_NODE = 1;         // ランダムウォークの開始ノード

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
        auto neighbors = graph[current_node];
        if (neighbors.empty()) {
            break;
        }

        // 隣接ノードからランダムに次のノードを選択
        int next_node = *next(neighbors.begin(), rand() % neighbors.size());
        path.push_back(next_node);

        // コミュニティが異なる場合
        if (node_communities[current_node] != node_communities[next_node]) {
            cout << "Node " << next_node << " (Community " << node_communities[next_node] << ") is in a different community from Node " << current_node << " (Community " << node_communities[current_node] << ")" << endl;
            move_count++;
        }

        current_node = next_node;
    }
    total_move += move_count;
    return path;
}

// プログラムの実行
int main() {
    // 時間計測を開始（ナノ秒）
    auto start_time = chrono::high_resolution_clock::now();

    srand(time(nullptr));  // ランダムシードの初期化

    // グラフとコミュニティのロード
    load_graph(GRAPH_FILE);
    load_communities(COMMUNITY_FILE);

    int total_move = 0;
    int total_length = 0;

    // ランダムウォークを複数回実行
    for (int i = 0; i < RW_COUNT; ++i) {
        vector<int> path = random_walk(total_move, START_NODE);
        total_length += path.size();

        // パスを出力
        cout << "Random walk " << i + 1 << " path:";
        for (int node : path) {
            cout << " " << node;
        }
        cout << endl;
    }

    // 平均経路長を計算して出力
    double average_length = static_cast<double>(total_length) / RW_COUNT;
    cout << "Average path length: " << average_length << endl;
    cout << "Total moves across communities: " << total_move << endl;

    // 時間計測を終了して結果を表示（ナノ秒）
    auto end_time = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::nanoseconds>(end_time - start_time).count();
    cout << "Program execution time: " << duration << " nanoseconds" << endl;

    return 0;
}