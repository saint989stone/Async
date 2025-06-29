from inspect import getgeneratorstate #метод позволяет получить текущий статус генератора

"""
Коротины или саб-программы - это генераторы, которые из вне могут получить данные при помощи метода send.

"""
def subgen():
    message = yield
    print('Subgen received:', message)

g = subgen()
print (getgeneratorstate(g))        #текущий статус генератора
g.send(None)            #метод приостанавливает генератор
print (getgeneratorstate(g))            #текущий статус генератора