#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <iomanip>
#include <filesystem>

namespace fs = std::filesystem;

// Function to parse a single result file and extract values
bool parseResultFile(const std::string &filePath, double &averageLength, double &totalLength, int &totalMoves, int &executionTime)
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
        if (line.find("Average length:") != std::string::npos)
        {
            iss >> label >> label >> averageLength;
        }
        else if (line.find("Total length:") != std::string::npos)
        {
            iss >> label >> label >> totalLength;
        }
        else if (line.find("Total moves across communities:") != std::string::npos)
        {
            iss >> label >> label >> totalMoves;
        }
        else if (line.find("Execution time:") != std::string::npos)
        {
            iss >> label >> label >> executionTime;
        }
    }
    file.close();
    return true;
}

// フォルダごとの平均を計測して処理する関数
bool processFolder(const fs::path &folderPath, double &avgAvgLength, double &avgTotalLength, int &avgTotalMoves, int &avgExecutionTime)
{
    std::vector<double> avgLengths;
    std::vector<double> totalLengths;
    std::vector<int> totalMoves;
    std::vector<int> executionTimes;

    // fu
    for (const auto &entry : fs::directory_iterator(folderPath))
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

int main()
{
    const fs::path baseFolder = "./result/";

    std::ofstream outFile("./result/overall_average_results.txt");
    if (!outFile.is_open())
    {
        std::cerr << "Error opening output file." << std::endl;
        return 1;
    }

    outFile << std::fixed << std::setprecision(5);

    // Process each subfolder within the base folder
    for (const auto &entry : fs::directory_iterator(baseFolder))
    {
        if (entry.is_directory())
        {
            std::cout << "Processing folder: " << entry.path() << std::endl;

            double avgAvgLength, avgTotalLength;
            int avgTotalMoves, avgExecutionTime;

            // フォルダの数だけ出力する
            if (processFolder(entry.path(), avgAvgLength, avgTotalLength, avgTotalMoves, avgExecutionTime))
            {
                // Output the results to the file with folder name
                outFile << "Folder: " << entry.path().filename() << std::endl;
                outFile << "Average length: " << avgAvgLength << std::endl;
                outFile << "Total length: " << avgTotalLength << std::endl;
                outFile << "Total moves across communities: " << avgTotalMoves << std::endl;
                outFile << "Execution time: " << avgExecutionTime << std::endl;
                outFile << "-----------------------------" << std::endl;
            }
        }
    }

    outFile.close();
    std::cout << "Overall results written to ./result/overall_average_results.txt" << std::endl;

    return 0;
}
