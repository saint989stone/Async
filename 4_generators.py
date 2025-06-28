import socket
from select import select

"""
Генераторы отдают кортежи где первый элемент кортежа это признак read или write второй элемент кортежа это сокет
По признаку кортежа read или write сокет попадает на мониторинг функции select в соотвествующий аргумент
Функция select отдает списки сокетов готовых к чтению и записи в событийный блок event_loop
Event loop происходит вызов функции next() с аргументом task (генератором), который попадает в соотвествующий список to_read, to_write, сокеты которых готовы к работе.
Методом select отбираем сокеты которые котовы к чтению и записи и добавляем их в соотвествующий список ready_to_read, ready_to_write
В каждый список ready_to_read ready_to_write добавляем ключи сокеты значения генераторы
"""

tasks = []          #список с генераторами

to_read = {}        #ключ - сокет, значение генератор
to_write = {}

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #SOCK_STREAM = TCP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #определяем переиспользование порта
    server_socket.bind(('localhost', 5000))
    server_socket.listen()      #прослушивание сокета

    while True:
        yield ('read', server_socket)
        print('Before accept')
        client_socket, address = server_socket.accept()          #принимаем клиентское подключение
        print('Connection from', address)
        tasks.append(client(client_socket))         #добавляем генератор обрабатывющий сокет

def client(client_socket):
    while True:
        yield ('read', client_socket)
        print('Before receive')
        request = client_socket.recv(4096)      #read запрос блокирующая функция не блокирует выполнение, потому что есть yield которая возвращает выполенение программы
        if not request:
            break
        else:
            response = 'Hello world\n'.encode()      #подготавливаем ответ кодируем его в байты
            yield ('write', client_socket)
            client_socket.send(response)     #write отправляем ответ клиенту
    print('Outside inner Receive Loop')
    client_socket.close()

def event_loop():
    while any([tasks, to_read, to_write])         #any возвращает True если хотя бы один элемент итерируемого объекте True
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])        #в списки ready_to_read и ready_to_write попадают ключи (сокеты), которые готовы к чтению и записи
            for sock in ready_to_read:      #перебираем сокеты
                tasks.append(to_read.pop(sock))     #добавляем в список tasks сокеты, метод pop позволяет осуществлять их ротацию удаляя из списка ready_to_read и добавляя в список tasks
            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
        try:
            task = tasks.pop(0)     #получаем генератор 
            reason, sock = next(task)       #запускаем итерацию генератора
            if reason == 'read':
                to_read[sock] = task    #добавляем в словарь ключ сокет значение генератор
            if reason =='write':
                to_write[sock] = task
        except StopIteration:
            print('Done')
tasks.append(server())
event_loop()