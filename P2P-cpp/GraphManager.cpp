#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <thread>
#include <queue>
#include <zmq.hpp>
#include <arpa/inet.h>
#include <netdb.h>
#include "Graph.cpp"  // Graphクラスのヘッダーファイル
#include "Message.cpp" // Messageクラスのヘッダーファイル

class GraphManager {
public:
    GraphManager(const std::string& id, Graph* graph, const std::string& ip_addr)
        : id(id), graph(graph), ip_addr(ip_addr), port(10010) {
        start();
    }

    static GraphManager* initForEspresso(const std::string& dir_path) {
        char hostname[1024];
        gethostname(hostname, sizeof(hostname));
        std::string host_name = hostname;
        std::string host_ip = getHostIP(host_name);
        std::string graph_txt_file = dir_path + host_name + ".txt";

        std::ifstream f(graph_txt_file);
        std::string line;
        std::unordered_map<std::string, Node*> nodes;
        std::unordered_map<std::string, std::vector<std::string>> ADJ;

        while (std::getline(f, line)) {
            std::stringstream ss(line);
            std::string edge[3];
            for (int i = 0; i < 3; ++i) {
                std::getline(ss, edge[i], ',');
            }
            std::string src = edge[0], dest = edge[1], dest_ip = edge[2];

            if (nodes.find(src) == nodes.end()) {
                nodes[src] = new Node(src, host_ip);
            }
            if (ADJ.find(src) == ADJ.end()) {
                ADJ[src] = std::vector<std::string>();
            }
            if (nodes.find(dest) == nodes.end()) {
                nodes[dest] = new Node(dest, dest_ip);
            }
            ADJ[src].push_back(dest);
        }

        f.close();

        Graph* graph = new Graph(ADJ, nodes);
        return new GraphManager(host_name, graph, host_ip);
    }

    void start() {
        std::thread thr_random_walk(&GraphManager::random_walk, this);
        thr_random_walk.detach();
        std::thread thr_notify_result(&GraphManager::notify_result, this);
        thr_notify_result.detach();
        std::thread thr_send_message(&GraphManager::send_message, this);
        thr_send_message.detach();
        std::thread thr_receive_message(&GraphManager::receive_message, this);
        thr_receive_message.detach();
        std::cout << "GraphManager started. IP addr: " << ip_addr << ", recv port: " << port << std::endl;
    }

private:
    std::string id;
    Graph* graph;
    std::string ip_addr;
    int port;
    std::queue<Message> receive_queue;
    std::queue<Message> send_queue;
    std::queue<std::pair<std::string, std::unordered_map<std::string, int>>> notify_queue;

    void random_walk() {
        while (true) {
            Message message = receive_queue.front();
            receive_queue.pop();

            // notify immediately when source is dangling node.
            if (graph->getNodes().find(message.source_id) == graph->getNodes().end()) {
                notify_queue.push({ message.user, {{message.source_id, message.count}} });
                continue;
            }
            auto end_walk = graph->random_walk(message.source_id, message.count, message.alpha);
            if (!end_walk.empty()) {
                notify_queue.push({ message.user, end_walk });
            }
            // Handle escaped walk if needed
        }
    }

    void notify_result() {
        zmq::context_t context(1);
        zmq::socket_t socket(context, ZMQ_PUSH);
        while (true) {
            auto notify = notify_queue.front();
            notify_queue.pop();
            socket.connect("tcp://" + notify.first + ":" + std::to_string(port));
            socket.send(zmq::buffer(notify.second), zmq::send_flags::none);
            std::cout << "Notified to " << notify.first << std::endl;
        }
    }

    void send_message() {
        zmq::context_t context(1);
        zmq::socket_t socket(context, ZMQ_PUSH);
        while (true) {
            Message message = send_queue.front();
            send_queue.pop();
            socket.connect("tcp://" + message.GM + ":" + std::to_string(port));
            socket.send(zmq::buffer(message), zmq::send_flags::none);
            std::cout << "Sent to " << message.GM << std::endl;
        }
    }

    void receive_message() {
        zmq::context_t context(1);
        zmq::socket_t socket(context, ZMQ_PULL);
        socket.bind("tcp://" + ip_addr + ":" + std::to_string(port));
        while (true) {
            zmq::message_t message;
            socket.recv(message);
            Message msg = Message::from_bytes(message.data());
            receive_queue.push(msg);
            std::cout << "Received message\nsource " << msg.source_id << ", count " << msg.count << std::endl;
        }
    }

    static std::string getHostIP(const std::string& host_name) {
        struct hostent* he = gethostbyname(host_name.c_str());
        if (he == nullptr) {
            perror("gethostbyname");
            return "";
        }
        struct in_addr** addr_list = (struct in_addr**)he->h_addr_list;
        return inet_ntoa(*addr_list[0]);
    }
};

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <directory_path>" << std::endl;
        return 1;
    }

    GraphManager* gm = GraphManager::initForEspresso(argv[1]);
    // Do necessary cleanup and exit
    delete gm;
    return 0;
}
