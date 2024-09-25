/*
Rwerのコンストラクタを生成するファイル
それぞれのRwerが構造体を持つことで、認証情報などを適当に持つことが可能になる
*/

#include <vector>
#include <string>
// #include "define_jwt.cpp"

// RandomWalker構造体
struct RandomWalker
{
  std::string token; // トークン
  int ver_id_;
  int flag_;
  int RWer_size_;
  int RWer_id_;
  int RWer_life_;
  int path_length_at_current_host_;
  int reserved_;
  int next_index_;
  std::vector<int> path_;

  // 構造体を生成する
  RandomWalker(const std::string& token, int ver_id, int flag, int RWer_size, int RWer_id, int RWer_life, int path_length, int reserved, int next_index)
    : token(token), ver_id_(ver_id), flag_(flag), RWer_size_(RWer_size), RWer_id_(RWer_id), RWer_life_(RWer_life),
    path_length_at_current_host_(path_length), reserved_(reserved), next_index_(next_index) {}
};

// RandomWalker構造体
struct RandomWalker_nojwt
{
  int id; // 一意のID
  int ver_id_;
  int flag_;
  int RWer_size_;
  int RWer_id_;
  int RWer_life_;
  int path_length_at_current_host_;
  int reserved_;
  int next_index_;
  std::vector<int> path_;

  // 構造体を生成する
  RandomWalker_nojwt(int id, int ver_id, int flag, int RWer_size, int RWer_id, int RWer_life, int path_length, int reserved, int next_index)
    : id(id), ver_id_(ver_id), flag_(flag), RWer_size_(RWer_size), RWer_id_(RWer_id), RWer_life_(RWer_life),
    path_length_at_current_host_(path_length), reserved_(reserved), next_index_(next_index) {}
};
