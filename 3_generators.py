"""
Событийный цикл на основе принципа RoundRobin Карусель основан на цикличности выполнения когда объект после выполнения становится в конец очереди.
Генераторы это функции, у которых происходит приостановка выполнения то есть передача контроля выполнения программы
Пример:
def gen_filename():
    while True:
        pattern = 'file-{}.jpeg'
        t = int(time() * 1000)

        yield pattern.format(str(t)) #возвращение значения приостановка выполнения

        summ = 234 + 234 #выполнение при следующей итерации

Интрукций yield может быть несколько
def gen():
    yield 1
    yield 2
    yield 3
"""
from time import time

def gen1(s):
    for i in s:
        yield i



def gen_filename():
    while True:
        pattern = 'file-{}.jpeg'
        t = int(time() * 1000)
        yield pattern.format(str(t))

def gen2(n):
    for i in range(n):
        yield i

g1 = gen1('oleg')
g2 = gen2(4)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)
    try: 
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        pass
