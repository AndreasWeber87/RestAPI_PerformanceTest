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


async def __task(taskNumber: str, queue: asyncio.queues.Queue, testCat: Testcategory, url: str):
    timer = Timer(text=f"Task {taskNumber} elapsed time: {{:.1f}}s")
    timer.start()
    async with aiohttp.ClientSession() as session:
        while not queue.empty():
            street = await queue.get()

            if testCat == Testcategory.AddTest:
                async with session.post(url, json={"skz": street.skz, "streetname": street.streetname}) as response:
                    if response.status != 201:
                        print(f"error on data: skz={street.skz}, streetname={street.streetname}")
            elif testCat == Testcategory.ChangeTest:
                async with session.put(url + str(street.skz), json={"streetname": street.streetname + "2"}) as response:
                    if response.status != 200:
                        print(f"error on data: skz={street.skz}, streetname={street.streetname}")
            elif testCat == Testcategory.GetTest:
                async with session.get(url + str(street.skz)) as response:
                    if response.status != 200:
                        print(f"error on data: skz={street.skz}, streetname={street.streetname}")
                    else:
                        respJson = await response.json()
                        if respJson != {"skz": street.skz, "streetname": street.streetname + "2"}:
                            print(f"error in json comparison on data: skz={street.skz}, streetname={street.streetname}")
            elif testCat == Testcategory.DeleteTest:
                async with session.delete(url + str(street.skz)) as response:
                    if response.status != 200:
                        print(f"error on data: skz={street.skz}, streetname={street.streetname}")
    timer.stop()


async def runTest(testCat: Testcategory, urlToTest: str, streets: list, tasksCnt: int):
    queues = []

    if testCat == Testcategory.AddTest:  # On the AddTest create first a new table in the database.
        async with aiohttp.ClientSession() as session:
            async with session.post(urlToTest + "createTable") as response:
                if response.status != 201:
                    print(f"error on creating table")

    if testCat == Testcategory.AddTest:
        urlToTest += "addStreet"
    elif testCat == Testcategory.ChangeTest:
        urlToTest += "changeStreet/"
    elif testCat == Testcategory.GetTest:
        urlToTest += "getStreet?skz="
    elif testCat == Testcategory.DeleteTest:
        urlToTest += "deleteStreet/"

    for i in range(tasksCnt):  # Create new queues for the tasks.
        queues.append(asyncio.Queue())

    iData = 0
    while iData < len(streets):  # Fills the queues evenly with tasks. Each task contain a record.
        iTask = 0
        while iData < len(streets) and iTask < tasksCnt:
            await queues[iTask].put(streets[iData])
            iData += 1
            iTask += 1

    printWithTime(f"{testCat.name} on {urlToTest} starts...")

    with Timer(text="\nTotal elapsed time: {:.1f}s"):
        async with asyncio.TaskGroup() as tg:
            for i in range(tasksCnt):
                tg.create_task(__task(str(i + 1), queues[i], testCat, urlToTest))

    printWithTime(f"{testCat.name} finished...")
