import asyncio
import aiohttp
from time import time

def write_image(data):
    filename = 'file-{}.jpeg'.format(int(time() *1000))
    with open(filename, 'wb') as file:
        file.write(data)

async def fetch_content(url, session):          #корутина получения контента
    async with session.get(url, allow_redirects=True) as response:       #async with - это асинхронный контекстный менеджер
        data = await response.read()            #метод read возращает бинарные данные
        write_image(data)

async def main():           
    url = 'https://loremflickr.com/320/240'
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))         #для добавления коррутин в цикл событий оборачиваем функции в эземпляры класса Task
            tasks.append(task)          #добавляем их в список задач
        await asyncio.gather(*tasks)            #запускает несколько асинхронных задач (корутин) параллельно и ожидает их завершения. Она возвращает результаты всех задач в порядке их передачи.

if __name__ == '__main__':
    t0 = time()
    asyncio.run(main())
    print(time() - t0)