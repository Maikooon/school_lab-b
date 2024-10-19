#include <iostream>
#include <string>
#include "GraphManager.cpp"

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <directory_path>" << std::endl;
        return 1;
    }

    std::string dir_path = argv[1];
    GraphManager gm = GraphManager::init_for_espresso(dir_path);

    // 実行中のGraphManagerに関するメッセージやクエリを処理するためのロジックをここに追加できます。

    return 0;
}


// g++ main.cpp GraphManager.cpp Message.cpp Graph.cpp -o graph_manager -lzmq
// ./user 10.58.58.97

