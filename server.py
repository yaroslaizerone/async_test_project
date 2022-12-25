import os
import re
import socket
from select import select
from os import listdir
from os.path import isfile, join
from prettytable import PrettyTable
from pathlib import Path
tasks = []
to_read = {}
to_write = {}


def server():
    try:
        # создание объекта сокета
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # настройка опций сокета
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # привязка адреса к сокету
        server_socket.bind(("0.0.0.0", 9990))
        # переводим сервер в режим ожидания подключения
        server_socket.listen(0)
        print("[+] Waiting for incoming connections")
    except:
        print("Error")

    while True:
        # возвращаем в основную прорамму, то что сервер работает в режиме чтения
        yield ('read', server_socket)
        # записываем в переменные объект сокета и его адресс
        cl_socket, remote_address = server_socket.accept()
        print(f"[+] Got a connection from {remote_address} ")
        # добавляем в список задач состояния объектов
        tasks.append(process_client(cl_socket, remote_address))


def process_client(cl_socket: socket, remote_address):
    while True:
        yield ('read', cl_socket)
        # получаем данные из сокета
        message = cl_socket.recv(1024).decode()
        dict = r'C:\Users\kolpa\PycharmProjects\Extask\server_files'
        pattern = re.compile(r'ALL')
        if pattern.findall(message):
            result = 0
        else:
            result = 1
        if not message:
            break
        else:
            if message == 'FILES':
                onlyfiles = [f for f in listdir(dict) if isfile(join(dict, f))]
                for file in onlyfiles:
                    print(file)
                # отправляем в терминал сервера полученный результат
                message = " ".join(onlyfiles)
                print(f"Message from the client {remote_address}: " + message)
            elif result == 0:
                item_search = re.search(r'ALL', message)
                file = str(message.split("FILE ", 1)[1])

                if item_search.group(0) == "ALL":
                    #out_all(file)
                    a=1
            else:
                test = re.search(r'-\d{1,2}', message)
                if test is None:
                    item_search = re.search(r'\d{1,2}', message)
                    file = str(message.split("FILE ", 1)[1])
                    out_row(int(item_search.group(0)), file)
                else:
                    item_search = re.search(r'\d{1,2}', message)
                    file = str(message.split("FILE ", 1)[1])
                    count: int = int(item_search.group(0)) * -1
                    print(count)
                    out_row(count, file)
            # отправляем результат клиенту
            cl_socket.send(message.encode())
    cl_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):
        # пока не закончатся элементы в списке
        while not tasks:
            # запишем их в списки
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))
            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
        # распределим эементы по спискам
        try:
            task = tasks.pop(0)
            reason, sock = next(task)
            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
        except StopIteration:
            print('Done!')


def out_all(file):
    try:
        my_table = PrettyTable(["id", "first_name", "last_name", "age", "city", "phone", "email", "birthday"])
        my_file = open(r'C:\Users\kolpa\PycharmProjects\Extask\server_files\data_low.csv', encoding='utf8')
        s: list = my_file.readlines()
        a: int = 0

        while a < len(s):
            line: str = len(s[a])
            if a + 1 == len(s):
                id, name, surname, age, city, phone, email, birthday = map(str, s[a].split(";"))
                my_table.add_row([id, name, surname, age, city, phone, email, birthday])
            else:
                remove_last: str = s[a][:line - 1]
                id, name, surname, age, city, phone, email, birthday = map(str, remove_last.split(";"))
                my_table.add_row([id, name, surname, age, city, phone, email, birthday])
            a += 1
        print(my_table)
        my_file.close()
    except SyntaxError:
        print("Ошибка чтения файла!")
    except:
        print("Шото пошло не так")


def out_row(row, file):
    try:
        my_table = PrettyTable(["id", "first_name", "last_name", "age", "city", "phone", "email", "birthday"])
        my_file = open(r'C:\Users\kolpa\PycharmProjects\Extask\server_files\data_low.csv', encoding='utf8')
        s: list = my_file.readlines()
        length_list = len(s)
        a: int = 0
        if row < 0:
            a = length_list+row
            print(a)
        else:
            length_list = row

        while a < length_list:
            line: str = len(s[a])
            if a + 1 == len(s):
                id, name, surname, age, city, phone, email, birthday = map(str, s[a].split(";"))
                my_table.add_row([id, name, surname, age, city, phone, email, birthday])
            else:
                remove_last: str = s[a][:line - 1]
                id, name, surname, age, city, phone, email, birthday = map(str, remove_last.split(";"))
                my_table.add_row([id, name, surname, age, city, phone, email, birthday])
            a += 1
        print(my_table)
        my_file.close()
    except SyntaxError:
        print("Ошибка чтения файла!")
    except:
        print("Шото пошло не так")


if __name__ == "__main__":
    tasks.append(server())
    event_loop()