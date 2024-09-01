/*
Rwerが構造体を持って認証を行うプログラム
ここでは、Rwerの生成と同時に一意のIDとトークンを持つ構造体を生成することで、移動時に認証の検証を行うことを可能にする
結果は、result に格納
create token
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJSV2VyX2lkIjoiMSIsImV4cCI6MTcyMzk3MDIwNCwiaXNzIjoiYXV0aDAifQ.QdG8wFF1nOxgXbNybc9OO5-F0POknENHirtFs7Ql538
recieced token
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJSV2VyX2lkIjoiMSIsImV4cCI6MTcyMzk2OTk4NSwiaXNzIjoiYXV0aDAifQ.0ustSRCe1-aR-zFFWGp6wNUBl7cja8KEoQPqKiCOgHg

mpic++ -std=c++11 -I../json/single_include -I../jwt-cpp/include -I/opt/homebrew/opt/openssl@3/include -L/opt/homebrew/opt/openssl@3/lib -o jwt jwt.cpp -lssl -lcrypto

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

using namespace std;
// グラフの定義
unordered_map<int, unordered_set<int>> graph;
unordered_map<int, int> node_communities;

const string SECRET_KEY = "your_secret_key";
const string VERIFY_SECRET_KEY = "your_secret_key";

// const double expiration_seconds = 0; // トークンの有効期限（秒）
int expiration_microseconds = 1000000; // 1000 = 1ミリ秒　　トークンの有効期限（マイクロ秒）
std::int16_t count_token_expired = 0;  //時間切れのトークンの数を数える
int total_token_generation_time = 0; // 合計時間


// トークンの生成
std::string generate_token(int proc_rank, int expiration_seconds, int RWer_id, string SECRET_KEY)
{

    auto now = chrono::system_clock::now();
    // auto exp_time = now + std::chrono::seconds(expiration_seconds);
    auto exp_time = now + std::chrono::microseconds(expiration_microseconds);

    // 認証する要素をつけたしたい場合にはここに加える
    auto token = jwt::create()
        .set_issuer("auth0")
        .set_type("JWT")
        //  .set_payload_claim("rank", jwt::claim(std::to_string(proc_rank)))
        .set_payload_claim("RWer_id", jwt::claim(std::to_string(RWer_id)))
        .set_expires_at(exp_time) // 有効期限を設定
        .sign(jwt::algorithm::hs256{ SECRET_KEY });

    return token;
}

// グローバル変数または適切な場所にノードIDリストを定義
std::set<int> allowed_node_ids;

// debug;;簡単のため、全てのノードが許可されるように全てのノード数をカバーする配列を追加
//  コンストラクタや初期化関数内で1から100までの数字を追加
// ノードリストをチェックする関数
bool checkNumberInList(int number, const std::vector<int>& list) {
    return std::find(list.begin(), list.end(), number) != list.end();
}

// ノードが許可されているかを確認する関数
bool isNodeAllowed(int current_node, int next_node, int next_community, const std::string& filename) {
    // ファイル名から拡張子を取り除く
    std::string name = filename.substr(0, filename.find_last_of("."));

    // ファイルパスを生成
    std::ifstream file("./../create_table/table/" + name + "/community_" + std::to_string(next_community) + "_result.txt");

    // ファイルが開けなかった場合
    if (!file.is_open()) {
        std::cerr << "ファイルを開けませんでした: " << filename << std::endl;
        return false;
    }

    std::unordered_map<int, std::vector<int>> community_map;
    std::string line;

    // ファイルからデータを読み込む
    while (std::getline(file, line)) {
        // 行の形式が [key, value1, value2, ...] であると仮定
        size_t pos = line.find('[');
        if (pos != std::string::npos) {
            line.erase(0, pos + 1); // '[' の後ろを取り出す
        }
        pos = line.find(']');
        if (pos != std::string::npos) {
            line.erase(pos); // ']' 以降を削除
        }
        std::istringstream iss(line);
        int key;
        if (iss >> key) {
            std::vector<int> values;
            int value;
            while (iss >> value) {
                values.push_back(value);
            }
            community_map[key] = values;
        }
    }

    file.close();

    // 読み込んだコミュニティの内容を確認
    std::cout << "読み込んだコミュニティの内容:" << std::endl;
    for (const auto& [community, nodes] : community_map) {
        std::cout << "コミュニティ " << community << ": [";
        for (size_t i = 0; i < nodes.size(); ++i) {
            std::cout << nodes[i];
            if (i < nodes.size() - 1) {
                std::cout << ", ";
            }
        }
        std::cout << "]" << std::endl;
    }

    // 指定されたコミュニティに対するノードリストを取得
    auto it = community_map.find(next_node);
    if (it == community_map.end()) {
        std::cerr << "コミュニティが見つかりません: " << next_node << std::endl;
        return false;
    }

    // ノードリストを取得
    const std::vector<int>& nodes = it->second;

    // current_node がノードリストに含まれているかをチェック
    return checkNumberInList(current_node, nodes);
}


// 認証情報を検証する関数
bool authenticate_move(std::string token, int current_node, int next_node, int next_community, int proc_rank, string VERIFY_SECRET_KEY, std::string& graph_name)
{
    /// 受け取ったTOkenを出力
    std::cout << "auth Token" << token << std::endl;
    try
    {
        // トークンを検証
        auto decoded = jwt::decode(token);
        auto verifier = jwt::verify()
            .allow_algorithm(jwt::algorithm::hs256{ VERIFY_SECRET_KEY })
            .with_issuer("auth0");

        verifier.verify(decoded);

        // 有効期限の検証
        auto exp_claim = decoded.get_expires_at(); // すでに time_point 型
        auto now = std::chrono::system_clock::now();

        // debug;;comment off
        std::cout << "Current time: " << std::chrono::duration_cast<std::chrono::microseconds>(now.time_since_epoch()).count() << " microseconds since epoch" << std::endl;
        std::cout << "Token expiration time: " << std::chrono::duration_cast<std::chrono::microseconds>(exp_claim.time_since_epoch()).count() << " microseconds since epoch" << std::endl;


        if (now >= exp_claim)
        {
            cerr << "Token expired." << endl;
            return false;
        }

        // debug;;comment off
        //  トークンから経路情報と出発ノードIDを取得
        // int rwer_id = std::stoi(decoded.get_payload_claim("rwer_id").as_string());

        std::cout << "next node: " << next_node << std::endl;

        // 特定のノードIDリストに含まれている場合は認証を許可
        // 次に進む予定のノードが許可するノードのリストに含まれているのかどうかを確認
        return isNodeAllowed(current_node, next_node, next_community, graph_name);
    }
    catch (const std::exception& e)
    {
        cerr << "Token validation failed: " << e.what() << endl;
        return false;
    }
}

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
    // 一意のIDを生成
    // int id = generate_unique_id();

    // ここでは上の乱数に変わり簡単のためidを固定して認証機能を確かめる
    int id = 1;
    // 全てのrw

    // std::string token = generate_token(id, expiration_seconds, id, SECRET_KEY); // トークンを生成
    /// 生成したTokenをRwer構造体に格納
    // printf("Token: %s\n", token.c_str());
    return RandomWalker_nojwt(id, ver_id, flag, RWer_size, RWer_id, RWer_life, path_length, reserved, next_index);
}

///////////////////////////////////////////////////////////////////////////////////

// ランダムウォークの関数,ここでRandomWalker &rwの中のTOkenも渡される
vector<int> random_walk(int& total_move, int start_node, double ALPHA, int proc_rank, const RandomWalker_nojwt& rwer, string graph_name)
{
    int fail_count = 0; // 認証が期限切れになった回数をカウント
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

        // トークン生成の時間計測
        auto start = std::chrono::high_resolution_clock::now();
        //次のノードが決まり次第Tokenを生成する
        std::string token = generate_token(proc_rank, expiration_microseconds, rwer.RWer_id_, SECRET_KEY);
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
        total_token_generation_time += 1; // 合計時間に加算

    std:int16_t next_community = node_communities[next_node];

        // コミュニティが異なる場合には
        if (node_communities[current_node] != node_communities[next_node])
        {
            std::cout << "コミュニティが異なるので認証を行います " << next_node << std::endl;

            // 認証情報が一致するのかどうか確認する
            if (!authenticate_move(token, current_node, next_node, next_community, proc_rank, VERIFY_SECRET_KEY, graph_name))
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

// 結果の出力
void output_results(int global_total, int global_total_move, const string& community_path, const string& path, long long duration, long long total_token_generation_time)
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
    // std::string filepath = "./result/" + filename + "/" + path + "_time_" + std::to_string(expiration_microseconds);
    std::string filepath = "./jwt-result-0.15-table/" + filename + "/" + path;

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

    outputFile << "Token generate time: " << total_token_generation_time << std::endl;

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
        "email-enron-connected.cm",
        "fb-caltech-connected.cm",
        "fb-pages-company.cm",
        "karate-graph.cm",
        "karate.tcm",
        "rt-retweet.cm",
        "simple_graph.cm",
        "soc-slashdot.cm" ,
        "tcm.cm" };

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
        "tcm.gr"
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
    string COMMUNITY_FILE_PATH = "./../../../Louvain/community/" + community_file_list[graph_number];
    string GRAPH_FILE_PATH = "./../../../Louvain/graph/" + graph_file_list[graph_number];



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

        // 上で定義したRwerのRWを実行,tokenは渡されない
        vector<int> path = random_walk(total_move, start_node, ALPHA, proc_rank, rwer, graph_name);
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
        output_results(global_total, global_total_move, COMMUNITY_FILE_PATH, filename, duration, total_token_generation_time);
    }
    return 0;
}
