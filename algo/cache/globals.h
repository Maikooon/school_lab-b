//globals.h
#ifndef GLOBALS_H
#define GLOBALS_H

#include <unordered_map>
#include <unordered_set>
#include <string>

extern int cache_use_count;
extern std::unordered_map<int, std::unordered_set<int>> graph;
extern std::unordered_map<int, int> node_communities;

extern const std::string SECRET_KEY;
extern const std::string VERIFY_SECRET_KEY;

extern std::int16_t count_token_expired;

extern double total_token_generation_time;
extern double total_search_time;
extern double total_token_verification_time;
extern double total_token_construction_time;
extern double total_difference_time;
extern double default_time;

extern int authentication_count;
extern int cache_use_count;

#endif
