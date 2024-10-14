/*
Rwerのコンストラクタを生成するファイル
それぞれのRwerが構造体を持つことで、認証情報などを適当に持つことが可能になる
*/

#include <vector>
#include <string>

// RandomWalker構造体
struct RandomWalker
{
    int id; // 一意のID
    int next_index_;
    std::vector<int> path_;

    // 構造体を生成する
    RandomWalker(int id, int next_index, std::vector<int> path)
        : id(id), next_index_(next_index), path_(path) {}
};

// RandomWalker(int id, int ver_id, int flag, int RWer_size, int RWer_id, int RWer_life, int path_length, int reserved, int next_index)
//         : id(id), ver_id_(ver_id), flag_(flag), RWer_size_(RWer_size), RWer_id_(RWer_id), RWer_life_(RWer_life),
//         p
