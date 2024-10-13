#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

using namespace std;

// int YOUR_AWS_PUBLIC_IP = "3.112.51.163"; // サーバのパブリックIPアドレス

// グラフの定義
unordered_map<int, unordered_set<int>> graph;
unordered_map<int, int> node_communities;

void send_message_to_server(const string &message, const string &server_ip, int server_port)
{
    int sock = 0;
    struct sockaddr_in serv_addr;
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        cerr << "Socket creation error" << endl;
        return;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(server_port);

    if (inet_pton(AF_INET, server_ip.c_str(), &serv_addr.sin_addr) <= 0)
    {
        cerr << "Invalid address/ Address not supported" << endl;
        return;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        cerr << "Connection Failed" << endl;
        return;
    }

    // 送信タイムアウト設定
    struct timeval timeout;
    timeout.tv_sec = 5;
    timeout.tv_usec = 0;
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &timeout, sizeof(timeout));

    if (send(sock, message.c_str(), message.length(), 0) < 0)
    {
        cerr << "Send message failed" << endl;
    }
    close(sock);
}

// ランダムウォークの関数
vector<int> random_walk(int &total_move, int start_node, double alpha, const string &server_ip, int server_port)
{
    int move_count = 0;
    vector<int> path;
    int current_node = start_node;
    path.push_back(current_node);

    while ((double)rand() / RAND_MAX > alpha)
    {
        // 隣接ノードのリストを取得
        auto neighbors = graph[current_node];
        if (neighbors.empty())
        {
            break;
        }

        // 次のノードをランダムに選択
        int next_node = *next(neighbors.begin(), rand() % neighbors.size());
        path.push_back(next_node);

        // コミュニティが異なる場合はメッセージを送信
        if (node_communities[current_node] != node_communities[next_node])
        {
            stringstream ss;
            ss << "Node " << next_node << " moved from Community " << node_communities[current_node] << " to Community " << node_communities[next_node];
            string message = ss.str();
            cout << "Sending message: " << message << endl; // デバッグ用メッセージ
            send_message_to_server(message, server_ip, server_port);
            move_count++;
        }

        current_node = next_node;
    }
    total_move += move_count;
    return path;
}

int main()
{
    // 実行時間を計測する///////////////////////////////////
    auto start_time = std::chrono::high_resolution_clock::now();
    ////////////////////////////////
    int total_move = 0;
    srand(time(nullptr)); // ランダムシードを初期化

    // エッジリストファイルの読み込み
    ifstream edges_file("./../../Louvain/graph/fb-pages-company.gr");
    if (!edges_file.is_open())
    {
        cerr << "Failed to open edges file." << endl;
        return 1;
    }

    string line;
    int max_node = 0;
    while (getline(edges_file, line))
    {
        if (line.empty())
            continue;
        istringstream iss(line);
        int node1, node2;
        if (!(iss >> node1 >> node2))
        {
            cerr << "Error reading edge data." << endl;
            return 1;
        }
        graph[node1].insert(node2);
        graph[node2].insert(node1);

        // ノードの最大値を更新
        max_node = max(max_node, max(node1, node2));
    }
    edges_file.close();

    // コミュニティファイルの読み込み
    ifstream communities_file("./../../Louvain/community/fb-pages-company.cm");
    if (!communities_file.is_open())
    {
        cerr << "Failed to open communities file." << endl;
        return 1;
    }

    while (getline(communities_file, line))
    {
        if (line.empty())
            continue;
        istringstream iss(line);
        int node, community;
        if (!(iss >> node >> community))
        {
            cerr << "Error reading community data." << endl;
            return 1;
        }
        node_communities[node] = community;
    }
    communities_file.close();

    // αの確率
    double alpha = 0.85;
    string server_ip = "3.112.51.163"; // サーバのパブリックIPアドレス
    int server_port = 5000;            // サーバのポート番号

    int total = 0;

    for (int i = 1; i <= max_node; ++i)
    { // 1から最大ノード数までのスタートノードを試行
        // ランダムウォークの実行
        vector<int> path = random_walk(total_move, i, alpha, server_ip, server_port);
        int length = path.size();

        // パスの出力
        cout << "Random walk path:";
        for (int node : path)
        {
            cout << " " << node;
        }
        cout << endl;

        total += length;
    }

    double ave = static_cast<double>(total) / static_cast<double>(max_node);
    cout << "Average length: " << ave << endl;
    cout << "Total length: " << total << endl;
    cout << "Total moves across communities: " << total_move << endl;

    // プログラムの終了時間を記録
    auto end_time = std::chrono::high_resolution_clock::now();
    // 経過時間を計算
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();
    std::cout << "Program execution time: " << duration << " milliseconds" << std::endl;

    return 0;
}
