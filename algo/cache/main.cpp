/*
Rwerが構造体を持って認証を行うプログラム
ここでは、Rwerの生成と同時に一意のIDとトークンを持つ構造体を生成することで、移動時に認証の検証を行うことを可能にする
結果は、result に格納
create token
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJSV2VyX2lkIjoiMSIsImV4cCI6MTcyMzk3MDIwNCwiaXNzIjoiYXV0aDAifQ.QdG8wFF1nOxgXbNybc9OO5-F0POknENHirtFs7Ql538
recieced token
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJSV2VyX2lkIjoiMSIsImV4cCI6MTcyMzk2OTk4NSwiaXNzIjoiYXV0aDAifQ.0ustSRCe1-aR-zFFWGp6wNUBl7cja8KEoQPqKiCOgHg

mpic++ -std=c++11 -I../json/single_include -I../jwt-cpp/include -I/opt/homebrew/opt/openssl@3/include -L/opt/homebrew/opt/openssl@3/lib -o main main.cpp -lssl -lcrypto

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
// #include "define_jwt.cpp"
#include <mpi.h>
#include "jwt-cpp/jwt.h"
#include <map>
#include <filesystem>  
#include "read_data.cpp"
#include <iostream>
#include "generate_token.cpp"

using namespace std;

// グラフの定義
unordered_map<int, unordered_set<int>> graph;
unordered_map<int, int> node_communities;

const string SECRET_KEY = "your_secret_key";
const string VERIFY_SECRET_KEY = "your_secret_key";

// const double expiration_seconds = 0; // トークンの有効期限（秒）
// int expiration_milliseconds = 1000; // 1000ms = 1秒　　トークンの有効期限（マイクロ秒）
std::int16_t count_token_expired = 0;  //時間切れのトークンの数を数える

// 所要時間の内訳を調べる
//認証生成時間
double total_token_generation_time = 0;
//探索時間
double total_search_time = 0;
// トークンの検証時間
double total_token_verification_time = 0.0;

double total_token_construction_time = 0;   //構築時間
//デフォルトとの差分時間
double total_difference_time = 0;
double default_time = 28205; //soc

// // トークンの生成
// std::string generate_token(int proc_rank, int expiration_seconds, int RWer_id, string SECRET_KEY)
// {

//     auto now = chrono::system_clock::now();
//     auto exp_time = now + std::chrono::milliseconds(expiration_milliseconds);

//     // 認証する要素をつけたしたい場合にはここに加える
//     auto token = jwt::create()
//         .set_issuer("auth0")
//         .set_type("JWT")
//         //  .set_payload_claim("rank", jwt::claim(std::to_string(proc_rank)))
//         .set_payload_claim("RWer_id", jwt::claim(std::to_string(RWer_id)))
//         .set_expires_at(exp_time) // 有効期限を設定
//         .sign(jwt::algorithm::hs256{ SECRET_KEY });

//     return token;
// }

// // 認証情報を検証する関数
// bool authenticate_move(const RandomWalker& rwer, int start_node, int next_node, int next_community, int proc_rank, string VERIFY_SECRET_KEY, std::string& graph_name, std::map<std::string, std::map<int, std::vector<int>>>& all_node_maps)
// {
//     /// 受け取ったTOkenを出力
//     std::cout << "auth Token" << rwer.token << std::endl;
//     try
//     {
//         // トークンを検証
//         auto decoded = jwt::decode(rwer.token);
//         auto verifier = jwt::verify()
//             .allow_algorithm(jwt::algorithm::hs256{ VERIFY_SECRET_KEY })
//             .with_issuer("auth0");

//         verifier.verify(decoded);

//         // 有効期限の検証
//         auto exp_claim = decoded.get_expires_at(); // すでに time_point 型
//         auto now = std::chrono::system_clock::now();

//         // debug;;comment off
//         std::cout << "Current time: " << std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count() << " milliseconds since epoch" << std::endl;
//         std::cout << "Token expiration time: " << std::chrono::duration_cast<std::chrono::milliseconds>(exp_claim.time_since_epoch()).count() << " milliseconds since epoch" << std::endl;

//         if (now >= exp_claim)
//         {
//             cerr << "Token expired." << endl;
//             ///グローバル変数で持って回数を数える
//             count_token_expired++;
//             return false;
//         }

//         // debug;;comment off
//         //  トークンから経路情報と出発ノードIDを取得
//          // ペイロードからクレームを取得
//         auto rwer_id = decoded.get_payload_claim("RWer_id").as_string();
//         // int rwer_id = std::stoi(decoded.get_payload_claim("rwer_id").as_string());
//         std::cout << "rwer_id: " << rwer_id << std::endl;

//         std::cout << "next node: " << next_node << std::endl;

//         // 特定のノードIDリストに含まれている場合は認証を許可
//         // 次に進む予定のノードが許可するノードのリストに含まれているのかどうかを確認
//         //TODO:現実に近い

//         //次のノードが所属するコミュニティのファイルを読み込んで、そのファイルの中にHOP前のノードが含まれていたら許可
//         //読み込むファイルは以下のフォルダに格納されている

//         /*
//         ここも関数にして埋め込んでしまう
//         出発前のノードが自分
//         */
//         // return true;
//         return isNodeAllowed(start_node, next_node, next_community, all_node_maps);

//     }
//     catch (const std::exception& e)
//     {
//         cerr << "Token validation failed: " << e.what() << endl;
//         return false;
//     }

// }

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
    int id = generate_unique_id();
    // ここでは上の乱数に変わり簡単のためidを固定して認証機能を確かめる
    // int id = 1;

    // 実行時間を計測する
    auto start_time_generate = std::chrono::high_resolution_clock::now();
    //token生成
    std::string token = generate_token(id, expiration_seconds, id, SECRET_KEY);
    // プログラムの終了時間を記録
    auto end_time_generate = std::chrono::high_resolution_clock::now();
    // 経過時間を計算
    auto duration_generate = std::chrono::duration_cast<std::chrono::milliseconds>(end_time_generate - start_time_generate).count();
    total_token_generation_time += duration_generate;

    // std::string token = "a";
    /// 生成したTokenをRwer構造体に格納
       // printf("Token: %s\n", token.c_str());
    return RandomWalker(id, token, ver_id, flag, RWer_size, RWer_id, RWer_life, path_length, reserved, next_index);
}

///////////////////////////////////////////////////////////////////////////////////

// ランダムウォークの関数,ここでRandomWalker &rwの中のTOkenも渡される
vector<int> random_walk(int& total_move, int start_node, double ALPHA, int proc_rank, const RandomWalker& rwer, string graph_name, std::map<std::string, std::map<int, std::vector<int>>>& all_node_maps)
{
    int fail_count = 0; // 認証が期限切れになった回数をカウント
    // rwの実行を始める、TOkenの受け渡しがきちんとできているのか確認
    int move_count = 0;
    vector<int> path;
    int current_node = start_node;
    std::cout << "始点 " << start_node << std::endl;
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

        // // 実行時間を計測する
        auto start_time_verify = std::chrono::high_resolution_clock::now();

        // コミュニティが異なる場合には  今のユーザ　！＝　次のユーザ
        if (node_communities[current_node] != node_communities[next_node])
        {
            std::cout << "コミュニティが異なるので認証を行います " << next_node << std::endl;
            std::int16_t next_community = node_communities[next_node];

            //ここをコメントオフすると時間が大きく変わるのに、計測できない
            // 認証情報が一致するのかどうか確認する
            if (!authenticate_move(rwer, start_node, next_node, next_community, proc_rank, VERIFY_SECRET_KEY, graph_name, all_node_maps))
            {
                // 認証が通らない場合はRwerの移動を中止
                cout << "Authentication failed: Node " << current_node << " attempted to move to Node " << next_node << endl;
                // break;
            }
            {
                cout << "Authentication success: Node " << current_node << " moved to Node " << next_node << endl;
            }
        }
        // プログラムの終了時間を記録
        auto end_time_verify = std::chrono::high_resolution_clock::now();
        // 経過時間を計算
        auto duration_verify = std::chrono::duration_cast<std::chrono::milliseconds>(end_time_verify - start_time_verify).count();
        total_token_verification_time += duration_verify;



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
    std::cout << "total move: " << total_token_verification_time << std::endl;
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
    // std::string filepath = "./jwt-result-0.15/" + filename + "/" + path + "-time";
    std::string filepath = "./result/" + filename + "/" + path;
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

    //時間の内訳を調査する
    cout << "total token generate time; " << total_token_generation_time << std::endl;
    outputFile << "total token generate time: " << total_token_generation_time << std::endl;

    cout << "total token verification time: " << total_token_verification_time << std::endl;
    outputFile << "total token verification time: " << total_token_verification_time << std::endl;

    total_difference_time = duration - default_time - total_token_generation_time - total_token_verification_time;
    cout << "total difference time: " << total_difference_time << std::endl;
    outputFile << "total difference time: " << total_difference_time << std::endl;

    cout << "total construction time: " << total_token_construction_time << std::endl;
    outputFile << "total construction time: " << total_token_construction_time << std::endl;
    //ここまで

        //ファイルを閉じる
    outputFile.close();
    cout << "Result has been written to " << filepath << endl;


}

int main(int argc, char* argv[])
{// 許可ノードのリストを初期化
    // initialize_allowed_node_ids();

    // 定数設定ファイルの読み込み
    std::vector<std::string> community_file_list = {
        "ca-grqc-connected.cm",
        "cmu.cm",
        "com-amazon-connected.cm",
        // "email-enron-connected.cm",
        "fb-caltech-connected.cm",
        // "fb-pages-company.cm",
        "karate-graph.cm",
        "karate.cm",
        "rt-retweet.cm",
        "simple_graph.cm",
        // "soc-slashdot.cm",
        "tmp.cm" };

    std::vector<std::string> graph_file_list = {
        "ca-grqc-connected.gr",
        "cmu.gr",
        "com-amazon-connected.gr",
        // "email-enron-connected.gr",
        "fb-caltech-connected.gr",
        // "fb-pages-company.gr",
        "karate-graph.gr",
        "karate.gr",
        "rt-retweet.gr",
        "simple_graph.gr",
        // "soc-slashdot.gr",
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
    std::string graph_name = graph_file_list[graph_number];

    // string COMMUNITY_FILE_PATH = "./../../../calc-modularity/new_community/" + community_file_list[graph_number];
    string COMMUNITY_FILE_PATH = "./../../Louvain/community/" + community_file_list[graph_number];
    string GRAPH_FILE_PATH = "./../../Louvain/graph/" + graph_file_list[graph_number];

    //テーブルのファイルをすべて読み込む
    std::string name = graph_name.substr(0, graph_name.find_last_of("."));
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //  変更すること！！！！！
    std::string base_dir = "./../certification/create_table/table/" + name + "/";
    auto all_node_maps = loadAllowedNodesFromFiles(base_dir);

    // 実行時間を計測する
    auto start_time = std::chrono::high_resolution_clock::now();

    int total_move = 0;
    int invalid_move = 0;
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

        // debug
        //  上でrwerがTokenを持つようになる,この時点でTOkenが取得できるのか調べる
        //  検証すみ、この時点では上で生成したTokenを正しく取得することができる
        //  std::cout << "Recieved Token: " << rwer.token << std::endl;

        // 上で定義したRwerのRWを実行,rwerと一緒にTOkenも渡される
        vector<int> path = random_walk(total_move, start_node, ALPHA, proc_rank, rwer, graph_name, all_node_maps);
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
