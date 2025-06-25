import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #SOCK_STREAM = TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #определяем переиспользование порта
server_socket.bind(('localhost', 5000))
server_socket.listen()      #прослушивание сокета

while True:
    print('Before accept')
    client_socket, address = server_socket.accept()          #принимаем клиентское подключение
    print('Connection from', address)

    while True:
        print('Before receive')
        request = client_socket.recv(4096)
        if not request:
            break
        else:
            respose = 'Hello world\n'.encode()      #подготавливаем ответ кодируем его в байты
            client_socket.send(respose)     #отправляем ответ клиенту
    print('Outside inner Receive Loop')
    client_socket.close()