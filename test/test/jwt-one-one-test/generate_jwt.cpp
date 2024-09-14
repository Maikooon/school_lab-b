#include <iostream>
#include <fstream>
#include "jwt-cpp/jwt.h"

std::string generateJWT(uint32_t RWer_id, const std::string &secret_key)
{
    auto token = jwt::create()
                     .set_payload_claim("id", jwt::claim(std::to_string(RWer_id)))
                     .sign(jwt::algorithm::hs256{secret_key});

    // エンコードされたトークンを出力
    std::cout << "Generated JWT: " << token << std::endl;
    return token;
}

int main()
{
    uint32_t RWer_id = 12345;
    std::string secret_key = "my_secret_key";

    // トークン生成
    std::string token = generateJWT(RWer_id, secret_key);

    // トークンをファイルに保存
    std::ofstream outfile("token.txt");
    if (outfile.is_open())
    {
        outfile << token;
        outfile.close();
        std::cout << "Token saved to token.txt" << std::endl;
    }
    else
    {
        std::cerr << "Error opening file to save token." << std::endl;
    }

    return 0;
}
