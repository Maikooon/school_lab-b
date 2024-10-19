#ifndef NODE_H
#define NODE_H

#include <unordered_map>
#include <vector>
#include <string>
#include <random>
#include <stdexcept>

class Node {
public:
    int id;
    std::unordered_map<int, Node*> adj; // 隣接ノードのマップ
    int degree;
    std::string manager; // マネージャーのIPアドレス（例: 127.0.0.1）

    Node(int id, const std::string& manager = "") : id(id), degree(0), manager(manager) {}

    // 表示用の演算子オーバーロード
    std::string to_string() const {
        return std::to_string(id);
    }

    // 隣接ノードを追加
    void add_edge(Node* node) {
        adj[node->id] = node;
        degree = adj.size(); // 隣接ノードの数を更新
    }

    // ランダムな隣接ノードを取得
    Node* get_random_adjacent() {
        if (degree == 0) {
            return this; // 隣接ノードがない場合は自分自身を返す
        }
        else {
            // ランダムに隣接ノードを選ぶ
            int index = rand() % degree;
            auto it = adj.begin();
            std::advance(it, index);
            return it->second;
        }
    }

    // 演算子オーバーロード
    bool operator==(const Node& other) const {
        return id == other.id;
    }

    // __repr__メソッドに相当
    operator std::string() const {
        return to_string();
    }
};

#endif // NODE_H
