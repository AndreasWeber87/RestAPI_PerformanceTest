from codetiming import Timer
import aiohttp
import asyncio
from main import printWithTime


async def __insertTask(taskName: str, queue: asyncio.queues.Queue, url: str):
    timer = Timer(text=f"Task {taskName} elapsed time: {{:.1f}}s")
    timer.start()
    async with aiohttp.ClientSession() as session:
        while not queue.empty():
            street = await queue.get()
            async with session.post(url, json={"skz": street.skz, "streetname": street.streetname}) as response:
                if response.status != 201:
                    print(f"error on data: {street}")
                #resp = await response.text()
                #print(resp)
    timer.stop()


async def runInsertTest(portToTest: int, streets: list, tasksCnt: int):
    baseUrl = f'http://localhost:{portToTest}/'
    queues = []

    for i in range(tasksCnt):  # Create new queues for the tasks.
        queues.append(asyncio.Queue())

    iData = 0
    while iData < len(streets):  # Fills the queues evenly with the tasks.
        iTask = 0
        while iData < len(streets) and iTask < tasksCnt:
            await queues[iTask].put(streets[iData])
            iData += 1
            iTask += 1

    printWithTime("Insert-Test starts...")

    with Timer(text="\nTotal elapsed time: {:.1f}s"):
        async with asyncio.TaskGroup() as tg:
            for i in range(tasksCnt):
                tg.create_task(__insertTask(str(i + 1), queues[i], baseUrl + "addStreet"))

    printWithTime("Insert-Test finished...")
