#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

#define MAX_COMMUNITIES 1000
#define MAX_NODES 10000

const char* input_dir = "./../../Louvain/community";
const char* output_dir = "./table";

const char* community_file_list[] = {
    "ca-grqc-connected.cm",
    "cmu.cm",
    "com-amazon-connected.cm",
    "fb-caltech-connected.cm",
    "karate-graph.cm",
    "karate.cm",
    "rt-retweet.cm",
    "simple_graph.cm",
    "tmp.cm",
};

int community_list[MAX_COMMUNITIES][MAX_NODES];
int community_size[MAX_COMMUNITIES];
int total_communities = 0;

void select_graph(char* selected_graph) {
    // グラフファイルを選択する
    int choice;
    printf("グラフファイルを選択してください:\n");
    for (int i = 0; i < sizeof(community_file_list) / sizeof(char*); i++) {
        printf("%d: %s\n", i, community_file_list[i]);
    }

    printf("番号を入力してください: ");
    scanf("%d", &choice);

    if (choice < 0 || choice >= sizeof(community_file_list) / sizeof(char*)) {
        printf("無効な番号が入力されました。\n");
        exit(1);
    }

    strcpy(selected_graph, community_file_list[choice]);
}

void process_communities(const char* graph_file_name) {
    char input_file_path[256];
    snprintf(input_file_path, sizeof(input_file_path), "%s/%s", input_dir, graph_file_name);

    FILE* fp = fopen(input_file_path, "r");
    if (fp == NULL) {
        perror("ファイルを開けませんでした");
        exit(1);
    }

    // コミュニティごとにノードを格納する
    int node, community;
    while (fscanf(fp, "%d %d", &node, &community) != EOF) {
        if (community >= MAX_COMMUNITIES) {
            printf("コミュニティ数が最大値を超えました。\n");
            exit(1);
        }
        community_list[community][community_size[community]++] = node;
    }

    fclose(fp);

    // 各コミュニティに対して処理を行う
    for (community = 0; community < MAX_COMMUNITIES; community++) {
        if (community_size[community] == 0 || community < 21) {
            continue;
        }

        // 出力ディレクトリの作成
        char output_dir_path[256];
        snprintf(output_dir_path, sizeof(output_dir_path), "%s/%s", output_dir, graph_file_name);
        mkdir(output_dir_path, 0755);

        // 結果をファイルに書き出し
        char output_file_path[256];
        snprintf(output_file_path, sizeof(output_file_path), "%s/community_%d_result.txt", output_dir_path, community);
        FILE* out_fp = fopen(output_file_path, "w");
        if (out_fp == NULL) {
            perror("出力ファイルを開けませんでした");
            exit(1);
        }

        // ノードリストの書き出し
        for (int i = 0; i < community_size[community]; i++) {
            int key_node = community_list[community][i];
            fprintf(out_fp, "%d: ", key_node);
            for (int c = 0; c < MAX_COMMUNITIES; c++) {
                if (c == community) {
                    continue;
                }
                for (int j = 0; j < community_size[c]; j++) {
                    fprintf(out_fp, "%d", community_list[c][j]);
                    if (j < community_size[c] - 1) {
                        fprintf(out_fp, ", ");
                    }
                }
            }
            fprintf(out_fp, "\n");
        }

        fclose(out_fp);
        printf("コミュニティ %d の結果を %s に書き出しました。\n", community, output_file_path);
    }
}

int main() {
    char selected_graph[256];
    select_graph(selected_graph);
    printf("選択されたグラフ: %s\n", selected_graph);
    process_communities(selected_graph);
    return 0;
}
