/*
Mainを修正することで、複数マシンでの実行を可能に
mainに比べて、コミュニティ＝サーバ　という前提の実現が可能
これを　== dis.cpp　　と比較する
具体的な認証は関数の判定を行わない
mpic++ -std=c++11 -I../json/single_include -I../jwt-cpp/include -I/opt/homebrew/opt/openssl@3/include -L/opt/homebrew/opt/openssl@3/lib -o my_mpi_program jwt.cpp -lssl -lcrypto
によりコンパイル、
mpirun -np 4 ./main -> main.txt
により実行

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
#include <mpi.h>

using namespace std;

// グラフの定義
unordered_map<int, unordered_set<int>> graph;
unorde

    // ランダムウォークの関数--new
    /*
    !Rwerの動き
    確立αで終了して、確立１ーαで遷移するRWの実装
    */
    vector<int>
    random_walk(int &total_move, int start_node, double alpha)
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

        // コミュニティが異なる場合は認証を行う/////////////////////////////////////////////////
        if (node_communities[current_node] != node_communities[next_node])
        {
            cout << "Authentication failed: Node " << current_node << " attempted to move to Node " << next_node << endl;
            // if (!authenticate_move(current_node, next_node))
            // {
            //     // 認証が通らない場合は移動を中止
            //     cout << "Authentication failed: Node " << current_node << " attempted to move to Node " << next_node << endl;
            //     break;
            // }
            // else
            // {
            //     cout << "Authentication success: Node " << current_node << " moved to Node " << next_node << endl;
            // }
        }
        ////////////////////////////////////////////////////////////////////////////////

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

int main(int argc, char *argv[])
{
    // 実行時間を計測する
    auto start_time = std::chrono::high_resolution_clock::now();

    int total_move = 0;
    // αの確率
    double alpha = 0.85;
    int total = 0;
    srand(time(nullptr)); // ランダムシードを初期化

    int rank, size;
    MPI_Init(&argc, &argv);               // MPIの初期化
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // プロセスのランクを取得
    MPI_Comm_size(MPI_COMM_WORLD, &size); // プロセスの総数を取得

    // エッジリストファイルの読み込みとコミュニティファイルの読み込み（rank 0のみ）
    unordered_map<int, int> community_assignment;
    if (rank == 0)
    {
        ifstream communities_file("./../../Louvain/community/fb-pages-company.cm");
        if (!communities_file.is_open())
        {
            cerr << "Failed to open communities file." << endl;
            MPI_Abort(MPI_COMM_WORLD, 1); // エラーがあればMPIを終了
        }

        string line;
        while (getline(communities_file, line))
        {
            if (line.empty())
                continue;
            istringstream iss(line);
            int node, community;
            if (!(iss >> node >> community))
            {
                cerr << "Error reading community data." << endl;
                MPI_Abort(MPI_COMM_WORLD, 1); // エラーがあればMPIを終了
            }
            node_communities[node] = community;
            community_assignment[node] = community % size; // コミュニティをプロセスに割り当て
        }
        communities_file.close();
    }

    // コミュニティ割り当て情報を全プロセスにブロードキャスト
    int community_data_size = node_communities.size();
    MPI_Bcast(&community_data_size, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank != 0)
    {
        node_communities.clear();
        community_assignment.clear();
    }

    for (int i = 0; i < community_data_size; ++i)
    {
        int node, community;
        if (rank == 0)
        {
            node = node_communities.begin()->first;
            community = node_communities.begin()->second;
            node_communities.erase(node_communities.begin());
        }
        MPI_Bcast(&node, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&community, 1, MPI_INT, 0, MPI_COMM_WORLD);
        node_communities[node] = community;
        community_assignment[node] = community % size;
    }

    // 各プロセスは自分が担当するコミュニティのノードのみを読み込む
    // ifstream edges_file("./../../Louvain/graph/karate.txt");
    ifstream edges_file("./../../Louvain/graph/fb-pages-company.gr");
    if (!edges_file.is_open())
    {
        cerr << "Failed to open edges file." << endl;
        MPI_Abort(MPI_COMM_WORLD, 1); // エラーがあればMPIを終了
    }

    string line;
    while (getline(edges_file, line))
    {
        if (line.empty())
            continue;
        istringstream iss(line);
        int node1, node2;
        if (!(iss >> node1 >> node2))
        {
            cerr << "Error reading edge data." << endl;
            MPI_Abort(MPI_COMM_WORLD, 1); // エラーがあればMPIを終了
        }
        if (community_assignment[node1] == rank || community_assignment[node2] == rank)
        {
            graph[node1].insert(node2);
            graph[node2].insert(node1);
        }
    }
    edges_file.close();

    /*
    実際にRWを行う
    ここでは、前ノードからスタートさせている*/

    for (const auto &node_entry : graph)
    {
        int start_node = node_entry.first;
        vector<int> path = random_walk(total_move, start_node, alpha);
        int length = path.size();

        // パスの出力
        cout << "Process " << rank << " Random walk path:";
        for (int node : path)
        {
            cout << " " << node;
        }
        cout << endl;

        total += length;
    }

    // 全プロセスの結果を集約
    int global_total;
    MPI_Reduce(&total, &global_total, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    int global_total_move;
    MPI_Reduce(&total_move, &global_total_move, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    // if (rank == 0)
    // {
    //     double ave = static_cast<double>(global_total) / node_communities.size();
    //     cout << "Average length: " << ave << endl;
    //     cout << "Total length: " << global_total << endl;
    //     cout << "Total moves across communities: " << global_total_move << endl;
    // }

    MPI_Finalize(); // MPIの終了

    // プログラムの終了時間を記録
    auto end_time = std::chrono::high_resolution_clock::now();
    // 経過時間を計算
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    cout << "Program execution time: " << duration << " milliseconds" << endl;
    // 合計の経路長をノード数で割り、平均経路長を求める
    double ave = static_cast<double>(global_total) / node_communities.size();
    cout << "Average length: " << ave << endl;
    cout << "Total length: " << global_total << endl;
    cout << "Total moves across communities: " << global_total_move << endl;

    return 0;
}
