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
// const std::string COMMUNITY_FILE = "./../../Louvain/community/karate.tcm";
// const std::string GRAPH_FILE = "./../../Louvain/graph/karate.gr";
// const std::string GROUP_PER_COMMUNITY = "./../create-tables/result/karate/dynamic_groups.txt";
// const std::string NG_NODES_PER_COMMUNITY = "./../create-tables/result/karate/ng_nodes.txt";

const std::string GRAPH = "METIS-fb-caltech";
const std::string COMMUNITY_FILE = "./../create-tables/result/" + GRAPH + "/community.txt";
const std::string GRAPH_FILE = "./../../Louvain/graph/fb-caltech-connected.gr";         /// ここを変更
const std::string GROUP_PER_COMMUNITY = "./../create-tables/result/" + GRAPH + "/dynamic_groups.txt";
const std::string NG_NODES_PER_COMMUNITY = "./../create-tables/result/" + GRAPH + "/ng_nodes.txt";


const double ALPHA = 0.15;
const int RW_COUNT = 1000;  // ランダムウォークの実行回数
int START_NODE = 12;         // ランダムウォークの開始ノード

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
vector<int> random_walk(int& total_move, int START_NODE, int start_community) {

    int move_count = 0;
    vector<int> path;
    int current_node = START_NODE;
    std::set <int> ng_list;
    path.push_back(current_node);
    start_community = node_communities[START_NODE];

    while ((double)rand() / RAND_MAX > ALPHA) {
        auto neighbors = graph[current_node];
        if (neighbors.empty()) {
            break;
        }

        // 隣接ノードからランダムに次のノードを選択
        int next_node;
        do {
            // 隣接ノードからランダムに次のノードを選択
            next_node = *next(neighbors.begin(), rand() % neighbors.size());

            // 自分のコミュニティ内を移動する時には、そのノードに対して移動していいのかを確かめる
            // NGリストに含まれている場合は、再度選び直す
            if (ng_list.find(next_node) != ng_list.end()) {
                std::cout << "NGなのでスキップ" << next_node << std::endl;
                next_node = current_node;  // 現在のノードに戻す
            }

        } while (ng_list.find(next_node) != ng_list.end());  // NGノードの場合、繰り返す
        //ここまで


        // 現在のノードとHop先のコミュニティが異なる場合
        //NGノードは、自分と同じコミュニティに対してしか設定されていない
        // 次のコミュニティにおいて、どのノードにアクセス可能なのかを知るためには、次のコミュニティのアクセスリストを改めて参照する必要がある
        if (node_communities[current_node] != node_communities[next_node]) {
            int current_community = node_communities[current_node];
            int next_community = node_communities[next_node];
            //始点コミュニティと移動さきコミュニティが同じ時にはアクセス権の確認なし
            if (next_community == start_community) {
                move_count++;
                // printf("skip access check\n");
                continue;
            }

            // 次のコミュニティのグループを取得--start_communityが次のコミュニティでどのような権限が与えられているのかをみる

            //ここから二つのテーブルを参照して行う
            printf("比較を開始");
            for (auto& group : community_groups[next_community]) {
                if (std::find(group.second.begin(), group.second.end(), start_community) != group.second.end()) {
                    // NGリストを参照、ここでコミュニティので更新して、次に移動するまで同じものを参照できるようにする
                    ng_list = community_ng_nodes[next_community][group.first];
                    //debug 参照したリストを出力
                    std::cout << "NG nodes for Group " << group.first << ": ";
                    for (const int node : ng_list) {
                        std::cout << node << " ";
                    }
                    std::cout << std::endl;
                    /// .debug

                    // 次のHop先がNGノードであるかを確認
                    printf("次のHop先がNGノードであるかを確認");
                    if (ng_list.find(next_node) != ng_list.end()) {
                        // std::cout << "NG node found" << next_node << ::endl;
                        //進まないようにやり直す
                        next_node = current_node;
                        printf("やり直し！");
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



void saveResultsToFile(const std::string& filePath, const std::string& results) {
    // std::ofstreamを使用してファイルを開く。ios::truncを指定して上書き。

    std::ofstream outputFile(filePath, std::ios::out | std::ios::app);

    // ファイルが正常に開けたかを確認
    if (!outputFile) {
        std::cerr << "ファイルを開くことができませんでした: " << filePath << std::endl;
        return;
    }

    // 結果をファイルに書き込む
    outputFile << results;

    // ファイルを閉じる
    outputFile.close();
}
/*------------------------------------------------------------------------------------------------------------------------*/


// プログラムの実行
int main() {
    // 時間計測を開始（ナノ秒）
    // auto start_time = chrono::high_resolution_clock::now();

    srand(time(nullptr));  // ランダムシードの初期化

    // グラフとコミュニティのロード
    load_graph(GRAPH_FILE);
    load_communities(COMMUNITY_FILE);

    //その他テーブルの読み込み
    load_community_groups(GROUP_PER_COMMUNITY);
    load_community_ng_nodes(NG_NODES_PER_COMMUNITY);
    auto start_time = chrono::high_resolution_clock::now();

    int total_move = 0;
    int total_length = 0;
    int start_community = node_communities[START_NODE];

    // ランダムウォークを複数回実行
    for (int i = 0; i < RW_COUNT; ++i) {
        //RWの実行
        vector<int> path = random_walk(total_move, START_NODE, start_community);
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



    //結果を出力する
     // 保存したい結果
    std::string results = "grouped-ng-list\n";
    results += "Average path length: " + std::to_string(average_length) + "\n";
    results += "Total moves across communities: " + std::to_string(total_move) + "\n";
    results += "Program execution time: " + std::to_string(duration) + " nanoseconds\n";

    // ファイルパス
    std::string filePath = "./../result/" + GRAPH + "/access.txt";

    // 結果をファイルに保存
    saveResultsToFile(filePath, results);

    std::cout << "結果をファイルに保存しました。" << std::endl;
    return 0;
}
