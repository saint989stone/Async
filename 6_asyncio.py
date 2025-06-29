
"""
Корутина (coroutine) — это специальная функция или компонент программы, которая может приостанавливать своё выполнение и 
возобновлять его позже, сохраняя при этом своё состояние между вызовами.

Asyncio фреймворк для создания событийных циклов, является менеджером и планировщиком задач.
Организует событийный цикл, то есть когда происходит событие, отреагировать определенным образом вызвать функцию b.
События реализованы как экзепляры класса Tasks, который является под классом класса Future, который является "заглушкой", которые являются контейнерами для корутин
Экземпляры класса Task это действия которые должны выполняться ассинхронно.
После вызовыва ассинхронной функции она сразу должна передать управление передав в основной цикл залушку класса Future.
Схема работы
Event Loop:
    coroutine > Task (Future)
В event loop берется первая в очереди задача Task у ассоциированной с ней корутины вызывается метод step. Выполняет свой код.
@asyncio.coroutine - декоратор который из функции создает корутину основанную на генераторах, с python 3.5 заменен на async def, yield from на await
"""
import asyncio
from time import time

async def  print_nums():
    num = 1
    while True:
        print(num)
        num += 1
        await asyncio.sleep(0.1)

async def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print('{} seconds pass'.format(count))
        count += 1
        await asyncio.sleep(1)

async def main():
    task1 = asyncio.create_task(print_time())         #функции оборачиваются в экземплры класса Tasks, метод create_task отвечает за передачу событий в очередь событийного цикла.
    task2 = asyncio.create_task(print_nums())

    await asyncio.gather(task1, task2)         #gather - генератор 

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())         #
    # loop.close()
    asyncio.run(main())