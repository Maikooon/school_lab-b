#include <iostream>
#include <string>
#include "User.cpp"

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <IP_ADDRESS>" << std::endl;
        return 1;
    }

    std::string ip_address = argv[1];
    User user(ip_address);

    // サンプルデータでクエリを送信
    user.send_query("source_id_1", 10, "127.0.0.1");  // GMのIPアドレスは適宜変更してください。

    return 0;
}

// g++ main.cpp User.cpp Message.cpp -o user -lzmq
// ./user 10.58.58.97

