// g++ main.cpp User.cpp Message.cpp -o user -lzmq


#ifndef USER_H
#define USER_H

#include <iostream>
#include <string>
#include <zmq.hpp>
#include <queue>
#include <unordered_map>
#include <sstream>
#include "Message.cpp"

class User {
public:
    std::string ip_addr;
    int port = 10010;

    User(const std::string& ip_addr) : ip_addr(ip_addr) {}

    void send_query(const std::string& source_id, int count, const std::string& GM) {
        zmq::context_t context(1);
        zmq::socket_t sender(context, ZMQ_PUSH);
        sender.connect("tcp://" + GM + ":" + std::to_string(port));

        // メッセージを作成して送信
        Message message(source_id, count, GM, ip_addr);
        sender.send(zmq::buffer(message.to_bytes()), zmq::send_flags::none);

        sender.close();
        context.close();

        std::unordered_map<std::string, int> end_count;
        int total_count = 0;

        // レシーバーのセットアップ
        zmq::socket_t receiver(context, ZMQ_PULL);
        receiver.bind("tcp://" + ip_addr + ":" + std::to_string(port));

        std::cout << "これから送信を開始します\n";

        while (total_count < count) {
            std::cout << "Expected count: " << count << "\n";
            std::cout << "count: " << total_count << "\n";

            // パケットを受け取るまでブロック
            zmq::message_t message;
            receiver.recv(message, zmq::recv_flags::none);
            std::string rtn_bytes(static_cast<char*>(message.data()), message.size());
            std::cout << "Received: " << rtn_bytes << "\n";

            // 受信したデータを解析
            auto end_walk = Message::from_bytes(rtn_bytes);
            for (const auto& [node_id, val] : end_walk) {
                end_count[node_id] += val;
                total_count += val;
                std::cout << "count: " << total_count << "\n";
            }
        }

        std::cout << "Query solved: ";
        for (const auto& [node_id, val] : end_count) {
            std::cout << node_id << ": " << val << " ";
        }
        std::cout << "\n";

        receiver.close();
        context.close();
    }

private:
    Message create_message(const std::string& source_id, int count, const std::string& GM) {
        return Message(source_id, count, GM, ip_addr);
    }
};

#endif // USER_H
