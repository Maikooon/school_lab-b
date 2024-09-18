// /*
// 全てのグラフの実行時間を出したのちにこれを実行する
// g++ -std=c++17 -o calc-ave calc-ave.cpp

// 計算ファイルの一箇所のみの変更が必要
// */

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <iomanip>
#include <filesystem>

namespace fs = std::filesystem;
// const fs::path BASEFOLDER = "./nojwt/result/";
const fs::path BASEFOLDER = "./research/rwer-count-fb/every/";

// 各フォルダのファイル情報から平均を計算する関数
bool parseResultFile(const std::string& filePath, double& averageLength, double& totalLength, int& totalMoves, int& executionTime)
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
    }
    file.close();
    return true;
}

// フォルダごとの平均を計測して処理する関数
bool processFolder(const fs::path& folderPath, double& avgAvgLength, double& avgTotalLength, int& avgTotalMoves, int& avgExecutionTime)
{
    std::vector<double> avgLengths;
    std::vector<double> totalLengths;
    std::vector<int> totalMoves;
    std::vector<int> executionTimes;

    // fu
    for (const auto& entry : fs::directory_iterator(folderPath))
    {
        if (entry.is_regular_file() && entry.path().extension() == "")
        {
            double avgLength, totalLength;
            int totalMove, executionTime;

            if (parseResultFile(entry.path().string(), avgLength, totalLength, totalMove, executionTime))
            {
                avgLengths.push_back(avgLength);
                totalLengths.push_back(totalLength);
                totalMoves.push_back(totalMove);
                executionTimes.push_back(executionTime);
            }
        }
    }

    if (avgLengths.empty())
    {
        std::cerr << "No result files found in folder: " << folderPath << std::endl;
        return false;
    }

    // Calculate averages
    avgAvgLength = 0.0;
    avgTotalLength = 0.0;
    avgTotalMoves = 0;
    avgExecutionTime = 0;

    for (size_t i = 0; i < avgLengths.size(); ++i)
    {
        avgAvgLength += avgLengths[i];
        avgTotalLength += totalLengths[i];
        avgTotalMoves += totalMoves[i];
        avgExecutionTime += executionTimes[i];
    }

    avgAvgLength /= avgLengths.size();
    avgTotalLength /= avgLengths.size();
    avgTotalMoves /= avgLengths.size();
    avgExecutionTime /= avgLengths.size();

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
    std::unordered_map<std::string, std::pair<int, int>>
        graphInfo;
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

            double avgAvgLength, avgTotalLength;
            int avgTotalMoves, avgExecutionTime;

            if (processFolder(entry.path(), avgAvgLength, avgTotalLength, avgTotalMoves, avgExecutionTime))
            {
                std::string folderName = entry.path().filename().string();

                // 結果を出力する
                outFile << "Folder: " << folderName << std::endl;
                outFile << "Average length: " << avgAvgLength << std::endl;
                outFile << "Total length: " << avgTotalLength << std::endl;
                outFile << "Total moves across communities: " << avgTotalMoves << std::endl;
                outFile << "Execution time: " << avgExecutionTime << std::endl;

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

// #include <iostream>
// #include <fstream>
// #include <sstream>
// #include <string>
// #include <vector>
// #include <iomanip>
// #include <filesystem>
// #include <algorithm>
// #include <numeric>
// #include <cmath>  // std::sqrt

// // 分散と標準偏差を計算する関数
// void calculateVarianceAndStdDev(const std::vector<double>& data, double& variance, double& stdDev)
// {
//     if (data.empty())
//     {
//         variance = 0.0;
//         stdDev = 0.0;
//         return;
//     }

//     double mean = std::accumulate(data.begin(), data.end(), 0.0) / data.size();

//     double sumSquares = std::accumulate(data.begin(), data.end(), 0.0, [mean](double acc, double val) {
//         return acc + (val - mean) * (val - mean);
//         });

//     variance = sumSquares / data.size();
//     stdDev = std::sqrt(variance);
// }


// namespace fs = std::filesystem;
// const fs::path BASEFOLDER = "./nojwt/result/";

// // 各フォルダのファイル情報から測定値を読み取る関数
// bool parseResultFile(const std::string& filePath, double& avgLength, double& totalLength, int& totalMoves, int& executionTime)
// {
//     std::ifstream file(filePath);
//     if (!file.is_open())
//     {
//         std::cerr << "Error opening file: " << filePath << std::endl;
//         return false;
//     }

//     std::string line;
//     while (std::getline(file, line))
//     {
//         std::istringstream iss(line);
//         std::string label;
//         if (line.find("Average length: ") != std::string::npos)
//         {
//             iss >> label >> label >> avgLength;
//         }
//         else if (line.find("Total length: ") != std::string::npos)
//         {
//             iss >> label >> label >> totalLength;
//         }
//         else if (line.find("Total moves across communities: ") != std::string::npos)
//         {
//             iss >> label >> label >> label >> label >> totalMoves;
//         }
//         else if (line.find("Execution time: ") != std::string::npos)
//         {
//             iss >> label >> label >> executionTime;
//         }
//     }
//     file.close();
//     return true;
// }

// // フォルダごとの統計を計測して処理する関数
// bool processFolder(const fs::path& folderPath, std::vector<double>& avgLengths, std::vector<double>& totalLengths, std::vector<int>& totalMoves, std::vector<int>& executionTimes)
// {
//     for (const auto& entry : fs::directory_iterator(folderPath))
//     {
//         if (entry.is_regular_file() && entry.path().extension() == "")
//         {
//             double avgLength, totalLength;
//             int totalMove, executionTime;

//             if (parseResultFile(entry.path().string(), avgLength, totalLength, totalMove, executionTime))
//             {
//                 avgLengths.push_back(avgLength);
//                 totalLengths.push_back(totalLength);
//                 totalMoves.push_back(totalMove);
//                 executionTimes.push_back(executionTime);
//             }
//         }
//     }

//     if (avgLengths.empty())
//     {
//         std::cerr << "No result files found in folder: " << folderPath << std::endl;
//         return false;
//     }

//     return true;
// }

// // 統計情報を計算する関数
// void calculateStatistics(const std::vector<double>& data, double& median, double& q1, double& q3, double& min, double& max, double& variance, double& stdDev)
// {
//     if (data.empty())
//         return;

//     std::vector<double> sortedData = data;
//     std::sort(sortedData.begin(), sortedData.end());

//     size_t n = sortedData.size();
//     min = sortedData.front();
//     max = sortedData.back();

//     // 中央値
//     if (n % 2 == 0)
//         median = (sortedData[n / 2 - 1] + sortedData[n / 2]) / 2.0;
//     else
//         median = sortedData[n / 2];

//     // 第1四分位点
//     size_t q1_index = n / 4;
//     if (n % 4 == 0)
//         q1 = (sortedData[q1_index - 1] + sortedData[q1_index]) / 2.0;
//     else
//         q1 = sortedData[q1_index];

//     // 第3四分位点
//     size_t q3_index = 3 * n / 4;
//     if (n % 4 == 0)
//         q3 = (sortedData[q3_index - 1] + sortedData[q3_index]) / 2.0;
//     else
//         q3 = sortedData[q3_index];

//     // 分散と標準偏差
//     calculateVarianceAndStdDev(data, variance, stdDev);
// }

// int main()
// {
//     // ここを平均を取りたいフォルダ名に変更する
//     // const fs::path BASEFOLDER = "./construction/jwt-result-new-community/";
//     const fs::path outputFilePath = BASEFOLDER / "overall_statistics.txt";

//     // 出力ファイルを開く
//     std::ofstream outFile(outputFilePath);
//     if (!outFile.is_open())
//     {
//         std::cerr << "Error opening output file." << std::endl;
//         return 1;
//     }

//     outFile << std::fixed << std::setprecision(5);

//     // 各サブフォルダを処理する
//     for (const auto& entry : fs::directory_iterator(BASEFOLDER))
//     {
//         if (entry.is_directory())
//         {
//             std::cout << "Processing folder: " << entry.path() << std::endl;

//             std::vector<double> avgLengths;
//             std::vector<double> totalLengths;
//             std::vector<int> totalMoves;
//             std::vector<int> executionTimes;

//             if (processFolder(entry.path(), avgLengths, totalLengths, totalMoves, executionTimes))
//             {
//                 std::string folderName = entry.path().filename().string();

//                 // 統計情報を計算する
//                 double median, q1, q3, min, max, variance, stdDev;

//                 // Average lengthの統計
//                 calculateStatistics(avgLengths, median, q1, q3, min, max, variance, stdDev);
//                 outFile << "Folder: " << folderName << std::endl;
//                 outFile << "Average length - Minimum: " << min << ", 1st Quartile (Q1): " << q1 << ", Median: " << median << ", 3rd Quartile (Q3): " << q3 << ", Maximum: " << max << ", Variance: " << variance << ", Standard Deviation: " << stdDev << std::endl;

//                 // Total lengthの統計
//                 calculateStatistics(totalLengths, median, q1, q3, min, max, variance, stdDev);
//                 outFile << "Total length - Minimum: " << min << ", 1st Quartile (Q1): " << q1 << ", Median: " << median << ", 3rd Quartile (Q3): " << q3 << ", Maximum: " << max << ", Variance: " << variance << ", Standard Deviation: " << stdDev << std::endl;

//                 // Total movesの統計
//                 calculateStatistics(std::vector<double>(totalMoves.begin(), totalMoves.end()), median, q1, q3, min, max, variance, stdDev);
//                 outFile << "Total moves - Minimum: " << min << ", 1st Quartile (Q1): " << q1 << ", Median: " << median << ", 3rd Quartile (Q3): " << q3 << ", Maximum: " << max << ", Variance: " << variance << ", Standard Deviation: " << stdDev << std::endl;

//                 // Execution timeの統計
//                 calculateStatistics(std::vector<double>(executionTimes.begin(), executionTimes.end()), median, q1, q3, min, max, variance, stdDev);
//                 outFile << "Execution time - Minimum: " << min << ", 1st Quartile (Q1): " << q1 << ", Median: " << median << ", 3rd Quartile (Q3): " << q3 << ", Maximum: " << max << ", Variance: " << variance << ", Standard Deviation: " << stdDev << std::endl;

//                 outFile << "-----------------------------" << std::endl;
//             }
//         }
//     }
// }