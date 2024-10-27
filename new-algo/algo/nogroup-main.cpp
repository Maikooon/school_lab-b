/**
    こちらの票を作ってから実行する
    なお、その表は丁寧に書いているNGノード表からのみ作成できるので注意

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
#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>

using namespace std;



// グローバル変数の定義
const std::string GRAPH = "METIS-fb-caltech";
const std::string COMMUNITY_FILE = "./../create-tables/result/" + GRAPH + "/community.txt";
const std::string GRAPH_FILE = "./../../Louvain/graph/fb-caltech-connected.gr";         /// ここを変更
const std::string NGFILE = "./../create-tables/result/" + GRAPH + "/non-group-ng-nodes.txt"; // 読み込むファイルのパス


// const std::string GRAPH = "METIS-fb-caltech";
// const std::string COMMUNITY_FILE = "./../create-tables/result/" + GRAPH + "/community.txt";
// const std::string GRAPH_FILE = "./../../Louvain/graph/fb-caltech-connected.gr";         /// ここを変更
// const std::string GROUP_PER_COMMUNITY = "./../create-tables/result/" + GRAPH + "/dynamic_groups.txt";
// const std::string NG_NODES_PER_COMMUNITY = "./../create-tables/result/" + GRAPH + "/ng_nodes.txt";
// const std::string NGFILE = "./../create-tables/result/" + GRAPH + "/non-group-ng-nodes.txt"; // 読み込むファイルのパス

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
        //ここで一回のコミュニティの移動後は、ng_list以外を参照できるようにしたい
        int next_node;
        do {
            // 隣接ノードからランダムに次のノードを選択
            next_node = *next(neighbors.begin(), rand() % neighbors.size());

            //TODO;同じコミュニティに対しては、NGに指定していないので、ような場合はないとできる
            if (ng_list.find(next_node) != ng_list.end()) {
                std::cout << "NGなのでスキップ" << next_node << std::endl;
                next_node = current_node;  // 現在のノードに戻す
            }

        } while (ng_list.find(next_node) != ng_list.end());  // NGノードの場合、繰り返す
        //ここまで

        // 現在のノードとHop先のコミュニティが異なる場合

        // リストから次にHopするノードを探す（縦）
        //あった場合は、その配列の中から、自分のさっきまでいたノードを探す
        //配列の中に現在のノードがあった場合には、移動を止める、なかった場合には、次のノードに進む
        std::cout << "start_node; next_node" << START_NODE << next_node << std::endl;

        if (node_communities[current_node] != node_communities[next_node]) {    // 次のコミュニティと現在のコミュニティが異なっていたら
            std::string a;

            auto it = ng_table.find(next_node);
            if (it != ng_table.end()) {
                std::cout << "NG nodes for node " << next_node << ": ";
                for (int num : it->second) {
                    std::cout << num << " ";
                    a += std::to_string(num) + " "; // ノードを文字列に追加
                }
                std::cout << std::endl;
            }

            // START_NODEが文字列aに含まれているか確認
            if (a.find(std::to_string(START_NODE)) != std::string::npos) {
                std::cout << "Node " << START_NODE << " is in the NG nodes for community " << current_node << std::endl;
                next_node = current_node;  // 現在のノードに戻す
                continue;
            }
            else {
                std::cout << "Node " << START_NODE << " is not in the NG nodes for community " << current_node << std::endl;
            }
        }
        move_count++;

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
    load_ng_table(NGFILE); // データを読み込む

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


    // 結果を出力する
    //  保存したい結果
    std::string results = "Average path length: " + std::to_string(average_length) + "\n";
    results += "Total moves across communities: " + std::to_string(total_move) + "\n";
    results += "Program execution time: " + std::to_string(duration) + " nanoseconds\n";
    results += "\n";

    // ファイルパス
    std::string filePath = "./../result/" + GRAPH + "/access.txt";

    // 結果をファイルに保存
    saveResultsToFile(filePath, results);

    std::cout << "結果をファイルに保存しました。" << std::endl;

    return 0;
}

