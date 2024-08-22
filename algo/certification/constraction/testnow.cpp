// // g++ - std = c++ 17 - o test - now testnow.cpp

// #include <iostream>
// #include <fstream>
// #include <sstream>
// #include <string>
// #include <vector>
// #include <iomanip>
// #include <filesystem>

// namespace fs = std::filesystem;

// // Function to parse a single result file and extract values
// bool parseResultFile(const std::string &filePath, double &averageLength, double &totalLength, int &totalMoves, int &executionTime)
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
//         double value;
//         if (line.find("Average length:") != std::string::npos)
//         {
//             iss >> label >> label >> averageLength;
//         }
//         else if (line.find("Total length:") != std::string::npos)
//         {
//             iss >> label >> label >> totalLength;
//         }
//         else if (line.find("Total moves across communities:") != std::string::npos)
//         {
//             iss >> label >> label >> totalMoves;
//         }
//         else if (line.find("Execution time:") != std::string::npos)
//         {
//             iss >> label >> label >> executionTime;
//         }
//     }
//     file.close();
//     return true;
// }

// // Function to process all result files in a given folder
// void processFolder(const fs::path &folderPath)
// {
//     std::vector<double> avgLengths;
//     std::vector<double> totalLengths;
//     std::vector<int> totalMoves;
//     std::vector<int> executionTimes;

//     // Iterate over all result files in the folder
//     for (const auto &entry : fs::directory_iterator(folderPath))
//     {
//         if (entry.is_regular_file() && entry.path().extension() == ".txt")
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
//         return;
//     }

//     // Calculate averages
//     double avgAvgLength = 0.0, avgTotalLength = 0.0;
//     int avgTotalMoves = 0, avgExecutionTime = 0;

//     for (size_t i = 0; i < avgLengths.size(); ++i)
//     {
//         avgAvgLength += avgLengths[i];
//         avgTotalLength += totalLengths[i];
//         avgTotalMoves += totalMoves[i];
//         avgExecutionTime += executionTimes[i];
//     }

//     avgAvgLength /= avgLengths.size();
//     avgTotalLength /= avgLengths.size();
//     avgTotalMoves /= avgLengths.size();
//     avgExecutionTime /= avgLengths.size();

//     // Output the results to a file
//     std::ofstream outFile(folderPath / "average_results.txt");
//     if (!outFile.is_open())
//     {
//         std::cerr << "Error opening output file in folder: " << folderPath << std::endl;
//         return;
//     }

//     outFile << std::fixed << std::setprecision(5);
//     outFile << "Average length: " << avgAvgLength << std::endl;
//     outFile << "Total length: " << avgTotalLength << std::endl;
//     outFile << "Total moves across communities: " << avgTotalMoves << std::endl;
//     outFile << "Execution time: " << avgExecutionTime << std::endl;

//     outFile.close();
//     std::cout << "Results written to " << folderPath / "average_results.txt" << std::endl;
// }

// void listFilesInFolder(const fs::path &folderPath)
// {
//     std::cout << "Files in folder " << folderPath << ":" << std::endl;
//     for (const auto &entry : fs::directory_iterator(folderPath))
//     {
//         if (entry.is_regular_file())
//         {
//             std::cout << "Found file: " << entry.path() << std::endl;
//         }
//         else if (entry.is_directory())
//         {
//             std::cout << "Found directory: " << entry.path() << std::endl;
//         }
//     }
// }

// int main()
// {
//     const fs::path baseFolder = "./result/";
//     // Process each subfolder within the base folder
//     for (const auto &entry : fs::directory_iterator(baseFolder))
//     {
//         if (entry.is_directory())
//         {
//             std::cout << "Processing folder: " << entry.path() << std::endl;
//             listFilesInFolder(entry.path()); // List files for debugging
//             processFolder(entry.path());
//         }
//     }
//     // Process each subfolder within the base folder
//     for (const auto &entry : fs::directory_iterator(baseFolder))
//     {
//         if (entry.is_directory())
//         {
//             processFolder(entry.path());
//         }
//     }

//     return 0;
// }
