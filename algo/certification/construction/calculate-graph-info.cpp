/*
グラフごとのノード数などの詳細情報をとるためのプログラム
結果はcalc.txtに格納される
g++ -std=c++11 -o all-result all-result.cpp


[計算方法]
1. フォルダを指定する
2. 指定フォルダに平均値を求めたファイル生成される
3. そのファイルを表に変換する

*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <set>
#include <string>

// それぞれのグラフの基本情報をt抽出する関数
void countNodesAndEdges(const std::string &filename, int &nodeCount, int &edgeCount)
{
    std::ifstream file(filename);
    std::string line;
    std::set<int> nodes;
    edgeCount = 0;

    if (file.is_open())
    {
        while (std::getline(file, line))
        {
            if (line.empty())
            {
                continue; // 空行をスキップ
            }

            int node1, node2;
            std::istringstream iss(line);
            iss >> node1 >> node2;

            nodes.insert(node1);
            nodes.insert(node2);
            edgeCount++;
        }
        nodeCount = nodes.size();
    }
    else
    {
        std::cerr << "Error opening file: " << filename << std::endl;
    }
}

// // 任意の文字列を取り出す関数
std::string extractBeforeExtension(const std::string &filename, const std::string &extension)
{
    std::size_t pos = filename.find(extension);
    if (pos != std::string::npos)
    {
        return filename.substr(0, pos);
    }
    return filename; // 拡張子が見つからない場合は元の文字列を返す
}

// // 既存のファイルから結果を読み取る関数
// calc.txtに格納する
int main()
{

    std::ofstream resultFile("calc.txt");
    std::string filenames[] = {
        "ca-grqc-connected.gr", "cmu.gr", "com-amazon-connected.gr",
        "email-enron-connected.gr", "fb-caltech-connected.gr",
        "fb-pages-company.gr", "fb-pages-food.gr", "karate-graph.gr",
        "karate.gr",
        "modularity.gr", "ns.gr", "prefectures.gr",
        "rt-retweet.gr", "simple_graph.gr", "soc-slashdot.gr",
        "tmp.gr", "web-polblogs.gr"};

    for (const auto &filename : filenames)
    {
        std::string GRAPH_FILE_PATH = "./../../../Louvain/graph/";
        // 出力先のファイルを指定
        // 結果を格納するファイルを開く

        // ノードの初期化
        int nodeCount = 0, edgeCount = 0;
        std::string filePath = GRAPH_FILE_PATH + filename;
        countNodesAndEdges(filePath, nodeCount, edgeCount);
        std::string graphName = extractBeforeExtension(filename, ".gr");

        // コンソールに出力
        // std::cout << "graph: " << graphName << std::endl;
        // std::cout << "Nodes: " << nodeCount << ", Edges: " << edgeCount << std::endl
        //           << std::endl;

        // ファイルに出力
        resultFile << "graph: " << graphName << std::endl;
        resultFile << "Nodes: " << nodeCount << ", Edges: " << edgeCount << std::endl
                   << std::endl;
    }

    // ファイルを閉じる
    resultFile.close();

    return 0;
}
