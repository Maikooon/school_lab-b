// config.h
#ifndef CONFIG_H
#define CONFIG_H

#include <string>
#include <unordered_map>
#include <unordered_set>
#include <cstdlib>

const std::string GRAPH = std::getenv("GRAPH") ? std::getenv("GRAPH") : "ng_0.05/METIS-amazon/1000";
const std::string GRAPH_NAME = std::getenv("GRAPH_NAME") ? std::getenv("GRAPH_NAME") : "com-amazon-connected";
const int ALLNODE = std::getenv("ALLNODE") ? std::stoi(std::getenv("ALLNODE")) : 334863;

//2. Louvainではない時にはこちらを使用
const std::string COMMUNITY_FILE = "./../create-tables/result/" + GRAPH + "/node_community.txt";

// グラフファイルパス
const std::string GRAPH_FILE = "./../../Louvain/graph/" + GRAPH_NAME + ".gr";
// const std::string GRAPH_FILE = GRAPH_NAME + ".gr";
const std::string GROUP_PER_COMMUNITY = "./../create-tables/result/" + GRAPH + "/dynamic_groups.txt";
const std::string NG_NODES_PER_COMMUNITY = "./../create-tables/result/" + GRAPH + "/ng_nodes.txt";
const std::string NGFILE = "./../create-tables/result/" + GRAPH + "/non-group-ng-nodes.txt"; // 読み込むファイルのパス

const double ALPHA = 0.15;
const int RW_COUNT = 10000;
const int START_NODE = 22;


#endif // CONFIG_H