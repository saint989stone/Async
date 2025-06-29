from inspect import getgeneratorstate #метод позволяет получить текущий статус генератора

"""
Делигирующий генератор - это генератор который вызывает другой генератор, который принимает подгенератор
Подгенератор - генератор который вызывает делигирующий 
Нужно когда один генератор нужно разбить на несколько. 
yield from <примаемый генератор> позволяет инициализировать подгенератор, который принимает значение return из подгенератора. 
По другому yield from называется await и смысл его вызывающий код напрямую управляет генератор, то есть блокирующий код вынужден ожидать, подгенератор должен обязательно содержать return,
в противном случае блокирующий код будет всегда заблокирован.
"""

class BlaExcept(Exception):
    pass

def coroutine(func):            #декоратор для отправки send для инициализации корутины
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner

@coroutine
def subgen():       #функция подгенератора
    while True:
        try:
            message = yield
        except BlaExcept:
            print('BlaExecept')
        else:
            print('sg', message)

@coroutine
def delgen(g):      #функция делигирующего генератора
    while True:
        try:
            data = yield
            g.send(data)
        except BlaExcept as e:
            g.throw(e)

def subgen1():       #функция подгенератора
    while True:
        try:
            message = yield
        except StopIteration:
            print('StopItera')
            break
        else:
            print('sg', message)
    return 'Result from SubGen'

@coroutine
def delgen1(g):      #функция делигирующего генератора
    result = yield from g
    print(result)

sg = subgen()
dg = delgen(sg)
dg.send('Hello')
dg.throw(BlaExcept)

sg1 = subgen1()
dg1 = delgen1(sg1)
dg1.send('adsd')
dg1.throw(StopIteration)
