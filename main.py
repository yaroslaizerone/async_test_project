import socket


def main():
    try:
        # создаём объект сокета
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # настройка опций сокета
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # подключение к удалённому сокету
        client_socket.connect(('localhost', 9990))
        print("Success connect")
    except:
        print("Error connect")

    while True:
        try:
            # ввод клиента сообщения для сервера
            message: str = input("Enter a message for the server>> ")
            # отправка данных в сокет
            client_socket.send(message.encode())
            # преобразование полученного ответа
            message_server = client_socket.recv(1024).decode()
            # вывод ответа
            print("Message from the server: " + message_server)

        except Exception:
            print("Что-то пошло не так...")
        except KeyboardInterrupt:
            client_socket.close()
            exit()


if __name__ == '__main__':
    main()