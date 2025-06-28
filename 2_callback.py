import socket
import selectors
"""
Selectors более верхуровневый объект в отличие от select. Позволяет использовать функцию мониторинга файла предусмотренную в ОС
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
selector = selectors.DefaultSelector()      #получаем дефолт фунцию ОС

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #SOCK_STREAM = TCP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #определяем переиспользование порта
    server_socket.bind(('localhost', 5001))
    server_socket.listen()      #прослушивание сокета
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connect)          #1 аргумент объект который отслеживаем, 2 аргумент событие которое ожидаем, 3 аргумент связанные данные 


def accept_connect(server_socket):
    client_socket, address = server_socket.accept()          #принимаем клиентское подключение
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)
    print('Connection from', address)

def send_message(client_socket):
 
    print('Before receive')
    request = client_socket.recv(4096)
    if request:
        respose = 'Hello world\n'.encode()      #подготавливаем ответ кодируем его в байты
        client_socket.send(respose)     #отправляем ответ клиенту
    else:
        print('Close socket')
        selector.unregister(client_socket)  #снятие с регистрации объекта
        client_socket.close()


def event_loop():           #event loop управляет запуском функций
    while True:
        events = selector.select()          
        """
        Метод select() Возвращает кортеж (key, events) где: 
        key - это именнованный кортеж SelectorKey с ключами указанными при регистрации fileobj, events, data
        events - это тип события который сработал
        """
        for key, _ in events:
            callback = key.data     #получаем функцию указанную при регистрации 
            callback(key.fileobj)       #отправляем в функцию объект
if __name__ == '__main__':
    server()
    event_loop()
    #accept_connect(server_socket)
    