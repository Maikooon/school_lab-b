
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <cstdlib>
#include <ctime>
#include <chrono>
// #include "define_jwt.cpp"
#include <mpi.h>
#include "jwt-cpp/jwt.h"
#include <map>
#include <filesystem>  
#include <iostream>
#include <algorithm>
#include "globals.h"

using namespace std;

// const double expiration_seconds = 0; // トークンの有効期限（秒）
int expiration_milliseconds = 1000; // 1000ms = 1秒　　トークンの有効期限（マイクロ秒）


std::string generate_token(int proc_rank, int expiration_seconds, int RWer_id, string SECRET_KEY)
{

    auto now = chrono::system_clock::now();
    auto exp_time = now + std::chrono::milliseconds(expiration_milliseconds);

    // 認証する要素をつけたしたい場合にはここに加える
    auto token = jwt::create()
        .set_issuer("auth0")
        .set_type("JWT")
        //  .set_payload_claim("rank", jwt::claim(std::to_string(proc_rank)))
        .set_payload_claim("RWer_id", jwt::claim(std::to_string(RWer_id)))
        .set_expires_at(exp_time) // 有効期限を設定
        .sign(jwt::algorithm::hs256{ SECRET_KEY });

    return token;
}

// RandomWalker構造体のキャッシュを調べて、次のノードに移動するかどうかを決定する


// 特定のファイルのデータを参照して、ノードが許可されているかを確認
bool isNodeAllowed(int start_node, int start_community, int next_node, int next_community, const std::map<std::string, std::map<int, std::vector<int>>>& all_node_maps)
{
    std::string filename = "community_" + std::to_string(next_community) + "_result.txt";
    //ファイルのコミュニテイxを指定する
    auto file_it = all_node_maps.find(filename);
    if (file_it != all_node_maps.end()) {
        const std::map<int, std::vector<int>>& node_map = file_it->second;
        auto it = node_map.find(next_node);
        if (it != node_map.end()) {
            const std::vector<int>& allowed_nodes = it->second;
            if (std::find(allowed_nodes.begin(), allowed_nodes.end(), start_node) != allowed_nodes.end()) {
                std::cout << "数字 " << start_node << " はリストに存在します。\n";
                return true;
            }
            //次のノードのコミュニティが始点と同じコミュニティだったとき
            else if (next_community == start_community) {
                std::cout << "数字 " << start_node << " が移動先と同じコミュニティです。\n";
                return true;
            }
            else {
                std::cout << "数字 " << start_node << " はリストに存在しません。\n";
                return false;
            }
        }
        else {
            std::cerr << "ノードが見つかりませんでした: " << next_node << std::endl;
            return false;
        }
    }
    else {
        std::cerr << "ファイルが見つかりませんでした: " << filename << std::endl;
        return false;
    }
}


// 認証情報を検証する関数
bool authenticate_move(const RandomWalker& rwer, int start_node, int start_community, int next_node, int next_community, int proc_rank, string VERIFY_SECRET_KEY, std::string& graph_name, std::map<std::string, std::map<int, std::vector<int>>>& all_node_maps)
{
    //認証せずとも、キャッシュに一度次ホップの０ーどへの移動履歴があれば許可->デコードの必要なし
    //　ここでReturn をしておくことで、デコード処理が行われない
    if (std::find(rwer.path_.begin(), rwer.path_.end(), next_node) != rwer.path_.end()) {
        cout << "キャッシュに一度次ホップの０ーどへの移動履歴があるので許可" << endl;
        cache_use_count++;
        return true;
    }

    /// 受け取ったTOkenを出力
    std::cout << "auth Token" << rwer.token << std::endl;
    try
    {
        // トークンを検証
        auto decoded = jwt::decode(rwer.token);
        auto verifier = jwt::verify()
            .allow_algorithm(jwt::algorithm::hs256{ VERIFY_SECRET_KEY })
            .with_issuer("auth0");

        verifier.verify(decoded);

        // 有効期限の検証
        auto exp_claim = decoded.get_expires_at(); // すでに time_point 型
        auto now = std::chrono::system_clock::now();

        // debug;;comment off
        std::cout << "Current time: " << std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count() << " milliseconds since epoch" << std::endl;
        std::cout << "Token expiration time: " << std::chrono::duration_cast<std::chrono::milliseconds>(exp_claim.time_since_epoch()).count() << " milliseconds since epoch" << std::endl;

        if (now >= exp_claim)
        {
            cerr << "Token expired." << endl;
            ///グローバル変数で持って回数を数える
            return false;
        }

        // debug;;comment off
        //  トークンから経路情報と出発ノードIDを取得
         // ペイロードからクレームを取得
        auto rwer_id = decoded.get_payload_claim("RWer_id").as_string();
        // int rwer_id = std::stoi(decoded.get_payload_claim("rwer_id").as_string());
        std::cout << "rwer_id: " << rwer_id << std::endl;

        std::cout << "next node: " << next_node << std::endl;

        std::cout << "next_community " << next_community << std::endl;

        return isNodeAllowed(start_node, start_community, next_node, next_community, all_node_maps);

    }
    catch (const std::exception& e)
    {
        cerr << "Token validation failed: " << e.what() << endl;
        return false;
    }

}


