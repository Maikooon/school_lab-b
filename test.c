#include <mpi.h>
#include <stdio.h>

int main(int argc, char **argv)
{
    // 初期化
    MPI_Init(&argc, &argv);

    // プロセスの総数と現在のプロセスのランクを取得
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // 現在のプロセスがランク0の場合、他のプロセスにメッセージを送信
    if (world_rank == 0)
    {
        const char *message = "Hello, World";
        for (int i = 1; i < world_size; i++)
        {
            MPI_Send(message, 13, MPI_CHAR, i, 0, MPI_COMM_WORLD);
        }
    }
    else
    {
        // ランク0以外のプロセスはメッセージを受信
        char message[13];
        MPI_Recv(message, 13, MPI_CHAR, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Process %d received message: %s\n", world_rank, message);
    }

    // 終了
    MPI_Finalize();

    return 0;
}
