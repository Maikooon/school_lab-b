#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <cstdlib>
#include <ctime>

using namespace std;

// 関数の戻り値を std::vector<int> にする
vector<int> get_adjacent_nodes(int node, const unordered_map<int, unordered_set<int>>& adj_list) {
    const unordered_set<int>& neighbors = adj_list.at(node);
    // unordered_set から vector に変換
    return vector<int>(neighbors.begin(), neighbors.end());
}

// グラフクラスの定義
class Graph {
public:
    Graph(int num_nodes) : adj_list(num_nodes) {}

    void add_edge(int node1, int node2) {
        adj_list[node1].insert(node2);
        adj_list[node2].insert(node1);
    }

    // std::vector<int> を返すように修正
    vector<int> get_neighbors(int node) const {
        const unordered_set<int>& neighbors = adj_list[node];
        // unordered_set から vector に変換
        return vector<int>(neighbors.begin(), neighbors.end());
    }

    size_t size() const {
        return adj_list.size();
    }

private:
    vector<unordered_set<int>> adj_list;
};

// コミュニティデータを読み込む関数
unordered_map<int, int> load_communities(const string& filename) {
    unordered_map<int, int> node_communities;
    ifstream communities_file(filename);
    if (!communities_file.is_open()) {
        cerr << "Failed to open communities file." << endl;
        exit(1);
    }

    string line;
    while (getline(communities_file, line)) {
        if (line.empty())
            continue;
        istringstream iss(line);
        int node, community;
        if (!(iss >> node >> community)) {
            cerr << "Error reading community data." << endl;
            exit(1);
        }
        node_communities[node] = community;
    }
    communities_file.close();
    return node_communities;
}

// エッジデータを読み込む関数
Graph load_graph(const string& filename) {
    int max_node_id = 0;
    ifstream edges_file(filename);
    if (!edges_file.is_open()) {
        cerr << "Failed to open edges file." << endl;
        exit(1);
    }

    string line;
    while (getline(edges_file, line)) {
        if (line.empty())
            continue;
        istringstream iss(line);
        int node1, node2;
        if (!(iss >> node1 >> node2)) {
            cerr << "Error reading edge data." << endl;
            exit(1);
        }
        max_node_id = max({ max_node_id, node1, node2 });
    }
    edges_file.close();

    Graph graph(max_node_id + 1);  // ノード数を動的に設定
    ifstream edges_file2(filename);
    if (!edges_file2.is_open()) {
        cerr << "Failed to open edges file." << endl;
        exit(1);
    }

    while (getline(edges_file2, line)) {
        if (line.empty())
            continue;
        istringstream iss(line);
        int node1, node2;
        if (!(iss >> node1 >> node2)) {
            cerr << "Error reading edge data." << endl;
            exit(1);
        }
        graph.add_edge(node1, node2);
    }
    edges_file2.close();
    return graph;
}

vector<int> random_walk_path(const Graph& graph, int source_node, const unordered_map<int, int>& node_communities) {
    vector<int> path;
    int current_node = source_node;
    path.push_back(current_node);

    float alpha = 0.15;
    int move_count = 0; // コミュニティ変化のカウント

    while (true) {
        if ((float)rand() / RAND_MAX < alpha) { break; }

        const vector<int>& neighbors = graph.get_neighbors(current_node);
        int next_node;
        if (neighbors.empty()) {
            next_node = rand() % graph.size();
        }
        else {
            next_node = neighbors[rand() % neighbors.size()];
        }

        // ノードがコミュニティマップに存在するか確認
        if (node_communities.find(current_node) != node_communities.end() &&
            node_communities.find(next_node) != node_communities.end()) {
            // コミュニティが異なる場合はメッセージを出力
            if (node_communities.at(current_node) != node_communities.at(next_node)) {
                cout << "Node " << next_node << " (Community " << node_communities.at(next_node)
                    << ") is in a different community from Node " << current_node
                    << " (Community " << node_communities.at(current_node) << ")" << endl;
                move_count++;
            }
        }
        else {
            // ノードがマップに存在しない場合の処理
            cerr << "Error: Node " << current_node << " or " << next_node << " is not in the community map." << endl;
            continue;
        }

        current_node = next_node;
        path.push_back(current_node);
    }

    return path;
}

int main() {
    srand(time(0));

    // コミュニティファイルとエッジファイルのパス
    string community_file_path = "./../Louvain/community/cmu.cm";
    string edge_file_path = "./../Louvain/graph/cmu.gr";

    // データの読み込み
    auto node_communities = load_communities(community_file_path);
    auto graph = load_graph(edge_file_path);

    // ノードIDを収集
    vector<int> all_nodes;
    for (int node = 0; node < graph.size(); ++node) {
        if (node_communities.find(node) != node_communities.end()) {
            all_nodes.push_back(node);
        }
    }

    // ランダムウォークの実行
    int total_length = 0;
    int num_walks = 0;

    for (int start_node : all_nodes) {
        vector<int> path = random_walk_path(graph, start_node, node_communities);
        total_length += path.size();
        num_walks++;
    }

    float average_length = (num_walks > 0) ? static_cast<float>(total_length) / num_walks : 0.0;
    cout << "Average path length: " << average_length << endl;

    return 0;
}
