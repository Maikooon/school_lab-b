#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <random>
#include <ctime>
#include <queue>
#include <mpi.h>

#define TAG_MOVE 0

// ファイルからコミュニティデータを読み込み
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
        G[node2].push_back(node1); // Assuming undirected graph
    }
    return G;
}

// Function to perform the required check during random walk
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

// Perform PPR and check transitions
void personalized_pagerank_with_checks(int rank, int size, const std::unordered_map<int, std::vector<int>> &G, const std::unordered_map<int, std::unordered_set<int>> &communities, double alpha = 0.6, int max_steps = 100)
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
            std::tie(current_node, current_community) = perform_check_and_walk(current_node, current_community, communities, G);

            // ノードが移動したプロセスが現在のプロセスとは異なる場合→認証は必要ないので今回はコメントアウト
            if (current_community % size != rank)
            {
                int dest = current_community % size;
                MPI_Send(&current_node, 1, MPI_INT, dest, TAG_MOVE, MPI_COMM_WORLD);
                MPI_Send(&current_community, 1, MPI_INT, dest, TAG_MOVE, MPI_COMM_WORLD);
                // std::cout << "Rwer move from community " << current_community << " to community " << current_community << " (sent to server " << dest << ")" << std::endl;
                break;
            }
        }
    }
}

int main(int argc, char *argv[])
{
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // グラフデータの読み込み
    auto G = read_graph("./dataset/karate.txt");

    // コミュニティデータの読み込み
    auto communities = read_communities("./dataset/karate.tcm");

    // PPR with checksの実行
    personalized_pagerank_with_checks(rank, size, G, communities);

    MPI_Finalize();
    return 0;
}
