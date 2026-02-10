import time
import threading

from fastapi import FastAPI


app = FastAPI(docs_url=None)

@app.get("/sync/{id}")
def sync(id: int):
    print(f"sync. Потоков: {threading.active_count()}")
    print(f"sync. Начал {id}: {time.time(): 2f}")
    time.sleep(3)
    print(f"sync. Закончил {id}: {time.time(): 2f}")


@app.get("/async/{id}")
async def async_function(id: int):
    print(f"async. Потоков: {threading.active_count()}")
    print(f"async. Начал {id}: {time.time(): 2f}")
    await asyncio.sleep(3)
    print(f"async. Закончил {id}: {time.time(): 2f}")

import asyncio
import aiohttp

async def get_data(i: int, endpoint: str):
    print(f"Начал выполнение: {i}")
    url = f"http://127.0.0.1:8000/{endpoint}/{i}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(f"Закончил выполнение: {i}")


if __name__ == "__main__":
    async def test():
        start = time.time()
        await asyncio.gather(*[get_data(i, "sync") for i in range(3)])
        print(f"Время: {time.time() - start:.2f} сек")
        start = time.time()
        await asyncio.gather(*[get_data(i, "async") for i in range(3)])
        print(f"Время: {time.time() - start:.2f} сек")


    asyncio.run(test())
