
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

using namespace std;

// トークンの生成
std::string generate_token(int proc_rank, int expiration_seconds, int RWer_id, string SECRET_KEY)
{

    auto now = chrono::system_clock::now();
    auto exp_time = now + std::chrono::milliseconds(expiration_seconds);

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


// グローバル変数または適切な場所にノードIDリストを定義
// std::set<int> allowed_node_ids;

// debug;;簡単のため、全てのノードが許可されるように全てのノード数をカバーする配列を追加
//  コンストラクタや初期化関数内で1から100までの数字を追加


// 認証情報を検証する関数
bool authenticate_move(const RandomWalker& rwer, int start_node, int next_node, int next_community, int proc_rank, string VERIFY_SECRET_KEY, std::string& graph_name, std::map<std::string, std::map<int, std::vector<int>>>& all_node_maps)
{
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
            // count_token_expired++;
            return false;
        }

        // debug;;comment off
        //  トークンから経路情報と出発ノードIDを取得
         // ペイロードからクレームを取得
        auto rwer_id = decoded.get_payload_claim("RWer_id").as_string();
        // int rwer_id = std::stoi(decoded.get_payload_claim("rwer_id").as_string());
        std::cout << "rwer_id: " << rwer_id << std::endl;

        std::cout << "next node: " << next_node << std::endl;

        // 特定のノードIDリストに含まれている場合は認証を許可
        // 次に進む予定のノードが許可するノードのリストに含まれているのかどうかを確認
        //TODO:現実に近い

        //次のノードが所属するコミュニティのファイルを読み込んで、そのファイルの中にHOP前のノードが含まれていたら許可
        //読み込むファイルは以下のフォルダに格納されている

        /*
        ここも関数にして埋め込んでしまう
        出発前のノードが自分
        */
        // return true;
        return isNodeAllowed(start_node, next_node, next_community, all_node_maps);

    }
    catch (const std::exception& e)
    {
        cerr << "Token validation failed: " << e.what() << endl;
        return false;
    }

}




