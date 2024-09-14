#include "randomwalk.hpp"
#include <cstdlib>

// ランダムウォークを行う関数
vector<int> random_walk_path(const Graph& graph, int source_node) {
    vector<int> path;
    int current_node = source_node;
    path.push_back(current_node);

    float alpha = 0.15;
    while (true) {
        if ((float)rand() / RAND_MAX < alpha) { break; }

        const vector<int>& neighbors = graph.get_neighbors(current_node);
        if (neighbors.empty()) {
            current_node = rand() % graph.size();
        }
        else {
            current_node = neighbors[rand() % neighbors.size()];
        }
        path.push_back(current_node);
    }

    return path;
}


