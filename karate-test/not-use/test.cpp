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

using json = nlohmann::json;

// コミュニティデータの読み込み
std::unordered_map<int, std::unordered_set<int>> read_communities(const std::string &file_path)
{
    std::unordered_map<int, std::unordered_set<int>> communities;
    std::ifstream infile(file_path);
    std::string line;

    while (std::getline(infile, line))
    {
        std::istringstream iss(line);
        int node, community;
        if (iss >> node >> community)
        {
            communities[community].insert(node);
        }
    }
    return communities;
}

// グラフデータの読み込み
std::unordered_map<int, std::vector<int>> read_graph(const std::string &file_path)
{
    std::unordered_map<int, std::vector<int>> G;
    std::ifstream infile(file_path);
    int node1, node2;

    while (infile >> node1 >> node2)
    {
        G[node1].push_back(node2);
        G[node2].push_back(node1); // Undirected graph
    }
    return G;
}

// JWTトークンの生成
std::string generate_jwt(const std::string &secret, const std::string &node_info)
{
    auto token = jwt::create()
                     .set_issuer("server")
                     .set_type("JWT")
                     .set_payload_claim("node", jwt::claim(node_info))
                     .sign(jwt::algorithm::hs256{secret});
    return token;
}

// JWTトークンの検証
bool verify_jwt(const std::string &token, const std::string &secret)
{
    try
    {
        auto decoded = jwt::decode(token);
        auto verifier = jwt::verify()
                            .allow_algorithm(jwt::algorithm::hs256{secret})
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

// Rwerの移動とコミュニティの変化を検知する関数
std::pair<int, int> perform_check_and_walk(int node, int current_community, const std::unordered_map<int, std::unordered_set<int>> &communities, const std::unordered_map<int, std::vector<int>> &G)
{
    auto it = G.find(node);
    if (it == G.end() || it->second.empty())
    {
        return {node, current_community}; // Stay at the current node if no neighbors
    }

    static std::mt19937 rng(time(nullptr));
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
        return {next_node, next_community}; // Move to the new node and update the current community
    }

    return {next_node, current_community}; // Stay in the same community if no community change
}

// 各ノードに対して、PPRを実行
void personalized_pagerank_with_checks(int rank, int size, const std::unordered_map<int, std::vector<int>> &G, const std::unordered_map<int, std::unordered_set<int>> &communities, const std::string &secret, double alpha = 0.85, int max_steps = 100)
{
    for (const auto &node_entry : G)
    {
        int node = node_entry.first;
        int current_node = node;
        int current_community = -1;

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
            // Perform random walk and check for community change
            std::tie(current_node, current_community) = perform_check_and_walk(current_node, current_community, communities, G);

            // Generate JWT token based on the new community
            std::string token = generate_jwt(secret, std::to_string(current_node) + ":" + std::to_string(current_community));

            // JWTトークンの検証
            if (!verify_jwt(token, secret))
            {
                std::cout << "JWT verification failed, staying in community " << current_community << std::endl;
                break; // Optionally handle failure, e.g., retry, log, etc.
            }
            else
            {
                std::cout << "JWT verified successfully for community " << current_community << std::endl;
            }

            // If the node belongs to a different server, send a message
            if (current_community % size != rank)
            {
                int dest = current_community % size;
                MPI_Send(token.c_str(), token.size() + 1, MPI_CHAR, dest, TAG_MOVE, MPI_COMM_WORLD);
                std::cout << "Rwer move from community " << current_community << " to community " << current_community << " (sent to server " << dest << ")" << std::endl;
                break;
            }
        }
    }

    // 全てのノードのPPRが終了したことを通知
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
    MPI_Init(&argc, &argv);

    // プロセスの識別
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    std::string secret = "your_jwt_secret"; // JWTシークレットキー

    // グラフデータの読み込み
    auto G = read_graph("./dataset/karate.txt");

    // コミュニティデータの読み込み
    auto communities = read_communities("./dataset/karate.tcm");

    // PPR with checksの実行
    personalized_pagerank_with_checks(rank, size, G, communities, secret);

    // 他のサーバーからのメッセージを受信
    MPI_Status status;
    char token[256];
    bool finished = false;
    int finish_count = 0;

    printf("Server %d waiting for messages\n", rank);

    while (!finished)
    {
        MPI_Probe(MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
        if (status.MPI_TAG == TAG_MOVE)
        {
            MPI_Recv(token, 256, MPI_CHAR, MPI_ANY_SOURCE, TAG_MOVE, MPI_COMM_WORLD, &status);
            if (verify_jwt(token, secret))
            {
                std::cout << "JWT verified from server " << status.MPI_SOURCE << std::endl;
            }
            else
            {
                std::cout << "JWT verification failed from server " << status.MPI_SOURCE << std::endl;
            }
        }
        else if (status.MPI_TAG == TAG_FINISH)
        {
            MPI_Recv(nullptr, 0, MPI_CHAR, MPI_ANY_SOURCE, TAG_FINISH, MPI_COMM_WORLD, &status);
            finish_count++;
            if (finish_count == size - 1)
            {
                finished = true;
            }
        }
    }

    printf("Server %d finished receiving messages\n", rank);

    // MPI同期処理の終了
    MPI_Finalize();
    return 0;
}
