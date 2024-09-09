
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <map>
#include <filesystem>  
#include <iostream>
#include "globals.h"

using namespace std;

string OUTPUT_PATH = "./result/new-community/";

// 結果の出力
void output_results(int global_total, int global_total_move, const string& community_path, const string& path, long long duration)
{

    // 適切なファイル名を取得する（サブディレクトリ名に利用）
    size_t last_slash_idx = community_path.find_last_of("/\\");
    string filename = community_path.substr(last_slash_idx + 1);

    size_t period_idx = filename.rfind('.');
    if (period_idx != string::npos)
    {
        filename = filename.substr(0, period_idx);
    }

    // 出力先のパスを生成
    // std::string filepath = "./jwt-result-0.15/" + filename + "/" + path + "-time";
    std::string filepath = OUTPUT_PATH + filename + "/" + path;

    // 出力ファイルのストリームを開く
    std::ofstream outputFile(filepath);
    if (!outputFile.is_open())
    {
        std::cerr << "Failed to open file: " << filepath << std::endl;
        return;
    }

    // 結果の出力 
    double ave = static_cast<double>(global_total) / node_communities.size();
    cout << "Average length: " << ave << endl;
    outputFile << "Average length: " << ave << std::endl;

    cout << "Total length: " << global_total << endl;
    outputFile << "Total length: " << global_total << std::endl;

    cout << "Total moves across communities: " << global_total_move << endl;
    outputFile << "Total moves across communities: " << global_total_move << std::endl;

    cout << "Program execution time: " << duration << " milliseconds" << endl;
    outputFile << "Execution time: " << duration << std::endl;

    cout << "Authentication count: " << authentication_count << endl;
    outputFile << "Authentication count: " << authentication_count << std::endl;

    cout << "Cache use count: " << cache_use_count << endl;
    outputFile << "Cache use count: " << cache_use_count << std::endl;

    double percentage_of_cache = static_cast<double>(cache_use_count) / authentication_count;
    cout << "percentage of used cache: " << percentage_of_cache << std::endl;
    outputFile << "percentage of used cache: " << percentage_of_cache << std::endl;

    //時間の内訳を調査する
    cout << "total token generate time; " << total_token_generation_time << std::endl;
    outputFile << "total token generate time: " << total_token_generation_time << std::endl;

    cout << "total token verification time: " << total_token_verification_time << std::endl;
    outputFile << "total token verification time: " << total_token_verification_time << std::endl;

    total_difference_time = duration - default_time - total_token_generation_time - total_token_verification_time;
    cout << "total difference time: " << total_difference_time << std::endl;
    outputFile << "total difference time: " << total_difference_time << std::endl;

    cout << "total construction time: " << total_token_construction_time << std::endl;
    outputFile << "total construction time: " << total_token_construction_time << std::endl;

    //ここまで

        //ファイルを閉じる
    outputFile.close();
    cout << "Result has been written to " << filepath << endl;


}