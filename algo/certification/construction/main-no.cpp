/*
コンストラクタを定義はしているが、認証をしていないもの
構造体からJwtの部分を排除した
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

#include "define_jwt.cpp"
#include <mpi.h>
#include "jwt-cpp/jwt.h"
#include <map>
#include "read_data.cpp"

using namespace std;

// mpic++ -std=c++11 -I../json/single_include -I../jwt-cpp/include -I/opt/homebrew/opt/openssl@3/include -L/opt/homebrew/opt/openssl@3/lib -o main-no main-no.cpp -lssl -lcrypto

// グラフの定義
unordered_map<int, unordered_set<int>> graph;
unordered_map<int, int> node_communities;

// 定数設定ファイルの読み込み
const string SECRET_KEY = "your_secret_key";
const string VERIFY_SECRET_KEY = "your_secret_key";

const int expiration_seconds = 1; // トークンの有効期限（秒）

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
RandomWalker_nojwt create_random_walker(int ver_id, int flag, int RWer_size, int RWer_id, int RWer_life, int path_length, int reserved, int next_index, int expiration_seconds)
{

    // 認証は行わない
    //  一意のIDを生成
    //  int id = generate_unique_id();

    // // ここでは上の乱数に変わり簡単のためidを固定して認証機能を確かめる
    int id = 1;
    // // 全てのrw

    // std::string token = generate_token(id, expiration_seconds, id, SECRET_KEY); // トークンを生成
    /// 生成したTokenをRwer構造体に格納
    // printf("Token: %s\n", token.c_str());
    return RandomWalker_nojwt(id, ver_id, flag, RWer_size, RWer_id, RWer_life, path_length, reserved, next_index);
}

///////////////////////////////////////////////////////////////////////////////////

// ランダムウォークの関数,ここでRandomWalker &rwの中のTOkenも渡される
vector<int> random_walk(int& total_move, int start_node, double ALPHA, int proc_rank, const RandomWalker_nojwt& rwer)
{
    // rwの実行を始める、TOkenの受け渡しがきちんとできているのか確認
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
    std::string filepath = "./nojwt-result-0.15/" + filename + "/" + path;

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
        "soc-slashdot.cm",
        "tmp.cm" };

    std::vector<std::string> graph_file_list = {
        "ca-grqc-connected.gr",
        "cmu.gr",
        "com-amazon-connected.gr",
        "email-enron-connected.gr",
        "fb-caltech-connected.gr",
        "fb-pages-company.gr",
        "karate-graph.gr",
        "karate.gr",
        "rt-retweet.gr",
        "simple_graph.gr",
        "soc-slashdot.gr",
        "tmp.gr"
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

    // 実行時間を計測する
    auto start_time = std::chrono::high_resolution_clock::now();

    int total_move = 0;
    // αの確率
    double ALPHA = 0.15;
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

    // すべてのノードからランダムウォークを実行
    for (const auto& node_entry : graph)
    {
        int start_node = node_entry.first;

        // RandomWalkerの生成　　
        // 一意のIDを持たせることで、行う これが生成された時点でTokeも生成される
        RandomWalker_nojwt rwer = create_random_walker(
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

        // debug
        //  上でrwerがTokenを持つようになる,この時点でTOkenが取得できるのか調べる
        //  検証すみ、この時点では上で生成したTokenを正しく取得することができる
        //  std::cout << "Recieved Token: " << rwer.token << std::endl;

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

    if (proc_rank == 0)
    {
        output_results(global_total, global_total_move, COMMUNITY_FILE_PATH, filename, duration);
    }

    return 0;
}
