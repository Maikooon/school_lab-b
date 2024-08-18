/*
Rwerが構造体を持って認証を行うプログラム
ここでは、Rwerの生成と同時に一意のIDとトークンを持つ構造体を生成することで、移動時に認証の検証を行うことを可能にする

create token
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJSV2VyX2lkIjoiMSIsImV4cCI6MTcyMzk3MDIwNCwiaXNzIjoiYXV0aDAifQ.QdG8wFF1nOxgXbNybc9OO5-F0POknENHirtFs7Ql538
recieced token
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJSV2VyX2lkIjoiMSIsImV4cCI6MTcyMzk2OTk4NSwiaXNzIjoiYXV0aDAifQ.0ustSRCe1-aR-zFFWGp6wNUBl7cja8KEoQPqKiCOgHg
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
#include "construction.cpp"
#include "define_jwt.cpp"
#include <mpi.h>
#include "jwt-cpp/jwt.h"

using namespace std;

// mpic++ -std=c++11 -I../json/single_include -I../jwt-cpp/include -I/opt/homebrew/opt/openssl@3/include -L/opt/homebrew/opt/openssl@3/lib -o jwt jwt.cpp -lssl -lcrypto

// グラフの定義
unordered_map<int, unordered_set<int>> graph;
unordered_map<int, int> node_communities;

// 定数設定ファイルの読み込み
const string SECRET_KEY = "your_secret_key";
const string VERIFY_SECRET_KEY = "your_secret_key";
const string COMMUNITY_FILE_PATH = "./../../../Louvain/community/karate.tcm";
const string GRAPH_FILE_PATH = "./../../../Louvain/graph/karate.txt";
const int expiration_seconds = 60; // トークンの有効期限（秒）

// 一意のID生成関数
int generate_unique_id()
{
    static int id_counter = 0;
    auto now = std::chrono::high_resolution_clock::now();
    auto duration = now.time_since_epoch();
    int unique_id = std::chrono::duration_cast<std::chrono::milliseconds>(duration).count() + id_counter++;
    return unique_id;
}

// rwの作成関数を定義
RandomWalker create_random_walker(int ver_id, int flag, int RWer_size, int RWer_id, int RWer_life, int path_length, int reserved, int next_index, int expiration_seconds)
{
    // 一意のIDを生成
    // int id = generate_unique_id();

    // ここでは上の乱数に変わり簡単のためidを固定して認証機能を確かめる
    int id = 1;
    // 全てのrw

    std::string token = generate_token(id, expiration_seconds, id, SECRET_KEY); // トークンを生成
    /// 生成したTokenをRwer構造体に格納
    // printf("Token: %s\n", token.c_str());
    return RandomWalker(id, token, ver_id, flag, RWer_size, RWer_id, RWer_life, path_length, reserved, next_index);
}

///////////////////////////////////////////////////////////////////////////////////

// ランダムウォークの関数,ここでRandomWalker &rwの中のTOkenも渡される
vector<int> random_walk(int &total_move, int start_node, double ALPHA, int proc_rank, const RandomWalker &rwer)
{
    // rwの実行を始める、TOkenの受け渡しがきちんとできているのか確認
    // 確認済み、ここまではおk
    std ::cout << "Tokenの受け渡しを" << rwer.token << std::endl;
    int move_count = 0;
    vector<int> path;
    int current_node = start_node;
    path.push_back(current_node);

    while ((double)rand() / RAND_MAX > ALPHA)
    {
        // 隣接ノードのリストを取得
        auto neighbors = graph[current_node];
        if (neighbors.empty())
        {
            break;
        }

        // 次のノードをランダムに選択
        int next_node = *next(neighbors.begin(), rand() % neighbors.size());

        // コミュニティが異なる場合には
        if (node_communities[current_node] != node_communities[next_node])
        {
            std::cout << "コミュニティが異なるので認証を行います " << next_node << std::endl;

            // 認証情報が一致するのかどうか確認する
            if (!authenticate_move(rwer, next_node, proc_rank, VERIFY_SECRET_KEY))
            {
                // 認証が通らない場合はRwerの移動を中止
                cout << "Authentication failed: Node " << current_node << " attempted to move to Node " << next_node << endl;
                // break;
            }
            else
            {
                cout << "Authentication success: Node " << current_node << " moved to Node " << next_node << endl;
            }
        }

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
    double ALPHA = 0.85;
    int total = 0;

    srand(time(nullptr)); // ランダムシードを初期化

    int proc_rank, comm_size;
    MPI_Init(&argc, &argv);                    // MPIの初期化
    MPI_Comm_rank(MPI_COMM_WORLD, &proc_rank); // プロセスのランクを取得
    MPI_Comm_size(MPI_COMM_WORLD, &comm_size); // プロセスの総数を取得

    // エッジリストファイルの読み込みとコミュニティファイルの読み込み（rank 0のみ）
    unordered_map<int, int> community_assignment;
    if (proc_rank == 0)
    {
        // ifstream communities_file("./../../Louvain/community/fb-pages-company.cm");
        ifstream communities_file(COMMUNITY_FILE_PATH);
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
            community_assignment[node] = community % comm_size; // コミュニティをプロセスに割り当て
        }
        communities_file.close();
    }

    // コミュニティ割り当て情報を全プロセスにブロードキャスト
    int community_data_size = node_communities.size();
    MPI_Bcast(&community_data_size, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (proc_rank != 0)
    {
        node_communities.clear();
        community_assignment.clear();
    }

    for (int i = 0; i < community_data_size; ++i)
    {
        int node, community;
        if (proc_rank == 0)
        {
            node = node_communities.begin()->first;
            community = node_communities.begin()->second;
            node_communities.erase(node_communities.begin());
        }
        MPI_Bcast(&node, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&community, 1, MPI_INT, 0, MPI_COMM_WORLD);
        node_communities[node] = community;
        community_assignment[node] = community % comm_size;
    }

    // 各プロセスは自分が担当するコミュニティのノードのみを読み込む
    ifstream edges_file(GRAPH_FILE_PATH);
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
        if (community_assignment[node1] == proc_rank || community_assignment[node2] == proc_rank)
        {
            graph[node1].insert(node2);
            graph[node2].insert(node1);
        }
    }
    edges_file.close();

    // 全てのノードからRWを行う
    for (const auto &node_entry : graph)
        // すべてのノードからランダムウォークを実行
        for (const auto &node_entry : graph)
        {
            int start_node = node_entry.first;

            // RandomWalkerの生成　　
            // 一意のIDを持たせることで、行う これが生成された時点でTokeも生成される
            RandomWalker rwer = create_random_walker(
                /* ver_id */ 1,             // 適切な値に設定
                /* flag */ 0,               // 適切な値に設定
                /* RWer_size */ 100,        // 適切な値に設定
                /* RWer_id */ 1,            // 適切な値に設定
                /* RWer_life */ 10,         // 適切な値に設定
                /* path_length */ 0,        // 適切な値に設定
                /* reserved */ 0,           // 適切な値に設定
                /* next_index */ 0,         // 適切な値に設定
                /* expiration_seconds */ 60 // 適切な値に設定
            );
            // 上でrwerがTokenを持つようになる,この時点でTOkenが取得できるのか調べる
            // 検証すみ、この時点では上で生成したTokenを正しく取得することができる
            std::cout << "Recieved Token: " << rwer.token << std::endl;

            // 上で定義したRwerのRWを実行,rwerと一緒にTOkenも渡される
            vector<int> path = random_walk(total_move, start_node, ALPHA, proc_rank, rwer);
            int length = path.size();

            // パスの出力
            cout << "Process " << proc_rank << " Random walk path:";
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
    // プログラムの終了時間を記録
    auto end_time = std::chrono::high_resolution_clock::now();
    // 経過時間を計算
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    // 結果の書き込み
    std::string filename;
    std::cout << "Output file name: ";
    std::getline(std::cin, filename);

    std::string filepath = "./result/" + filename;

    // 出力ファイルのストリームを開く
    std::ofstream outputFile(filepath);
    if (!outputFile.is_open())
    {
        std::cerr << "Failed to open file: " << filepath << std::endl;
        return 1;
    }

    // 結果の出力
    if (proc_rank == 0)
    {
        double ave = static_cast<double>(global_total) / node_communities.size();
        // 平均経路長、rwの正当性を確認
        cout << "Average length: " << ave << endl;
        outputFile << "Average length: " << ave << std::endl;
        // 平均経路長＊ノード数＝全体の経路長
        cout << "Total length: " << global_total << endl;
        outputFile << "Total length: " << global_total << std::endl;
        // 異なるコミュニティ間の移動数
        cout << "Total moves across communities: " << global_total_move << endl;
        outputFile << "Total moves across communities: " << global_total_move << std::endl;
    }

    MPI_Finalize(); // MPIの終了

    cout << "Program execution time: " << duration << " milliseconds" << endl;
    outputFile << "execution time: " << duration << std::endl;

    // ファイルを閉じる
    outputFile.close();
    std::cout << "Result has been written to " << filename << std::endl;

    return 0;
}
