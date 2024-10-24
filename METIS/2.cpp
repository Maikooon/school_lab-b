#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <string>

using namespace std;

const string GRAPHNAME = "fb-pages-company";
// コミュニティごとのIPアドレスのマッピング
const unordered_map<int, string> ip_mapping = {
    {0, "10.58.60.3"},
    {1, "10.58.60.6"},
    {2, "10.58.60.11"}
};

// コミュニティ情報の読み込み
unordered_map<int, vector<int>> read_communities(const string& file_path) {
    unordered_map<int, vector<int>> communities;
    ifstream file(file_path);
    int node, community;

    while (file >> node >> community) {
        communities[community].push_back(node);
    }

    return communities;
}

// エッジ情報の読み込み
vector<pair<int, int>> read_edges(const string& file_path) {
    vector<pair<int, int>> edges;
    ifstream file(file_path);
    int node1, node2;

    while (file >> node1 >> node2) {
        edges.emplace_back(node1, node2);
    }

    return edges;
}

// IP付きのグラフを生成し、コミュニティごとにファイルに出力
void generate_and_save_ip_graph(const unordered_map<int, vector<int>>& communities, const vector<pair<int, int>>& edges) {
    unordered_map<int, vector<string>> ip_graph;

    // コミュニティ内の接続を追加
    for (const auto& [community_id, nodes] : communities) {
        for (size_t i = 0; i < nodes.size(); ++i) {
            for (size_t j = 0; j < nodes.size(); ++j) {
                if (i != j && find(edges.begin(), edges.end(), make_pair(nodes[i], nodes[j])) != edges.end()) {
                    ip_graph[community_id].emplace_back(
                        to_string(nodes[i]) + "," + to_string(nodes[j]) + "," + ip_mapping.at(community_id)
                    );
                }
            }
        }
    }

    // コミュニティ間の接続を追加
    for (const auto& [node1, node2] : edges) {
        auto community1 = communities.find(node1);
        auto community2 = communities.find(node2);

        if (community1 != communities.end() && community2 != communities.end() && community1->first != community2->first) {
            ip_graph[community1->first].emplace_back(
                to_string(node1) + "," + to_string(node2) + "," + ip_mapping.at(community2->first)
            );
            ip_graph[community2->first].emplace_back(
                to_string(node2) + "," + to_string(node1) + "," + ip_mapping.at(community1->first)
            );
        }
    }

    // コミュニティごとにファイルを書き込む
    for (const auto& [community_id, edges] : ip_graph) {
        string file_name = "./" + GRAPHNAME + "/community_" + to_string(community_id) + ".txt";
        ofstream out_file(file_name);
        for (const auto& edge : edges) {
            out_file << edge << endl; // エッジ情報をファイルに書き込み
        }
    }

    cout << "各コミュニティのファイルが生成されました。" << endl;
}

int main() {
    string community_file = "./" + GRAPHNAME + "/node_community.txt";
    string edge_file = "./../Louvain/graph/" + GRAPHNAME + ".gr";

    auto communities = read_communities(community_file);
    auto edges = read_edges(edge_file);

    // IP付きのグラフを生成し、ファイルに保存
    generate_and_save_ip_graph(communities, edges);

    return 0;
}
