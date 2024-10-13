# このコードはサーバ側(受け手側に配置してメッセージ受信の確認を行う)

# simple_server.py
import socket

def start_server(host='127.0.0.1', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started at {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        message = client_socket.recv(1024).decode()
        print(f"Received message: {message}")
        client_socket.close()

if __name__ == "__main__":
    start_server()
