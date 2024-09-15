/*
コンストラクタを定義はしているが、認証をしていないもの
構造体からJwtの部分を排除した

実行コマンド
g++ -std=c++11 -I../json/single_include -I../jwt-cpp/include -I/opt/homebrew/opt/openssl@3/include -L/opt/homebrew/opt/openssl@3/lib -o main-no main-no.cpp -lssl -lcrypto
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <cstdlib>
#include <ctime>
#include <chrono>

using namespace std;

// グラフの定義
unordered_map<int, unordered_set<int>> graph;
unordered_map<int, int> node_communities;

std::string OUTPUT_PATH = "./result/";
std::string COMMUNITY_PATH = "./../../Louvain/community/";
std::string GRAPH_PATH = "./../../Louvain/graph/";

// 一意のID生成関数
int generate_unique_id()
{
    static int id_counter = 0;
    auto now = std::chrono::high_resolution_clock::now();
    auto duration = now.time_since_epoch();
    int unique_id = std::chrono::duration_cast<std::chrono::milliseconds>(duration).count() + id_counter++;
    return unique_id;
}

// RandomWalker_nojwt構造体の定義
struct RandomWalker_nojwt {
    int id;
    int ver_id;
    int flag;
    int RWer_size;
    int RWer_id;
    int RWer_life;
    int path_length;
    int reserved;
    int next_index;

    RandomWalker_nojwt(int id, int ver_id, int flag, int RWer_size, int RWer_id, int RWer_life, int path_length, int reserved, int next_index)
        : id(id), ver_id(ver_id), flag(flag), RWer_size(RWer_size), RWer_id(RWer_id), RWer_life(RWer_life), path_length(path_length), reserved(reserved), next_index(next_index) {}
};

// rwの作成関数を定義
RandomWalker_nojwt create_random_walker(int ver_id, int flag, int RWer_size, int RWer_id, int RWer_life, int path_length, int reserved, int next_index)
{
    // 一意のIDを生成
    int id = generate_unique_id();
    return RandomWalker_nojwt(id, ver_id, flag, RWer_size, RWer_id, RWer_life, path_length, reserved, next_index);
}

// ランダムウォークの関数
vector<int> random_walk(int& total_move, int start_node, double ALPHA)
{
    int move_count = 0;
    vector<int> path;
    int current_node = start_node;
    path.push_back(current_node);

    while ((double)rand() / RAND_MAX > ALPHA)
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

        // コミュニティが異なる場合はメッセージを出力
        if (node_communities[current_node] != node_communities[next_node])
        {
            cout << "Node " << next_node << " (Community " << node_communities[next_node] << ") is in a different community from Node " << current_node << " (Community " << node_communities[current_node] << ")" << endl;
            move_count++;
        }

        current_node = next_node;
    }
    total_move += move_count;
    return path;
}

// 結果の出力
void output_results(int global_total, int global_total_move, const string& community_path, const string& path, long long duration)
{
    size_t last_slash_idx = community_path.find_last_of("/\\");
    string filename = community_path.substr(last_slash_idx + 1);

    size_t period_idx = filename.rfind('.');
    if (period_idx != string::npos)
    {
        filename = filename.substr(0, period_idx);
    }

    // 出力先のパスを生成
    std::string filepath = OUTPUT_PATH + filename + "/" + path;

    // 出力ファイルのストリームを開く
    std::ofstream outputFile(filepath);
    if (!outputFile.is_open())
    {
        std::cerr << "Failed to open file: " << filepath << std::endl;
        return;
    }

    double ave = static_cast<double>(global_total) / node_communities.size();
    cout << "Average length: " << ave << endl;
    outputFile << "Average length: " << ave << std::endl;

    cout << "Total length: " << global_total << endl;
    outputFile << "Total length: " << global_total << std::endl;

    cout << "Total moves across communities: " << global_total_move << endl;
    outputFile << "Total moves across communities: " << global_total_move << std::endl;

    cout << "Program execution time: " << duration << " nanoseconds" << endl;
    outputFile << "Execution time: " << duration << std::endl;

    outputFile.close();
    cout << "Result has been written to " << filepath << endl;
}

int main()
{
    // 定数設定ファイルの読み込み
    std::vector<std::string> community_file_list = {
        "ca-grqc-connected.cm",
        "cmu.cm",
        "com-amazon-connected.cm",
        "email-enron-connected.cm",
        "fb-caltech-connected.cm",
        "fb-pages-company.cm",
        "karate-graph.cm",
        "karate.tcm",
        "rt-retweet.cm",
        "simple_graph.cm",
        "soc-slashdot.cm",
        "tmp.cm"
    };

    std::vector<std::string> graph_file_list = {
        "ca-grqc-connected.gr",
        "cmu.gr",
        "com-amazon-connected.gr",
        "email-enron-connected.gr",
        "fb-caltech-connected.gr",
        "fb-pages-company.gr",
        "karate-graph.gr",
        "karate.gr",
        "rt-retweet.gr",
        "simple_graph.gr",
        "soc-slashdot.gr",
        "tmp.gr"
    };

    int graph_number;
    std::cout << "Community number: ";
    std::cin >> graph_number;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::string filename;
    std::cout << "Output file name: ";
    std::getline(std::cin, filename);

    // ファイルパスを指定
    string COMMUNITY_FILE_PATH = COMMUNITY_PATH + community_file_list[graph_number];
    string GRAPH_FILE_PATH = GRAPH_PATH + graph_file_list[graph_number];

    int total_move = 0;
    double ALPHA = 0.15;
    int total = 0;

    srand(time(nullptr)); // ランダムシードを初期化

    // エッジリストファイルとコミュニティファイルの読み込み
    ifstream communities_file(COMMUNITY_FILE_PATH);
    if (!communities_file.is_open())
    {
        cerr << "Failed to open communities file." << endl;
        return 1;
    }

    string line;
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

    ifstream edges_file(GRAPH_FILE_PATH);
    if (!edges_file.is_open())
    {
        cerr << "Failed to open edges file." << endl;
        return 1;
    }

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
    }
    edges_file.close();

    // 実行時間を計測する
    auto start_time = std::chrono::high_resolution_clock::now();

    // ランダムウォークを実行
    for (const auto& node_entry : graph)
    {
        int start_node = node_entry.first;

        RandomWalker_nojwt rwer = create_random_walker(
            /* ver_id */ 1,
            /* flag */ 0,
            /* RWer_size */ 100,
            /* RWer_id */ 1,
            /* RWer_life */ 10,
            /* path_length */ 0,
            /* reserved */ 0,
            /* next_index */ 0
        );

        vector<int> path = random_walk(total_move, start_node, ALPHA);
        total += path.size();
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    // ナノ秒単位で計測してからミリ秒に変換し、小数点付きのミリ秒として表示
    auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - start_time).count();

    // long long duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    output_results(total, total_move, COMMUNITY_FILE_PATH, filename, duration);

    return 0;
}
