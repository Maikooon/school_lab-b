#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <random>
#include <ctime>
#include <mpi.h>
#include <jwt-cpp/jwt.h>
#include <nlohmann/json.hpp>

#define TAG_MOVE 0
#define TAG_FINISH 1

// JSON操作にはライブラリを使用
using json = nlohmann::json;

// コミュニティデータの読み込み
std::unordered_map<int, std::unordered_set<int>> read_communities(const std::string &file_path)
{
    // キーがコミュニティID、値がノードIDのunordered_set
    std::unordered_map<int, std::unordered_set<int>> communities;
    std::ifstream infile(file_path);
    std::string line;

    // 1行づつファイルの内容を読み込む
    while (std::getline(infile, line))
    {
        std::istringstream iss(line);
        int node, community;
        if (iss >> node >> community)
        {
            // ノードをそれが属するコミュニティに追加する
            communities[community].insert(node);
        }
    }
    // キーがコミュニティID、値がノードIDのunordered_setーハッシュマップを返す
    return communities;
}

// グラフデータの読み込み
std::unordered_map<int, std::vector<int>> read_graph(const std::string &file_path)
{
    std::unordered_map<int, std::vector<int>> G;
    // 分割前の全体のデータを読み込む
    std::ifstream infile(file_path);
    int node1, node2;

    while (infile >> node1 >> node2)
    {
        // 無向グラフなので、双方向にエッジが貼られる
        // ノード１の隣接リストにノード２を入れる
        G[node1].push_back(node2);
        // ノード２の隣接リストにノード１を入れる
        G[node2].push_back(node1); // Undirected graph
    }
    // 無向グラフをハッシュマップGに格納する
    return G;
}

// JWTトークンの生成
std::string generate_jwt(const std::string &secret, const std::string &node_info)
{
    auto token = jwt::create()
                     // Tokenの発行者を設定
                     .set_issuer("server")
                     //  Tokenのタイプを設定
                     .set_type("JWT")
                     //  ペイロード、具体的なデータの部分
                     // キーに対して、ノード情報を持つ情報を送る
                     .set_payload_claim("node", jwt::claim(node_info))
                     //  tokenをアルゴリズムhs256で署名する
                     .sign(jwt::algorithm::hs256{secret});
    // 生成されたJWTトークンを返す
    return token;
}

// JWTトークンの検証
// 検証するべきTokenとシークレットキーを受け取り、検証結果を返す
bool verify_jwt(const std::string &token, const std::string &secret)
{
    try
    {
        // デーコードすることで、トークンのペイロードを取得
        auto decoded = jwt::decode(token);
        // 検証のルールを設定する
        auto verifier = jwt::verify()
                            // 検証するアルゴリズムとシークレットキーを設置
                            .allow_algorithm(jwt::algorithm::hs256{secret})
                            // Tokenの発行者を設定
                            .with_issuer("server");
        verifier.verify(decoded);
        return true;
    }
    catch (const std::exception &e)
    {
        std::cerr << "JWT verification failed: " << e.what() << std::endl;
        return false;
    }
}

/*
    Rwerの移動とコミュニティの変化を検知する関数
    コミュニティが変わる場合ー次のノードと次のコミュニティ
    コミュニティが変わらない場合ー次のノードと現在のコミュニティ を返す
*/

// 各ノードに対して、PPRを実行
std::tuple<int, int, int> perform_check_and_walk(int node, int current_community, const std::unordered_map<int, std::unordered_set<int>> &communities, const std::unordered_map<int, std::vector<int>> &G, double alpha)
{
    auto it = G.find(node);
    // 隣接ノードがない場合、そのノードに留まる
    if (it == G.end() || it->second.empty())
    {
        return {node, current_community, current_community}; // Stay at the current node and community if no neighbors
    }

    static std::mt19937 rng(time(nullptr));
    std::uniform_real_distribution<double> prob_dist(0.0, 1.0);
    double prob = prob_dist(rng);

    if (prob < alpha)
    {
        return {node, current_community, current_community}; // Stop the walk with probability alpha
    }

    std::uniform_int_distribution<int> dist(0, it->second.size() - 1);
    int next_node = it->second[dist(rng)];
    int next_community = -1;

    for (const auto &community : communities)
    {
        if (community.second.find(next_node) != community.second.end())
        {
            next_community = community.first;
            break;
        }
    }

    if (next_community != -1 && next_community != current_community)
    {
        std::cout << "Rwer move from community " << current_community << " to community " << next_community << std::endl;
        return {next_node, next_community, current_community}; // Move to the new node, update the current community, and return the new community
    }

    return {next_node, current_community, current_community}; // Stay in the same community if no community change
}

// 各ノードに対して、PPRを実行
void personalized_pagerank_with_checks(int count, int rank, int size, const std::unordered_map<int, std::vector<int>> &G, const std::unordered_map<int, std::unordered_set<int>> &communities, const std::string &secret, double alpha = 0.85, int max_steps = 100)
{
    int count_move = 0;
    int count_notmove = 0;
    int jwt_verification_count = 0;

    // 全てのノードからのPPRを回す
    for (const auto &node_entry : G)
    {
        int node = node_entry.first;
        int current_node = node;
        int current_community = -1;

        // PPRの起点を決める
        for (const auto &community : communities)
        {
            if (community.second.find(node) != community.second.end())
            {
                current_community = community.first;
                break;
            }
        }

        std::cout << "Starting PPR for node " << node << " in community " << current_community << std::endl;

        for (int step = 0; step < max_steps; ++step)
        {
            int prev_community = current_community;
            std::tie(current_node, current_community, std::ignore) = perform_check_and_walk(current_node, current_community, communities, G, alpha);

            if (current_node == node)
            {
                break;
            }

            if (current_community != prev_community)
            {
                std::string token = generate_jwt(secret, std::to_string(current_node) + ":" + std::to_string(current_community));

                if (!verify_jwt(token, secret))
                {
                    std::cout << "JWT verification failed, staying in community " << prev_community << std::endl;
                    count_notmove++;
                    break;
                }
                else
                {
                    std::cout << "JWT verified successfully for community " << current_community << std::endl;
                    count_move++;
                    jwt_verification_count++;
                }

                if (current_community % size != rank)
                {
                    int dest = current_community % size;
                    MPI_Send(token.c_str(), token.size() + 1, MPI_CHAR, dest, TAG_MOVE, MPI_COMM_WORLD);
                    std::cout << "[process] Rwer move from community " << prev_community << " to community " << current_community << " (sent to server " << dest << ")" << std::endl;
                    count++;
                    break;
                }
            }
        }
    }

    printf("count move %d, not move %d\n", count_move, count_notmove);
    printf("JWT verification count %d\n", jwt_verification_count);
    printf("Total moves across servers %d\n", count);

    for (int i = 0; i < size; ++i)
    {
        if (i != rank)
        {
            MPI_Send(nullptr, 0, MPI_CHAR, i, TAG_FINISH, MPI_COMM_WORLD);
        }
    }
}

int main(int argc, char *argv[])
{
    int count = 0;
    int count_move = 0;
    int count_notmove = 0;
    MPI_Init(&argc, &argv);

    // プロセスの識別子とサイズを取得
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    std::string secret = "your_jwt_secret"; // JWTシークレットキー

    // グラフデータの読み込み
    auto G = read_graph("./dataset/karate.txt");

    // コミュニティデータの読み込み
    auto communities = read_communities("./dataset/karate.tcm");

    // PPR with checksの実行
    personalized_pagerank_with_checks(count, rank, size, G, communities, secret);

    // 他のサーバーからのメッセージを受信
    MPI_Status status;
    char token[256];
    bool finished = false;
    int finish_count = 0;

    printf("Server %d waiting for messages\n", rank);

    while (!finished)
    {
        MPI_Recv(token, 256, MPI_CHAR, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);

        if (status.MPI_TAG == TAG_MOVE)
        {
            // Handle received token
            std::string received_token(token);
            if (!verify_jwt(received_token, secret))
            {
                std::cout << "JWT verification failed on server " << rank << std::endl;
                count_notmove++;
            }
            else
            {
                std::cout << "JWT verified successfully on server " << rank << std::endl;
                count_move++;
            }
        }
        else if (status.MPI_TAG == TAG_FINISH)
        {
            finish_count++;
            if (finish_count == size - 1) // All other processes have sent the finish signal
            {
                finished = true;
            }
        }
    }

    printf("Server %d finished receiving messages\n", rank);
    printf("count = %d\n", count);
    printf("count_move = %d\n", count_move);
    printf("count_notmove = %d\n", count_notmove);

    // MPI同期処理の終了
    MPI_Finalize();
    return 0;
}
