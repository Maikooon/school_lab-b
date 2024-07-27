#include <iostream>
#include <cstring>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 5000
#define BUFFER_SIZE 1024

void start_client()
{
    int sock = 0;
    struct sockaddr_in serv_addr;
    char buffer[BUFFER_SIZE] = {0};

    // ソケットの作成
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        std::cerr << "Socket creation error" << std::endl;
        return;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // サーバーアドレスの設定
    if (inet_pton(AF_INET, "3.112.51.163", &serv_addr.sin_addr) <= 0)
    {
        std::cerr << "Invalid address/ Address not supported" << std::endl;
        return;
    }

    // サーバーに接続
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        std::cerr << "Connection Failed" << std::endl;
        return;
    }

    // サーバーにデータを送信
    const char *message = "Hello, Server!";
    send(sock, message, strlen(message), 0);

    // サーバーからの応答を受信
    read(sock, buffer, BUFFER_SIZE);
    std::cout << "Received from server: " << buffer << std::endl;

    // クライアントソケットを閉じる
    close(sock);
}

int main()
{
    start_client();
    return 0;
}
