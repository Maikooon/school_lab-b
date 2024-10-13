// 複数マシンでの更新は困難
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
#include <mpi.h>

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

int main(int argc, char *argv[])
{
    // 実行時間を計測する///////////////////////////////////
    auto start_time = std::chrono::high_resolution_clock::now();
    ////////////////////////////////
    int total_move = 0;
    int max_node = 0;
    srand(time(nullptr)); // ランダムシードを初期化

    int rank, size;
    MPI_Init(&argc, &argv);               // MPIの初期化
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // プロセスのランクを取得
    MPI_Comm_size(MPI_COMM_WORLD, &size); // プロセスの総数を取得

    // エッジリストファイルの読み込み（rank 0のみ）
    if (rank == 0)
    {
        ifstream edges_file("./../../Louvain/graph/fb-pages-company.gr");
        if (!edges_file.is_open())
        {
            cerr << "Failed to open edges file." << endl;
            MPI_Abort(MPI_COMM_WORLD, 1); // エラーがあればMPIを終了
        }

        string line;
        // int max_node = 0;
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
            graph[node1].insert(node2);
            graph[node2].insert(node1);

            // ノードの最大値を更新
            max_node = max(max_node, max(node1, node2));
        }
        printf("max_node %d\n", max_node);
        edges_file.close();

        // ノードの最大値を全プロセスにブロードキャスト
        MPI_Bcast(&max_node, 1, MPI_INT, 0, MPI_COMM_WORLD);

        // コミュニティファイルの読み込み（rank 0のみ）
        ifstream communities_file("./../../Louvain/community/fb-pages-company.cm");
        if (!communities_file.is_open())
        {
            cerr << "Failed to open communities file." << endl;
            MPI_Abort(MPI_COMM_WORLD, 1); // エラーがあればMPIを終了
        }

        string comm_line;
        while (getline(communities_file, comm_line))
        {
            if (comm_line.empty())
                continue;
            istringstream iss(comm_line);
            int node, community;
            if (!(iss >> node >> community))
            {
                cerr << "Error reading community data." << endl;
                MPI_Abort(MPI_COMM_WORLD, 1); // エラーがあればMPIを終了
            }
            node_communities[node] = community;
        }
        communities_file.close();
    }
    else
    {
        int max_node;
        MPI_Bcast(&max_node, 1, MPI_INT, 0, MPI_COMM_WORLD); // ノードの最大値を受信
    }

    // αの確率
    double alpha = 0.85;

    int total = 0;
    for (int i = rank + 1; i <= max_node; i += size)
    { // ランクに応じてスタートノードを設定し、size分だけスキップして並列処理
        if (i <= max_node)
        {
            // ランダムウォークの実行
            vector<int> path = random_walk(total_move, i, alpha);
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
    }

    // 全プロセスの結果を集約
    int global_total;
    MPI_Reduce(&total, &global_total, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    int global_total_move;
    MPI_Reduce(&total_move, &global_total_move, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0)
    {
        double ave = static_cast<double>(global_total) / static_cast<double>(max_node);
        cout << "Average length: " << ave << endl;
        cout << "Total length: " << global_total << endl;
        cout << "Total moves across communities: " << global_total_move << endl;
    }
    if (rank == 1)
    {
        double ave = static_cast<double>(global_total) / static_cast<double>(max_node);
        cout << "Average length: " << ave << endl;
        cout << "Total length: " << global_total << endl;
        cout << "Total moves across communities: " << global_total_move << endl;
    }

    MPI_Finalize(); // MPIの終了

    // プログラムの終了時間を記録
    auto end_time = std::chrono::high_resolution_clock::now();
    // 経過時間を計算
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();
    std::cout << "Program execution time: " << duration << " milliseconds" << std::endl;

    return 0;
}
