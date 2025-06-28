import socket
from select import select
"""
select - системная функция для мониторинга состояния файловых объектов 
.fileno() - возвращает файловый дескриптор, то есть число которое ассоциировано с файлом
на вход select получает три списка объектов которые необходимо мониторить: 
    1. Объекты доступные для чтения
    2. Объекты доступные для записи
    3. Объекты с ошибками
На выходе отравляет те же списке, но с объектами на которых сработали события
"""
"""
В отличии от original, благодаря мониторингу через select позволяет запускать функциии асинхронно

"""
to_monitor = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #SOCK_STREAM = TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #определяем переиспользование порта
server_socket.bind(('localhost', 5001))
server_socket.listen()      #прослушивание сокета


def accept_connect(server_socket):
    client_socket, address = server_socket.accept()          #принимаем клиентское подключение
    print('Connection from', address)
    to_monitor.append(client_socket)    

def send_message(client_socket):
 
    print('Before receive')
    request = client_socket.recv(4096)
    if request:
        respose = 'Hello world\n'.encode()      #подготавливаем ответ кодируем его в байты
        client_socket.send(respose)     #отправляем ответ клиенту
    else:
        print('Close socket')
        client_socket.close()


def event_loop():           #event loop управляет запуском функций
    while True:
        ready_to_read, _, _ = select(to_monitor, [], []) #read, write, errors
        for sock in ready_to_read:
            if sock is server_socket:
                accept_connect(sock)
            else:
                send_message(sock)
if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()
    #accept_connect(server_socket)
    