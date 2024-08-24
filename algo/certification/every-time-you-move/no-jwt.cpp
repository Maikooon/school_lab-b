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

//  mpic++ -std=c++11 -I../json/single_include -I../jwt-cpp/include -I/opt/homebrew/opt/openssl@3/include -L/opt/homebrew/opt/openssl@3/lib -o no-jwt no-jwt.cpp -lssl -lcrypto

// グラフの定義
unordered_map<int, unordered_set<int>> graph;
unordered_map<int, int> node_communities;

// 定数設定ファイルの読み込み
const string SECRET_KEY = "your_secret_key";
const string VERIFY_SECRET_KEY = "your_secret_key";
const int expiration_seconds = 60; // トークンの有効期限（秒

// 認証の関数/////////////////////////////////////////////////////////////////////

// グローバル変数または適切な場所にノードIDリストを定義
std::set<int> allowed_node_ids;

// debug;;簡単のため、全てのノードが許可されるように全てのノード数をカバーする配列を追加
//  コンストラクタや初期化関数内で1から100までの数字を追加
void initialize_allowed_node_ids()
{
    for (int i = 1; i <= 100000; ++i)
    {
        allowed_node_ids.insert(i);
    }
}


// トークンの生成
std::string generate_token(int proc_rank, int expiration_seconds)
{

    auto now = chrono::system_clock::now();
    auto exp_time = now + std::chrono::seconds(expiration_seconds);

    // 認証する要素をつけたしたい場合にはここに加える
    auto token = jwt::create()
        .set_issuer("auth0")
        .set_type("JWT")
        .set_payload_claim("rank", jwt::claim(std::to_string(proc_rank)))
        .set_expires_at(exp_time) // 有効期限を設定
        .sign(jwt::algorithm::hs256{ SECRET_KEY });

    return token;
}

// トークンの検証
bool validate_token(const std::string& token, int proc_rank)
{
    try
    {
        auto decoded = jwt::decode(token);
        auto verifier = jwt::verify()
            .allow_algorithm(jwt::algorithm::hs256{ VERIFY_SECRET_KEY })
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
    catch (const std::exception& e)
    {
        cerr << "Token validation failed: " << e.what() << endl;
        return false;
    }
}

///////////////////////////////////////////////////////////////////////////////////

// ランダムウォークの関数
vector<int> random_walk(int& total_move, int start_node, double ALPHA, int proc_rank)
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

        //次のノードが決まったらトークンを生成
        // std::string token = generate_token(proc_rank, expiration_seconds);


        // // コミュニティが異なる場合には
        // if (node_communities[current_node] != node_communities[next_node])
        // {
        //     // 認証情報が一致するのかどうか確認する
        //     // if (!authenticate_move(current_node, next_node, proc_rank))
        //     if (!validate_token(token, proc_rank))
        //     {
        //         // 認証が通らない場合は移動を中止
        //         cout << "Authentication failed: Node " << current_node << " attempted to move to Node " << next_node << endl;
        //         break;
        //     }
        //     else
        //     {
        //         cout << "Authentication success: Node " << current_node << " moved to Node " << next_node << endl;
        //     }
        // }

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

// 結果の出力
void output_results(int global_total, int global_total_move, const string& community_path, const string& path, long long duration)
{

    // 適切なファイル名を取得する（サブディレクトリ名に利用）
    size_t last_slash_idx = community_path.find_last_of("/\\");
    string filename = community_path.substr(last_slash_idx + 1);

    size_t period_idx = filename.rfind('.');
    if (period_idx != string::npos)
    {
        filename = filename.substr(0, period_idx);
    }

    // 出力先のパスを生成
    std::string filepath = "./nojwt-result/" + filename + "/" + path;

    // 出力ファイルのストリームを開く
    std::ofstream outputFile(filepath);
    if (!outputFile.is_open())
    {
        std::cerr << "Failed to open file: " << filepath << std::endl;
        return;
    }

    // 結果の出力
    double ave = static_cast<double>(global_total) / node_communities.size();
    cout << "Average length: " << ave << endl;
    outputFile << "Average length: " << ave << std::endl;

    cout << "Total length: " << global_total << endl;
    outputFile << "Total length: " << global_total << std::endl;

    cout << "Total moves across communities: " << global_total_move << endl;
    outputFile << "Total moves across communities: " << global_total_move << std::endl;

    cout << "Program execution time: " << duration << " milliseconds" << endl;
    outputFile << "Execution time: " << duration << std::endl;

    outputFile.close();
    cout << "Result has been written to " << filepath << endl;


}

int main(int argc, char* argv[])
{
    initialize_allowed_node_ids();
    // 定数設定ファイルの読み込み
    std::vector<std::string> community_file_list = {
        "ca-grqc-connected.cm",
        "cmu.cm",
        "com-amazon-connected.cm",
        "email-enron-connected.cm",
        "fb-caltech-connected.cm",
        "fb-pages-company.cm",
        "karate-graph.cm",
        "karate.tcm",
        "rt-retweet.cm",
        "simple_graph.cm",
        "soc-slashdot.cm" };

    std::vector<std::string> graph_file_list = {
        "ca-grqc-connected.gr",
        "cmu.gr",
        "com-amazon-connected.gr",
        "email-enron-connected.gr",
        "fb-caltech-connected.gr",
        "fb-pages-company.gr",
        "fb-pages-food.gr",
        "karate-graph.gr",
        "karate.txt",
        "rt-retweet.gr",
        "simple_graph.gr",
        "soc-slashdot.gr",
    };
    std::int16_t graph_number;
    std::cout << "Community number: ";
    std::cin >> graph_number;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::string filename;
    std::cout << "Output file name: ";
    std::getline(std::cin, filename);
    // ファイルパスを指定
    string COMMUNITY_FILE_PATH = "./../../../Louvain/community/" + community_file_list[graph_number];
    string GRAPH_FILE_PATH = "./../../../Louvain/graph/" + graph_file_list[graph_number];

    int total_move = 0;
    // αの確率
    double ALPHA = 0.85;
    int total = 0;
    // 実行時間を計測する
    auto start_time = std::chrono::high_resolution_clock::now();



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
    for (const auto& node_entry : graph)
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
    // return 0;
    if (proc_rank == 0)
    {
        output_results(global_total, global_total_move, COMMUNITY_FILE_PATH, filename, duration);
    }
    return 0;
}
