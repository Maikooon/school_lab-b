#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <filesystem>
#include <iomanip>
#include <unordered_map>

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

// Function to read node and edge information from a file
bool loadGraphInfo(const std::string &filename, std::unordered_map<std::string, std::pair<int, int>> &graphInfo)
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
            std::string label;
            iss >> label >> currentGraph;
        }
        else if (line.find("Nodes:") != std::string::npos)
        {
            std::istringstream iss(line);
            std::string label;
            int nodes, edges;
            char comma;
            iss >> label >> nodes >> comma >> label >> edges;
            graphInfo[currentGraph] = {nodes, edges};
        }
    }
    file.close();
    return true;
}

// Function to process all result files in a given folder and calculate averages
bool processFolder(const fs::path &folderPath, double &avgAvgLength, double &avgTotalLength, int &avgTotalMoves, int &avgExecutionTime)
{
    std::vector<double> avgLengths, totalLengths;
    std::vector<int> totalMoves, executionTimes;

    for (const auto &entry : fs::directory_iterator(folderPath))
    {
        if (entry.is_regular_file() && entry.path().extension() == ".txt")
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
