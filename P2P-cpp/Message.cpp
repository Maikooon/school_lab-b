#ifndef MESSAGE_H
#define MESSAGE_H

#include <string>
#include <unordered_map>
#include <stdexcept>
#include <sstream>

class Message {
public:
    std::string source_id;
    int count;
    std::string GM;  // IP e.g., 127.0.0.1
    std::string user; // IP e.g., 127.0.0.1
    double alpha;

    Message(const std::string& source_id, int count, const std::string& GM, const std::string& user, double alpha = 0.2)
        : source_id(source_id), count(count), GM(GM), user(user), alpha(alpha) {}

    // 表示用の演算子オーバーロード
    std::string to_string() const {
        std::ostringstream oss;
        oss << "from: " << source_id << ", count: " << count << ", user: " << user;
        return oss.str();
    }

    // バイト列への変換
    std::string to_bytes() const {
        std::unordered_map<std::string, std::string> dict = {
            {"source_id", source_id},
            {"count", std::to_string(count)},
            {"GM", GM},
            {"user", user},
            {"alpha", std::to_string(alpha)}
        };
        std::ostringstream oss;
        oss << "{";
        for (auto it = dict.begin(); it != dict.end(); ++it) {
            oss << "\"" << it->first << "\": \"" << it->second << "\"";
            if (std::next(it) != dict.end()) {
                oss << ", ";
            }
        }
        oss << "}";
        return oss.str();
    }

    // バイト列からメッセージを生成
    static Message from_bytes(const std::string& b) {
        std::unordered_map<std::string, std::string> dic;
        std::string str = b;

        // 簡易的な文字列解析
        // {"source_id": "1", "count": "10", "GM": "127.0.0.1", "user": "127.0.0.1", "alpha": "0.2"}
        std::string key, value;
        size_t pos = 0;

        while ((pos = str.find(':')) != std::string::npos) {
            key = str.substr(1, pos - 2); // 1文字目から始め、2文字目は閉じのためのスラッシュ
            str.erase(0, pos + 2); // ":"とその後の空白を消去
            pos = str.find(',');
            if (pos == std::string::npos) {
                pos = str.find('}');
            }
            value = str.substr(1, pos - 2);
            dic[key] = value;
            str.erase(0, pos + 1); // ","または"}"の後の空白を消去
        }

        return Message(dic["source_id"], std::stoi(dic["count"]), dic["GM"], dic["user"], std::stod(dic["alpha"]));
    }

    // 演算子オーバーロード
    operator std::string() const {
        return to_string();
    }
};

#endif // MESSAGE_H
