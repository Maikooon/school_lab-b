/*
defailt のRWにテーブル参照を加えて時間を計測するもの
まだ、構造体の必要性はないので、普通のRWでテストを行う

実行コマンド
g++ -std=c++11 main.cpp -o main
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
#include <set>

using namespace std;

// グローバル変数の定義
const std::string COMMUNITY_FILE = "./../../Louvain/community/karate.tcm";
const std::string GRAPH_FILE = "./../../Louvain/graph/karate.gr";
const std::string GROUP_PER_COMMUNITY = "./../create-tables/dynamic_groups.txt";
const std::string NG_NODES_PER_COMMUNITY = "./../create-tables/ng_nodes.txt";

const double ALPHA = 0.15;
const int RW_COUNT = 1;  // ランダムウォークの実行回数
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

/*------------------------------------------------------------------------------------------------------------------------*/
// 読み込みの関数を定義
// コミュニティごとのグループとNGノードを保持するためのデータ構造

using CommunityGroups = std::unordered_map<int, std::unordered_map<int, std::vector<int>>>;
using CommunityNGNodes = std::unordered_map<int, std::unordered_map<int, std::set<int>>>;

// グローバル変数
CommunityGroups community_groups;
CommunityNGNodes community_ng_nodes;

// グループテーブルの読み込み関数
void load_community_groups(const std::string& filepath) {
    std::ifstream file(filepath);
    std::string line;
    int community, group;
    std::vector<int> nodes;

    while (std::getline(file, line)) {
        std::istringstream iss(line);
        if (iss >> community) {
            while (iss >> group) {
                int node;
                while (iss >> node) {
                    community_groups[community][group].push_back(node);
                }
            }
        }
    }
}

// NGノードテーブルの読み込み関数
void load_community_ng_nodes(const std::string& filepath) {
    std::ifstream file(filepath);
    std::string line;
    int community, group, node;

    while (std::getline(file, line)) {
        std::istringstream iss(line);
        if (iss >> community) {
            while (iss >> group) {
                while (iss >> node) {
                    community_ng_nodes[community][group].insert(node);
                }
            }
        }
    }
}
/*------------------------------------------------------------------------------------------------------------------------*/

// ランダムウォークを実行  1RWの誕生から死滅まですべて
vector<int> random_walk(int& total_move, int START_NODE) {
    int move_count = 0;
    vector<int> path;
    int current_node = START_NODE;
    path.push_back(current_node);

    //遷移確立が終わるまで繰り返す
    while ((double)rand() / RAND_MAX > ALPHA) {
        auto neighbors = graph[current_node];
        if (neighbors.empty()) {
            break;
        }

        // 隣接ノードからランダムに次のノードを選択
        int next_node = *next(neighbors.begin(), rand() % neighbors.size());
        printf("current_node: %d, next_node: %d\n", current_node, next_node);

        // 現在のノードとHop先のコミュニティが異なる場合
        if (node_communities[current_node] != node_communities[next_node]) {
            int current_community = node_communities[current_node];
            int next_community = node_communities[next_node];
            printf("current_community: %d, next_community: %d\n", current_community, next_community);

            // 次のコミュニティのグループを取得--ファイル中で該当グループを探索
            //ここから二つのテーブルを参照して行う
            for (auto& group : community_groups[next_community]) {
                printf("group: %d\n", group.first);
                if (std::find(group.second.begin(), group.second.end(), current_community) != group.second.end()) {
                    // NGリストを参照
                    auto ng_list = community_ng_nodes[next_community][group.first];

                    // 次のHop先がNGノードであるかを確認
                    if (ng_list.find(next_node) != ng_list.end()) {
                        continue; // NGノードの場合は次のHopを探す
                    }
                    break; // NGノードではない場合、次のHopを許可
                }
            }
            move_count++;
        }

        path.push_back(next_node);
        current_node = next_node;
    }
    total_move += move_count;
    return path;
}



/*------------------------------------------------------------------------------------------------------------------------*/


// プログラムの実行
int main() {
    // 時間計測を開始（ナノ秒）
    auto start_time = chrono::high_resolution_clock::now();

    srand(time(nullptr));  // ランダムシードの初期化

    // グラフとコミュニティのロード
    load_graph(GRAPH_FILE);
    load_communities(COMMUNITY_FILE);

    //その他テーブルの読み込み
    load_community_groups(GROUP_PER_COMMUNITY);
    load_community_ng_nodes(NG_NODES_PER_COMMUNITY);

    int total_move = 0;
    int total_length = 0;

    // ランダムウォークを複数回実行
    for (int i = 0; i < RW_COUNT; ++i) {
        //RWの実行
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
