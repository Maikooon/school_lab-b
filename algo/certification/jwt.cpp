/*
単に移動の時に認証を行うプログラム
構造体を持たない
構造体などは持たない
実行される
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
#include "jwt-cpp/jwt.h"

using namespace std;

// mpic++ -std=c++11 -I../json/single_include -I../jwt-cpp/include -I/opt/homebrew/opt/openssl@3/include -L/opt/homebrew/opt/openssl@3/lib -o jwt jwt.cpp -lssl -lcrypto

// グラフの定義
unordered_map<int, unordered_set<int>> graph;
unordered_map<int, int> node_communities;

// 定数設定ファイルの読み込み
const string SECRET_KEY = "your_secret_key";
const string VERIFY_SECRET_KEY = "your_secret_key";
const string COMMUNITY_FILE_PATH = "./../../Louvain/community/karate.tcm";
const string GRAPH_FILE_PATH = "./../../Louvain/graph/karate.txt";
const int expiration_seconds = 60; // トークンの有効期限（秒）

// 認証の関数/////////////////////////////////////////////////////////////////////

// トークンの生成
std ::string generate_token(int proc_rank, int expiration_seconds)
{

    auto now = chrono::system_clock::now();
    auto exp_time = now + std ::chrono::seconds(expiration_seconds);

    // 認証する要素をつけたしたい場合にはここに加える
    auto token = jwt::create()
                     .set_issuer("auth0")
                     .set_type("JWT")
                     .set_payload_claim("rank", jwt::claim(std::to_string(proc_rank)))
                     .set_expires_at(exp_time) // 有効期限を設定

                     .sign(jwt::algorithm::hs256{SECRET_KEY});

    return token;
}

// トークンの検証
bool validate_token(const std::string &token, int proc_rank)
{
    try
    {
        auto decoded = jwt::decode(token);
        auto verifier = jwt::verify()
                            .allow_algorithm(jwt::algorithm::hs256{VERIFY_SECRET_KEY})
                            .with_issuer("auth0");

        verifier.verify(decoded);
        // 有効期限のクレームを取得
        auto exp_claim = decoded.get_expires_at(); // すでに time_point 型
        // そのまま exp_time に代入
        // auto exp_time = exp_claim;

        auto now = chrono::system_clock::now();

        if (now >= exp_claim)
        {
            cerr << "Token expired." << endl;
            return false;
        }
        return decoded.get_payload_claim("rank").as_string() == std::to_string(proc_rank);
    }
    catch (const std::exception &e)
    {
        cerr << "Token validation failed: " << e.what() << endl;
        return false;
    }
}

// 認証の関数
bool authenticate_move(int current_node, int next_node, int proc_rank)
{
    if (node_communities[current_node] != node_communities[next_node])
    {
        // 異なるコミュニティへの移動時にトークンを生成して検証
        std::string token = generate_token(proc_rank, expiration_seconds);

        if (!validate_token(token, proc_rank))
        {
            cerr << "Token validation failed for process " << proc_rank << endl;
            return false;
        }
    }
    return true; // 同じコミュニティ内の移動は許可
}

///////////////////////////////////////////////////////////////////////////////////

// ランダムウォークの関数
vector<int> random_walk(int &total_move, int start_node, double ALPHA, int proc_rank)
{
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
            // 認証情報が一致するのかどうか確認する
            if (!authenticate_move(current_node, next_node, proc_rank))
            {
                // 認証が通らない場合は移動を中止
                cout << "Authentication failed: Node " << current_node << " attempted to move to Node " << next_node << endl;
                break;
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
    {
        int start_node = node_entry.first;
        // ランダムウォークを実行
        vector<int> path = random_walk(total_move, start_node, ALPHA, proc_rank);
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
