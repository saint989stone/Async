from inspect import getgeneratorstate #метод позволяет получить текущий статус генератора

"""
Коротины или саб-программы - это генераторы, которые из вне могут получить данные при помощи метода send.
При помощи метода throw в корутину можно передать исключения.
Корутины могут содержать return, которое отдает значение после остановки бесконечного цикла. Значение в return можно получить вызвав обработку исключения значение хранится в переменной value объекта исключения.
"""

class BlaExcept(Exception):
    pass

def coroutine(func):            #декоратор для отправки send для инициализации корутины
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner

def subgen():
    x = 'Ready to accept message'
    try:
        message = yield x       #метод send отправляет значение. при первом вызове send выполнилось x = 'Ready to accept message' и yield при втором вызове выполнилось присвоение значение аргумента переданного в send переменной message 
        print('Subgen received:', message)
    except StopIteration:
        print('Done')

@coroutine
def average():
    count = 0
    summ = 0
    average = None
    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done')
            break
        except BlaExcept:
            print('BlaExcept')
            break
        else:
            count += 1
            summ = x
            average = round(summ / count, 2)
    return average          


# g = subgen()
# print (getgeneratorstate(g))        #текущий статус генератора GEN_CREATED
# x = g.send(None)           #метод send c аргументом None заставляет генератор перейти к следующей итерации, работает как метод next()
# print(x)            #при                                                                                                                                  
# print (getgeneratorstate(g))            #текущий статус генератора GEN_SUSPENDED
# g.send('Hello')         #аргумент "Hello" попадает в переменную message функции subgen

g = average()
print (getgeneratorstate(g))
result1 = g.send(4)
print(result1)
result2 = g.send(5)
print(result2)
result3 = g.send(10)
print(result3)
try:
    g.throw(StopIteration)
except StopIteration as e:
    print(e.value)

