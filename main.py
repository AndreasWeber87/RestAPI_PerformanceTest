import asyncio
import aiohttp
from codetiming import Timer

import sys
import data


async def task(name, work_queue):
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    timer.start()
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"error on url {url}: " + str(response.status))
                #resp = await response.text()
    timer.stop()


async def main(appName: str):
    url = ""

    if appName.lower() == "go":
        url = "http://localhost:7000/getGemeinde?id="
    elif appName.lower() == "nodejs":
        url = "http://localhost:8000/getGemeinde?id="
    elif appName.lower() == "python":
        url = "http://localhost:9000/getGemeinde?id="
    else:
        raise Exception("unknown parameter")

    print("Performance Test for: " + appName.lower())
    queues = []
    gemeindeIDs = data.getGemeindeIdList()

    for i in range(5):
        queues.append(asyncio.Queue())
        for j in range(2000):
            await queues[i].put(url + gemeindeIDs[j])

    with Timer(text="\nTotal elapsed time: {:.1f}"):
        await asyncio.gather(
            asyncio.create_task(task("1", queues[0])),
            asyncio.create_task(task("2", queues[1])),
            asyncio.create_task(task("3", queues[2])),
            asyncio.create_task(task("4", queues[3])),
            asyncio.create_task(task("5", queues[4])),
        )

if __name__ == "__main__":
    try:
        #asyncio.run(main(sys.argv[0]))
        asyncio.run(main("go"))
        #asyncio.run(main("nodejs"))
        #asyncio.run(main("python"))
    except Exception as e:
        print(str(e))
