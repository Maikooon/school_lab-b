/**
    こちらの票を作ってから実行する
    なお、その表は丁寧に書いているNGノード表からのみ作成できるので注意

    実行コマンド
    g++ -std=c++11 nogroup-main.cpp -o nogroup
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
#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <set>
#include <string>


// グローバル変数の初期
using namespace std;
#include <map>
#include <set>



// グローバル変数の定義
// グローバル変数の定義
const std::string GRAPH = std::getenv("GRAPH") ? std::getenv("GRAPH") : "ng_0.05/METIS-karate";
const std::string GRAPH_NAME = std::getenv("GRAPH_NAME") ? std::getenv("GRAPH_NAME") : "karate";
const int ALLNODE = std::getenv("ALLNODE") ? std::stoi(std::getenv("ALLNODE")) : 34;
// const std::string GRAPH = std::getenv("GRAPH") ? std::getenv("GRAPH") : "ng_0.1/METIS-karate";
// const std::string GRAPH_NAME = std::getenv("GRAPH_NAME") ? std::getenv("GRAPH_NAME") : "karate";
// const int ALLNODE = std::getenv("ALLNODE") ? std::stoi(std::getenv("ALLNODE")) : 34;

//1. Louvainのときはこちらを使用
// const std::string COMMUNITY_FILE = "./../../Louvain/community/" + GRAPH + ".cm";

//2. Louvainではないよ時には、独自のコミュニティファイルを使用するのでこちら
const std::string COMMUNITY_FILE = "./../create-tables/result/" + GRAPH + "/node_community.txt";

const std::string GRAPH_FILE = "./../../Louvain/graph/" + GRAPH_NAME + ".gr";         /// ここを変更
const std::string NGFILE = "./../create-tables/result/" + GRAPH + "/non-group-ng-nodes.txt"; // 読み込むファイルのパス

const double ALPHA = 0.15;
const int RW_COUNT = 100;  // ランダムウォークの実行回数
// int START_NODE = 12;         // ランダムウォークの開始ノード

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

// コミュニティごとのグループとNGノードを保持するためのデータ構造
std::map<int, std::set<int>> ng_table;

// NGノードテーブルの読み込み関数
void load_ng_table(const std::string& filepath) {
    std::ifstream file(filepath);

    if (!file.is_open()) {
        std::cerr << "Error: Could not open the file at path: " << filepath << std::endl;
        return;
    }

    std::string line;
    while (std::getline(file, line)) {
        // 読み込んだ行をデバッグ出力
        // std::cout << "Read line: " << line << std::endl;

        std::istringstream iss(line);
        int community;
        std::string node_str;

        // ':' を使ってコミュニティIDとノードリストを分割する
        if (std::getline(iss, node_str, ':')) {
            community = std::stoi(node_str); // コミュニティIDを整数に変換
            // std::cout << "Parsed community: " << community << std::endl;

            // ノードをカンマで区切ってセットに追加
            while (std::getline(iss, node_str, ',')) {
                int node = std::stoi(node_str); // ノード番号を整数に変換
                ng_table[community].insert(node); // ノードをセットに追加
            }

            // 読み込んだ内容のデバッグ出力
            // std::cout << "Community " << community << " : ";
            // for (const int& n : ng_table[community]) {
            //     std::cout << n << " "; // ノードを表示
            // }
            // std::cout << std::endl;
        }
    }

    file.close();
}

// ランダムウォークを実行  
/*
    リストから次にHopするノードを探す（縦）
    あった場合は、その配列の中から、自分のさっきまでいたノードを探す
    配列の中に現在のノードがあった場合には、移動を止める、なかった場合には、次のノードに進む
    隣接ノードからランダムに次のノードを選択
*/
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

        int next_node;
        next_node = *next(neighbors.begin(), rand() % neighbors.size());
        std::cout << "start_node; next_node" << START_NODE << next_node << std::endl;

        std::string a;
        auto it = ng_table.find(next_node);  //すべてのノードに対して、NGノードの候補を探す
        printf("ここには全部到達l");

        // //次にHopするノードがNGノードの候補として上がっているのか(左一列)
        if (it != ng_table.end()) {
            std::cout << "次のノードに到達できない始点は以下 " << next_node << ": ";
            for (int num : it->second) {
                std::cout << num << " ";
                a += std::to_string(num) + " "; // ノードを文字列に追加
            }
            std::cout << std::endl;
        }
        // 次にHopするノードがNGノードの候補か確認
       // if (it != ng_table.end()) {
       //     // std::cout << "次のノードに到s達できない始点は以下 " << next_node << ": ";
       //     // std::cout << "要素数: " << it->second.size() << std::endl;
       //     bool first = true;
       //     for (int num : it->second) {
       //         if (!first) std::cout << ", ";
       //         std::cout << num;
       //         a += std::to_string(num) + ", ";
       //         first = false;
       //     }
       //     std::cout << std::endl;
       // }

       // START_NODEが文字列a(２列目以降)に含まれているか確認
        if (a.find(std::to_string(START_NODE)) != std::string::npos) {
            std::cout << "Node " << START_NODE << " is in the NG nodes for community " << current_node << std::endl;
            next_node = current_node;  // 現在のノードに戻す
            continue;
        }
        else {
            std::cout << "Node " << START_NODE << " is not in the NG nodes for community " << current_node << std::endl;
        }
        // }
        move_count++;

        path.push_back(next_node);
        current_node = next_node;
    }
    total_move += move_count;
    return path;
}



void saveResultsToFile(const std::string& filePath, const std::string& results) {
    std::ofstream outputFile(filePath, std::ios::out | std::ios::app);
    if (!outputFile) {
        std::cerr << "ファイルを開くことができませんでした: " << filePath << std::endl;
        return;
    }
    outputFile << results;
    outputFile.close();
}

// プログラムの実行
int main() {
    srand(time(nullptr));

    // グラフとコミュニティのロード
    load_graph(GRAPH_FILE);
    load_communities(COMMUNITY_FILE);

    //その他テーブルの読み込み
    load_ng_table(NGFILE);


    //時間の計測開始
    auto start_time = chrono::high_resolution_clock::now();

    int total_move = 0;
    int total_length = 0;
    // int start_community = node_communities[START_NODE];
    vector<int> start_nodes(ALLNODE);  // 1〜32までのノードをスタートノードとして設定
    for (int i = 0; i < ALLNODE; ++i) {
        start_nodes[i] = i + 1;  // ノード番号を1からスタートさせる
    }

    // 複数のスタートノードに対してランダムウォークを実行
    for (int start_node : start_nodes) {
        int start_community = node_communities[start_node];
        // ランダムウォークを複数回実行
        for (int i = 0; i < RW_COUNT; ++i) {
            //RWの実行
            vector<int> path = random_walk(total_move, start_node, start_community);
            total_length += path.size();

            // パスを出力
            // cout << "Random walk " << i + 1 << " path:";
            // for (int node : path) {
            //     cout << " " << node;
            // }
            // cout << endl;
        }
    }

    //計測終了
    auto end_time = chrono::high_resolution_clock::now();

    // 平均経路長を計算して出力
    double average_length = static_cast<double>(total_length) / RW_COUNT;
    cout << "Average path length: " << average_length / ALLNODE << endl;
    cout << "Total moves across communities: " << total_move / ALLNODE << endl;

    // 時間計測を終了して結果を表示（ナノ秒）
    auto duration = chrono::duration_cast<chrono::nanoseconds>(end_time - start_time).count();
    cout << "Program execution time: " << duration / ALLNODE << " nanoseconds" << endl;


    // 結果を出力
    std::string results = "Average path length: " + std::to_string(average_length / ALLNODE) + "\n";
    results += "Total moves across communities: " + std::to_string(total_move / ALLNODE) + "\n";
    results += "Program execution time: " + std::to_string(duration / ALLNODE) + " nanoseconds\n";
    results += "\n";

    // ファイルパス
    std::string filePath = "./../result/" + GRAPH + "/access.txt";

    // 結果をファイルに保存
    saveResultsToFile(filePath, results);

    std::cout << "結果をファイルに保存しました。" << std::endl;

    return 0;
}
