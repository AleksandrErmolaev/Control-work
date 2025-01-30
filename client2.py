import socket
import threading
import pickle

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break

            message = pickle.loads(message)
            print(f"\n{message['sender']}: {message['text']}")
        except:
            print("Соединение с сервером потеряно.")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    username = input("Введите ваше имя: ")

    while True:
        message_text = input()
        if message_text == "/stats":
            client_socket.send(pickle.dumps({"command": "stats", "sender": username}))
            continue

        message = {
            "sender": username,
            "text": message_text
        }

        client_socket.send(pickle.dumps(message))

if __name__ == "__main__":
    main()