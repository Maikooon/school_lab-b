#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <iomanip>
#include <filesystem>
#include <unordered_map>

namespace fs = std::filesystem;
const fs::path BASEFOLDER = "./../cache/result/";

// 各フォルダのファイル情報から平均を計算する関数
bool parseResultFile(const std::string& filePath, double& averageLength, double& totalLength, int& totalMoves, int& executionTime, double& cacheUse)
{
    std::ifstream file(filePath);
    if (!file.is_open())
    {
        std::cerr << "Error opening file: " << filePath << std::endl;
        return false;
    }

    std::string line;
    while (std::getline(file, line))
    {
        std::istringstream iss(line);
        std::string label;
        if (line.find("Average length: ") != std::string::npos)
        {
            iss >> label >> label >> averageLength;
        }
        else if (line.find("Total length: ") != std::string::npos)
        {
            iss >> label >> label >> totalLength;
        }
        else if (line.find("Total moves across communities: ") != std::string::npos)
        {
            iss >> label >> label >> label >> label >> totalMoves;
        }
        else if (line.find("Execution time: ") != std::string::npos)
        {
            iss >> label >> label >> executionTime;
        }
        else if (line.find("percentage of used cache: ") != std::string::npos)
        {
            iss >> label >> label >> label >> label >> cacheUse;
        }
    }
    file.close();
    return true;
}

// フォルダごとの平均を計測して処理する関数
bool processFolder(const fs::path& folderPath, double& avgAvgLength, double& avgTotalLength, int& avgTotalMoves, int& avgExecutionTime, double& avgCacheUse)
{
    std::vector<double> avgLengths;
    std::vector<double> totalLengths;
    std::vector<int> totalMoves;
    std::vector<int> executionTimes;
    std::vector<double> cacheUses;

    for (const auto& entry : fs::directory_iterator(folderPath))
    {
        if (entry.is_regular_file() && entry.path().extension() == "")
        {
            double avgLength, totalLength, cacheUse;
            int totalMove, executionTime;

            if (parseResultFile(entry.path().string(), avgLength, totalLength, totalMove, executionTime, cacheUse))
            {
                avgLengths.push_back(avgLength);
                totalLengths.push_back(totalLength);
                totalMoves.push_back(totalMove);
                executionTimes.push_back(executionTime);
                cacheUses.push_back(cacheUse);
            }
        }
    }

    if (avgLengths.empty())
    {
        std::cerr << "No result files found in folder: " << folderPath << std::endl;
        return false;
    }

    // 平均の計算
    avgAvgLength = 0.0;
    avgTotalLength = 0.0;
    avgTotalMoves = 0;
    avgExecutionTime = 0;
    avgCacheUse = 0.0;

    for (size_t i = 0; i < avgLengths.size(); ++i)
    {
        avgAvgLength += avgLengths[i];
        avgTotalLength += totalLengths[i];
        avgTotalMoves += totalMoves[i];
        avgExecutionTime += executionTimes[i];
        avgCacheUse += cacheUses[i];
    }

    avgAvgLength /= avgLengths.size();
    avgTotalLength /= avgLengths.size();
    avgTotalMoves /= avgLengths.size();
    avgExecutionTime /= avgLengths.size();
    avgCacheUse /= cacheUses.size();

    return true;
}

// グラフ情報を格納する関数
// グラフのノード数を取得するために必要
bool loadGraphInfo(const std::string& filename, std::unordered_map<std::string, std::pair<int, int>>& graphInfo)
{
    std::ifstream file(filename);
    if (!file.is_open())
    {
        std::cerr << "Error opening file: " << filename << std::endl;
        return false;
    }

    std::string line;
    std::string currentGraph;
    while (std::getline(file, line))
    {
        if (line.find("graph:") != std::string::npos)
        {
            std::istringstream iss(line);
            std::string label, graphName;
            iss >> label >> graphName;
            currentGraph = graphName;
        }
        else if (line.find("Nodes:") != std::string::npos)
        {
            std::istringstream iss(line);
            std::string label;
            int nodes, edges;
            char comma;
            iss >> label >> nodes >> comma >> label >> edges;
            graphInfo[currentGraph] = std::make_pair(nodes, edges);
        }
    }

    return true;
}

int main()
{
    //ここを平均を取りたいフォルダ名に変更する
    // const fs::path BASEFOLDER = "./construction/jwt-result-new-community/";
    // 固定値
    const std::string graphInfoFile = "./../count_node.txt";
    // 解析したいフォルダに格納される
    // const fs::path outputFilePath = "./result/overall_average_results.txt";
    const fs::path outputFilePath = BASEFOLDER / "overall_average_results.txt";

    // グラフ情報を読み込む
    std::unordered_map<std::string, std::pair<int, int>> graphInfo;
    if (!loadGraphInfo(graphInfoFile, graphInfo))
    {
        std::cerr << "Failed to load graph information." << std::endl;
        return 1;
    }

    // 出力ファイルを開く
    std::ofstream outFile(outputFilePath);
    if (!outFile.is_open())
    {
        std::cerr << "Error opening output file." << std::endl;
        return 1;
    }

    outFile << std::fixed << std::setprecision(5);

    // 各サブフォルダを処理する
    for (const auto& entry : fs::directory_iterator(BASEFOLDER))
    {
        if (entry.is_directory())
        {
            std::cout << "Processing folder: " << entry.path() << std::endl;

            double avgAvgLength, avgTotalLength, avgCacheUse;
            int avgTotalMoves, avgExecutionTime;

            if (processFolder(entry.path(), avgAvgLength, avgTotalLength, avgTotalMoves, avgExecutionTime, avgCacheUse))
            {
                std::string folderName = entry.path().filename().string();

                // 結果を出力する
                outFile << "Folder: " << folderName << std::endl;
                outFile << "Average length: " << avgAvgLength << std::endl;
                outFile << "Total length: " << avgTotalLength << std::endl;
                outFile << "Total moves across communities: " << avgTotalMoves << std::endl;
                outFile << "Execution time: " << avgExecutionTime << std::endl;
                outFile << "Average cache usage percentage: " << avgCacheUse << std::endl;

                // ノード数とエッジ数を出力する
                auto it = graphInfo.find(folderName);
                if (it != graphInfo.end())
                {
                    int nodes, edges;
                    std::tie(nodes, edges) = it->second;
                    outFile << "Nodes: " << nodes << ", Edges: " << edges << std::endl;
                }
                else
                {
                    outFile << "Nodes and edges information not found for graph: " << folderName << std::endl;
                }

                outFile << "-----------------------------" << std::endl;
            }
        }
    }

    outFile.close();
    std::cout << "Overall results written to " << outputFilePath << std::endl;

    return 0;
}
