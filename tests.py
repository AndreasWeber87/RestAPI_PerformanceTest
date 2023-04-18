from codetiming import Timer
import aiohttp
import asyncio
from enum import Enum
from main import printWithTime


class Testcategory(Enum):
    AddTest = 1
    ChangeTest = 2
    GetTest = 3
    DeleteTest = 4


async def __insertTask(taskNumber: str, queue: asyncio.queues.Queue, testCat: Testcategory, url: str):
    timer = Timer(text=f"Task {taskNumber} elapsed time: {{:.1f}}s")
    timer.start()
    async with aiohttp.ClientSession() as session:
        while not queue.empty():
            street = await queue.get()

            if testCat == Testcategory.AddTest:
                async with session.post(url, json={"skz": street.skz, "streetname": street.streetname}) as response:
                    if response.status != 201:
                        print(f"error on data: {street}")

            #resp = await response.text()
            #print(resp)
    timer.stop()


async def runTest(testCat: Testcategory, portToTest: int, streets: list, tasksCnt: int):
    url = f'http://localhost:{portToTest}/'
    queues = []

    if testCat == Testcategory.AddTest:  # On the AddTest create first a new table in the database.
        async with aiohttp.ClientSession() as session:
            async with session.post(url + "createTable") as response:
                if response.status != 201:
                    print(f"error on creating table")

    if testCat == Testcategory.AddTest:
        url += "addStreet"

    for i in range(tasksCnt):  # Create new queues for the tasks.
        queues.append(asyncio.Queue())

    iData = 0
    while iData < len(streets):  # Fills the queues evenly with tasks. Each task contain a record.
        iTask = 0
        while iData < len(streets) and iTask < tasksCnt:
            await queues[iTask].put(streets[iData])
            iData += 1
            iTask += 1

    printWithTime(f"{testCat.name} starts...")

    with Timer(text="\nTotal elapsed time: {:.1f}s"):
        async with asyncio.TaskGroup() as tg:
            for i in range(tasksCnt):
                tg.create_task(__insertTask(str(i + 1), queues[i], testCat, url))

    printWithTime(f"{testCat.name} finished...")
