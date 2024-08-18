#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <jwt-cpp/jwt.h>
#include <set>
using namespace std;

// mpic++ -std=c++11 -I../json/single_include -I../jwt-cpp/include -I/opt/homebrew/opt/openssl@3/include -L/opt/homebrew/opt/openssl@3/lib -o jwt jwt.cpp -lssl -lcrypto

// トークンの生成
std ::string generate_token(int proc_rank, int expiration_seconds, int RWer_id, string SECRET_KEY)
{

    auto now = chrono::system_clock::now();
    auto exp_time = now + std ::chrono::seconds(expiration_seconds);

    // 認証する要素をつけたしたい場合にはここに加える
    auto token = jwt::create()
                     .set_issuer("auth0")
                     .set_type("JWT")
                     //  .set_payload_claim("rank", jwt::claim(std::to_string(proc_rank)))
                     .set_payload_claim("RWer_id", jwt::claim(std::to_string(RWer_id)))
                     .set_expires_at(exp_time) // 有効期限を設定
                     .sign(jwt::algorithm::hs256{SECRET_KEY});

    return token;
}

// グローバル変数または適切な場所にノードIDリストを定義
std::set<int> allowed_node_ids;

// debug;;簡単のため、全てのノードが許可されるように全てのノード数をカバーする配列を追加
//  コンストラクタや初期化関数内で1から100までの数字を追加
void initialize_allowed_node_ids()
{
    for (int i = 1; i <= 100; ++i)
    {
        allowed_node_ids.insert(i);
    }
}

// 認証情報を検証する関数
bool authenticate_move(const RandomWalker &rwer, int next_node, int proc_rank, string VERIFY_SECRET_KEY)
{
    // 許可ノードのリストを初期化
    // これを呼び出さないと、許可されたノードが空になる
    initialize_allowed_node_ids();

    /// 受け取ったTOkenを出力
    std::cout << "auth Token: " << rwer.token << std::endl;
    try
    {
        // トークンを検証
        auto decoded = jwt::decode(rwer.token);
        auto verifier = jwt::verify()
                            .allow_algorithm(jwt::algorithm::hs256{VERIFY_SECRET_KEY})
                            .with_issuer("auth0");

        verifier.verify(decoded);

        // 有効期限の検証
        auto exp_claim = decoded.get_expires_at(); // すでに time_point 型
        auto now = std::chrono::system_clock::now();
        if (now >= exp_claim)
        {
            cerr << "Token expired." << endl;
            return false;
        }

        // debug;;comment off
        //  トークンから経路情報と出発ノードIDを取得
        // int rwer_id = std::stoi(decoded.get_payload_claim("rwer_id").as_string());

        std ::cout << "next node: " << next_node << std::endl;

        // 特定のノードIDリストに含まれている場合は認証を許可
        // 次に進む予定のノードが許可するノードのリストに含まれているのかどうかを確認
        if (allowed_node_ids.find(next_node) != allowed_node_ids.end())
        {
            return true;
        }
        else
        {
            cerr << "Authentication failed: Node ID not in allowed list." << endl;
            return false;
        }
    }
    catch (const std::exception &e)
    {
        cerr << "Token validation failed: " << e.what() << endl;
        return false;
    }
}
