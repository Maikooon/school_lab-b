/*
defailt のRWにテーブル参照を加えて時間を計測するもの
まだ、構造体の必要性はないので、普通のRWでテストを行う


create-talbe でNGノード用のテーブルを作ってから行う
なお、テーブルは文字がないものを作った方がいいかも
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
const std::string GRAPH = "METIS-fb-pages";
const std::string COMMUNITY_FILE = "./../create-tables/result/" + GRAPH + "/community.txt";
const std::string GRAPH_FILE = "./../../Louvain/graph/fb-pages-company.gr";         /// ここを変更
const std::string GROUP_PER_COMMUNITY = "./../create-tables/result/" + GRAPH + "/dynamic_groups.txt";
const std::string NG_NODES_PER_COMMUNITY = "./../create-tables/result/" + GRAPH + "/ng_nodes.txt";
const int ALLNODE = 14113;

// const std::string GRAPH = "METIS-fb-caltech";
// const std::string COMMUNITY_FILE = "./../create-tables/result/" + GRAPH + "/community.txt";
// const std::string GRAPH_FILE = "./../../Louvain/graph/fb-caltech-connected.gr";         /// ここを変更
// const std::string GROUP_PER_COMMUNITY = "./../create-tables/result/" + GRAPH + "/dynamic_groups.txt";
// const std::string NG_NODES_PER_COMMUNITY = "./../create-tables/result/" + GRAPH + "/ng_nodes.txt";


const double ALPHA = 0.15;
const int RW_COUNT = 1000;  // ランダムウォークの実行回数
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
        next_node = *next(neighbors.begin(), rand() % neighbors.size());
        int current_community = node_communities[current_node];
        int next_community = node_communities[next_node];

        //コミュニテイが同じ場合は、すでに読み込んであるリストを参照することで認可を行う
        if (current_community == next_community) {
            if (ng_list.find(next_node) != ng_list.end()) {
                std::cout << "NGなのでスキップ" << next_node << std::endl;
                next_node = current_node;  // 現在のノードに戻す

            }
        }
        // 現在のノードとHop先のコミュニティが異なる場合
        //NGノードは、自分と同じコミュニティに対してしか設定されていない
        // 次のコミュニティにおいて、どのノードにアクセス可能なのかを知るためには、次のコミュニティのアクセスリストを改めて参照する必要がある
        else {
            //始点コミュニティと移動先コミュニティが同じ時にはアクセス権の確認なし
            if (next_community == start_community) {     //ここはおk
                continue;
            }
            else {
                // 次のコミュニティのグループを取得--start_communityが次のコミュニティでどのような権限が与えられているのかをみる
                //ここから二つのテーブルを参照して行う
                for (auto& group : community_groups[next_community]) {
                    //dynamic-groupを参照して、、元々のコミュニティがどの権限(Group)になっているのかを確認
                    if (std::find(group.second.begin(), group.second.end(), start_community) != group.second.end()) {
                        // NGリストを参照、ここでコミュニティので更新して、次に移動するまで同じものを参照できるようにする
                        //ng_listを参照して、始点コミュニティにとってNGなノードを確認し、それが次のHop先でないことを確認
                        //次に移動するコミュニティ固有のNGリストを取得
                        ng_list = community_ng_nodes[next_community][group.first];
                        // std::cout << "NG nodes for Group " << group.first << ": ";  //ここまでもOK
                        // for (const int node : ng_list) {
                        //     std::cout << node << " ";
                        // }
                        // std::cout << std::endl;
                        printf("検査の結果大丈夫だと判断\n");

                        // 次のHop先に、出発もとのノードがアクセスできるのかを確認
                        if (ng_list.find(next_node) != ng_list.end()) {
                            // std::cout << "NG node found" << next_node << ::endl;
                            //進まないようにやり直す
                            next_node = current_node;
                            printf("やり直し！");
                            continue; // NGノードの場合は次のHopを探す
                        }
                        // break; // NGノードではない場合、次のHopを許可
                    }
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
    std::ofstream outputFile(filePath, std::ios::out | std::ios::app);
    if (!outputFile) {
        std::cerr << "ファイルを開くことができませんでした: " << filePath << std::endl;
        return;
    }
    outputFile << results;
    outputFile.close();
}
/*------------------------------------------------------------------------------------------------------------------------*/


// プログラムの実行
int main() {
    srand(time(nullptr));  // ランダムシードの初期化
    load_graph(GRAPH_FILE);
    load_communities(COMMUNITY_FILE);

    //その他テーブルの読み込み
    load_community_groups(GROUP_PER_COMMUNITY);
    load_community_ng_nodes(NG_NODES_PER_COMMUNITY);
    auto start_time = chrono::high_resolution_clock::now();

    int total_move = 0;
    int total_length = 0;
    // int start_community = node_communities[START_NODE];
    vector<int> start_nodes(ALLNODE);  // スタートノードをリストで定義

    for (int i = 0; i < ALLNODE; ++i) {
        start_nodes[i] = i + 1;  // ノード番号を1からスタートさせる
    }

    for (int start_node : start_nodes) {
        int start_community = node_communities[start_node];
        // ランダムウォークを複数回実行
        for (int i = 0; i < RW_COUNT; ++i) {
            //RWの実行
            vector<int> path = random_walk(total_move, start_node, start_community);
            total_length += path.size();
        }
    }


    // 時間計測を終了して結果を表示（ナノ秒）
    auto end_time = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::nanoseconds>(end_time - start_time).count();
    cout << "Program execution time: " << duration / ALLNODE << " nanoseconds" << endl;

    // 平均経路長を計算して出力
    double average_length = static_cast<double>(total_length) / RW_COUNT;
    cout << "Average path length: " << average_length / ALLNODE << endl;
    cout << "Total moves across communities: " << total_move / ALLNODE << endl;

    std::string results = "Average path length: " + std::to_string(average_length / ALLNODE) + "\n";
    results += "Total moves across communities: " + std::to_string(total_move / ALLNODE) + "\n";
    results += "Program execution time: " + std::to_string(duration / ALLNODE) + " nanoseconds\n";
    results += "\n";

    std::string filePath = "./../result/" + GRAPH + "/group-access.txt";

    saveResultsToFile(filePath, results);
    std::cout << "結果をファイルに保存しました。" << std::endl;
    return 0;
}
