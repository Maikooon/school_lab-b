#ifndef GRAPH_H
#define GRAPH_H

#include "Node.cpp"
#include <unordered_map>
#include <unordered_set>
#include <string>
#include <random>

class Graph {
public:
    std::unordered_map<int, Node*> nodes;
    std::unordered_map<int, Node*> outside_nodes;
    std::unordered_map<int, Node*> all_nodes;
    int node_count;

    Graph(const std::unordered_map<int, std::vector<int>>& ADJ, const std::unordered_map<int, Node*>& node_map) {
        for (const auto& [node_id, node] : node_map) {
            nodes[node_id] = node;
            all_nodes[node_id] = node;
        }

        for (const auto& [node_id, neighbors] : ADJ) {
            for (int adjacent_id : neighbors) {
                nodes[node_id]->add_edge(node_map.at(adjacent_id));
                if (node_map.find(adjacent_id) == node_map.end()) {
                    outside_nodes[adjacent_id] = nodes[node_id]->adj[adjacent_id];
                    all_nodes[adjacent_id] = node_map.at(adjacent_id);
                }
            }
        }

        node_count = nodes.size();
    }

    std::string to_string() const {
        std::string result;
        for (const auto& [id, node] : nodes) {
            result += node->to_string() + " -> { ";
            for (const auto& adj_node : node->adj) {
                result += adj_node.second->to_string() + " ";
            }
            result += "}\n";
        }
        return result;
    }

    std::pair<std::unordered_map<int, int>, std::unordered_map<int, int>> random_walk(int source_id, int count, double alpha = 0.2) {
        Node* source_node = nodes[source_id];
        std::unordered_map<int, int> end_walk;
        std::unordered_map<int, int> escaped_walk;

        for (int i = 0; i < count; ++i) {
            Node* current_node = source_node;
            while (true) {
                if (current_node->manager != source_node->manager) {
                    escaped_walk[current_node->id]++;
                    break;
                }
                if (static_cast<double>(rand()) / RAND_MAX < alpha) {
                    end_walk[current_node->id]++;
                    break;
                }
                current_node = current_node->get_random_adjacent();
            }
        }

        return { end_walk, escaped_walk };
    }
};

#endif // GRAPH_H
