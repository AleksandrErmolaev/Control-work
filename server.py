import socket
import threading
import pickle

MESSAGE_FILE = 'messages.pkl'

clients = []

message_count = 0

def broadcast_message(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(pickle.dumps(message))
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    global message_count
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break

            message = pickle.loads(message)

            if message.get("command") == "stats":
                stats_message = {"sender": "Сервер", "text": f"Количество сообщений: {message_count}"}
                client_socket.send(pickle.dumps(stats_message))
                continue

            print(f"Получено сообщение: {message}")

            with open(MESSAGE_FILE, 'ab') as f:
                pickle.dump(message, f)

            message_count += 1
            broadcast_message(message, client_socket)
        except:
            break

    client_socket.close()
    clients.remove(client_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen()

    print("Сервер запущен и ожидает подключения клиентов...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключен клиент: {addr}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()