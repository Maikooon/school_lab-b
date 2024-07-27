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
#include <openssl/hmac.h>
#include <openssl/sha.h>
#include <iomanip>
#include <sstream>

using namespace std;

// グラフの定義
unordered_map<int, unordered_set<int>> graph;
unordered_map<int, int> node_communities;

// 認証の関数/////////////////////////////////////////////////////////////////////

// HOTPの生成
std::string generate_hotp(const std::string &secret, unsigned int counter)
{
    unsigned char hmac_result[SHA256_DIGEST_LENGTH];
    unsigned int len = 0;

    // HMAC-SHA-256を計算
    HMAC(EVP_sha256(), secret.c_str(), secret.length(),
         reinterpret_cast<const unsigned char *>(&counter), sizeof(counter),
         hmac_result, &len);

    // ダイジェストを整数に変換
    uint32_t offset = hmac_result[SHA256_DIGEST_LENGTH - 1] & 0xf;
    uint32_t binary = ((hmac_result[offset] & 0x7f) << 24) | ((hmac_result[offset + 1] & 0xff) << 16) | ((hmac_result[offset + 2] & 0xff) << 8) | (hmac_result[offset + 3] & 0xff);

    // OTPを生成（6桁）
    uint32_t otp = binary % 1000000;

    std::ostringstream oss;
    oss << std::setw(6) << std::setfill('0') << otp;
    return oss.str();
}

// HOTPの検証
bool validate_hotp(const std::string &secret, unsigned int counter, const std::string &otp)
{
    return generate_hotp(secret, counter) == otp;
}

// 認証の関数
bool authenticate_move(int current_node, int next_node, int proc_rank)
{
    if (node_communities[current_node] != node_communities[next_node])
    {
        // 異なるコミュニティへの移動時にOTPを生成して検証
        // プロセスランクをカウンターとして使用
        unsigned int counter = proc_rank;

        // シークレットキー（プロセスランクに基づいて変更）
        std::string secret = "secret_key_for_rank_" + std::to_string(proc_rank);

        // OTPを生成
        std::string otp = generate_hotp(secret, counter);

        // OTPの検証
        if (!validate_hotp(secret, counter, otp))
        {
            cerr << "OTP validation failed for process " << proc_rank << endl;
            return false;
        }
    }
    return true; // 同じコミュニティ内の移動は許可
}

///////////////////////////////////////////////////////////////////////////////////

// ランダムウォークの関数
vector<int> random_walk(int &total_move, int start_node, double alpha, int proc_rank)
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

        // コミュニティが異なる場合は認証を行う
        if (node_communities[current_node] != node_communities[next_node])
        {
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
    double alpha = 0.85;
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
        if (community_assignment[node1] == proc_rank || community_assignment[node2] == proc_rank)
        {
            graph[node1].insert(node2);
            graph[node2].insert(node1);
        }
    }
    edges_file.close();

    for (const auto &node_entry : graph)
    {
        int start_node = node_entry.first;
        vector<int> path = random_walk(total_move, start_node, alpha, proc_rank);
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

    // 結果の出力
    if (proc_rank == 0)
    {
        double ave = static_cast<double>(global_total) / node_communities.size();
        cout << "Average length: " << ave << endl;
        cout << "Total length: " << global_total << endl;
        cout << "Total moves across communities: " << global_total_move << endl;
    }

    MPI_Finalize(); // MPIの終了

    // プログラムの終了時間を記録
    auto end_time = std::chrono::high_resolution_clock::now();
    // 経過時間を計算
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    cout << "Program execution time: " << duration << " milliseconds" << endl;

    return 0;
}
