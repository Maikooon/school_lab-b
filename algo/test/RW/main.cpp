/*
7/27
    大前提となるRWのアルゴリズム
    確立αで終了し、確立１ーで隣接ノードに遷移する
    経路長の平均は1/になるので、その部分で妥当性を確認

    Louvain法でコミュニティを分割して、コミュニティ間の移動がある際に、
    移動もとと移動先を明記している

    g++ -std=c++11 ex10.cpp -o ex10
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <chrono>

using namespace std;

// グラフの定義
unordered_map<int, unordered_set<int>> graph;
unordered_map<int, int> node_communities;

// ランダムウォークの関数
vector<int> random_walk(int &total_move, int start_node, double alpha)
{
    int move_count = 0;
    vector<int> path;
    int current_node = start_node;
    path.push_back(current_node);

    while ((double)rand() / RAND_MAX > alpha)
    {
        // 隣接ノードのリストを取得
        auto neighbors = graph[current_node];
        if (neighbors.empty())
        {
            break;
        }

        // 次のノードをランダムに選択
        int next_node = *next(neighbors.begin(), rand() % neighbors.size());
        path.push_back(next_node);

        // コミュニティが異なる場合はメッセージを出力
        if (node_communities[current_node] != node_communities[next_node])
        {
            cout << "Node " << next_node << " (Community " << node_communities[next_node] << ") is in a different community from Node " << current_node << " (Community " << node_communities[current_node] << ")" << endl;
            move_count++;
        }

        current_node = next_node;
    }
    total_move += move_count;
    return path;
}

int main()
{
    // 実行時間を計測する///////////////////////////////////
    auto start_time = std::chrono::high_resolution_clock::now();
    ////////////////////////////////
    int total_move = 0;
    srand(time(nullptr)); // ランダムシードを初期化

    // エッジリストファイルの読み込み
    ifstream edges_file("./../../Louvain/graph/fb-pages-company.gr");
    if (!edges_file.is_open())
    {
        cerr << "Failed to open edges file." << endl;
        return 1;
    }

    string line;
    int max_node = 0;
    while (getline(edges_file, line))
    {
        if (line.empty())
            continue;
        istringstream iss(line);
        int node1, node2;
        if (!(iss >> node1 >> node2))
        {
            cerr << "Error reading edge data." << endl;
            return 1;
        }
        graph[node1].insert(node2);
        graph[node2].insert(node1);

        // ノードの最大値を更新
        max_node = max(max_node, max(node1, node2));
    }
    edges_file.close();

    // コミュニティファイルの読み込み
    ifstream communities_file("./../../Louvain/community/fb-pages-company.cm");
    if (!communities_file.is_open())
    {
        cerr << "Failed to open communities file." << endl;
        return 1;
    }

    while (getline(communities_file, line))
    {
        if (line.empty())
            continue;
        istringstream iss(line);
        int node, community;
        if (!(iss >> node >> community))
        {
            cerr << "Error reading community data." << endl;
            return 1;
        }
        node_communities[node] = community;
    }
    communities_file.close();

    // αの確率
    double alpha = 0.85;

    int total = 0;

    for (int i = 1; i <= max_node; ++i)
    { // 1から最大ノード数までのスタートノードを試行
        // ランダムウォークの実行
        vector<int> path = random_walk(total_move, i, alpha);
        int length = path.size();

        // パスの出力
        cout << "Random walk path:";
        for (int node : path)
        {
            cout << " " << node;
        }
        cout << endl;

        total += length;
    }

    double ave = static_cast<double>(total) / static_cast<double>(max_node);
    cout << "Average length: " << ave << endl;
    cout << "Total length: " << total << endl;
    cout << "Total moves across communities: " << total_move << endl;

    // プログラムの終了時間を記録
    auto end_time = std::chrono::high_resolution_clock::now();
    // 経過時間を計算
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();
    std::cout << "Program execution time: " << duration << " milliseconds" << std::endl;

    return 0;
}
