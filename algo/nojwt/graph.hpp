#ifndef GRAPH_HPP
#define GRAPH_HPP
#include "header.hpp"

class Graph {
public:
    void add_edge(int u, int v) {
        adj_list[u].push_back(v);
        adj_list[v].push_back(u); // 無向グラフの場合。コメントアウトで有向グラフ対応
    }

    const vector<int>& get_neighbors(int u) const {
        static const vector<int> empty;
        auto it = adj_list.find(u);
        if (it != adj_list.end()) {
            return it->second;
        }
        else {
            return empty;
        }
    }

    int size() const {
        return adj_list.size();
    }

    vector<int> get_nodes() const {
        vector<int> nodes;
        for (const auto& pair : adj_list) {
            nodes.push_back(pair.first);
        }
        return nodes;
    }

    void print_degrees() const {
        for (const auto& pair : adj_list) {
            int node = pair.first;
            int degree = pair.second.size();
            cout << "Node " << node << " has degree " << degree << endl;
        }
    }

    void write_degrees_sorted(const string& filepath) const {
        vector<pair<int, int>> degrees;
        for (const auto& pair : adj_list) {
            degrees.push_back({ pair.first, pair.second.size() });
        }
        sort(degrees.begin(), degrees.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
            return a.second < b.second;
            });

        ofstream file(filepath);
        if (!file.good()) {
            cout << "Could not open file: " << filepath << endl;
            exit(-1);
        }

        for (const auto& pair : degrees) {
            file << "Node " << pair.first << " has degree " << pair.second << endl;
        }

        file.close();
    }

private:
    unordered_map<int, vector<int> > adj_list;
};

Graph read_graph(const string& filepath);

#endif //GRAPH_HPP