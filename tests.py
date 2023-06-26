import time
import aiohttp
import asyncio
import statistics
import asyncpg
from enum import Enum
from main import printWithTime


timeMeasurementsCurrTest = []  # measurements of the current test
allTimeMeasurements = []


class Testcategory(Enum):
    AddTest = 1
    ChangeTest = 2
    GetTest = 3
    DeleteTest = 4


class MeasurementsOfTest:
    timeMeasurements = []
    elapsedTime = 0.0
    testcategory = Testcategory.AddTest


async def __task(queue: asyncio.queues.Queue, testCat: Testcategory, url: str):
    async with aiohttp.ClientSession() as session:
        while not queue.empty():
            street = await queue.get()
            timeBeforeRequest = time.perf_counter_ns()

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

            timeAfterRequest = time.perf_counter_ns()
            timeMeasurementsCurrTest.append((timeAfterRequest - timeBeforeRequest) / 1_000_000)  # add measurement in ms


async def __connectDB():
    user = "postgres"
    password = "xsmmsgbAMfIOIWPPBrsc"
    host = "192.168.0.2"
    port = "5432"
    database = "ogd"

    return await asyncpg.connect(f'postgresql://{user}:{password}@{host}:{port}/{database}')


async def __resetDatabaseStatistics():
    conn = await __connectDB()
    await conn.execute('SELECT pg_stat_statements_reset();')
    await conn.close()


async def __getDatabaseStatistics():
    conn = await __connectDB()
    row = await conn.fetchrow("""select query, mean_exec_time
from pg_stat_statements
where query like '%public.strasse%'
order by calls desc
LIMIT 1;""")

    await conn.close()
    meanExecTime = float(row[1])
    print(f"Database mean_exec_time of '{str(row[0])}': {str(round(meanExecTime, 2))}ms")
    return meanExecTime


def outputTimeStats(timeMeasurements: list, timeElapsed: float):
    print(f"Total time: {str(round(timeElapsed, 2))}s")
    print(f"Count of requests: {str(len(timeMeasurements))}")
    print(f"Shortest response time: {round(min(timeMeasurements), 2)}ms")
    print(f"Longest response time: {round(max(timeMeasurements), 2)}ms")
    print(f"Arithmetic mean of response time: {round(statistics.mean(timeMeasurements), 2)}ms")

    deciles = statistics.quantiles(timeMeasurements, n=10, method='exclusive')
    print(f"20% percentiles: {round(deciles[1], 2)}ms")
    print(f"80% percentiles: {round(deciles[7], 2)}ms\n")


def outputGroupedTimeStats():
    timeMeasurementsOfAllTests = []
    timeElapsedOfAllTests = 0.0

    timeMeasurementsOfAllAddTests = []
    timeElapsedOfAllAddTests = 0.0

    timeMeasurementsOfAllChangeTests = []
    timeElapsedOfAllChangeTests = 0.0

    timeMeasurementsOfAllGetTests = []
    timeElapsedOfAllGetTests = 0.0

    timeMeasurementsOfAllDeleteTests = []
    timeElapsedOfAllDeleteTests = 0.0

    for measurement in allTimeMeasurements:
        timeMeasurementsOfAllTests += measurement.timeMeasurements
        timeElapsedOfAllTests += measurement.elapsedTime

        if measurement.testcategory == Testcategory.AddTest:
            timeMeasurementsOfAllAddTests += measurement.timeMeasurements
            timeElapsedOfAllAddTests += measurement.elapsedTime
        elif measurement.testcategory == Testcategory.ChangeTest:
            timeMeasurementsOfAllChangeTests += measurement.timeMeasurements
            timeElapsedOfAllChangeTests += measurement.elapsedTime
        elif measurement.testcategory == Testcategory.GetTest:
            timeMeasurementsOfAllGetTests += measurement.timeMeasurements
            timeElapsedOfAllGetTests += measurement.elapsedTime
        elif measurement.testcategory == Testcategory.DeleteTest:
            timeMeasurementsOfAllDeleteTests += measurement.timeMeasurements
            timeElapsedOfAllDeleteTests += measurement.elapsedTime

    if len(timeMeasurementsOfAllAddTests) != 0:
        print("Measurements of all AddTests since program start:")
        outputTimeStats(timeMeasurementsOfAllAddTests, timeElapsedOfAllAddTests)
    if len(timeMeasurementsOfAllChangeTests) != 0:
        print("Measurements of all ChangeTests since program start:")
        outputTimeStats(timeMeasurementsOfAllChangeTests, timeElapsedOfAllChangeTests)
    if len(timeMeasurementsOfAllGetTests) != 0:
        print("Measurements of all GetTests since program start:")
        outputTimeStats(timeMeasurementsOfAllGetTests, timeElapsedOfAllGetTests)
    if len(timeMeasurementsOfAllDeleteTests) != 0:
        print("Measurements of all DeleteTests since program start:")
        outputTimeStats(timeMeasurementsOfAllDeleteTests, timeElapsedOfAllDeleteTests)

    print("Measurements of all tests since program start:")
    outputTimeStats(timeMeasurementsOfAllTests, timeElapsedOfAllTests)


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

    await __resetDatabaseStatistics()
    printWithTime(f"{testCat.name} on {urlToTest} starts...")
    timeBeforeTest = time.perf_counter_ns()

    async with asyncio.TaskGroup() as tg:
        for i in range(tasksCnt):
            tg.create_task(__task(queues[i], testCat, urlToTest))

    printWithTime(f"{testCat.name} finished...")

    timeAfterTest = time.perf_counter_ns()
    timeElapsedOnTest = (timeAfterTest - timeBeforeTest) / 1_000_000_000
    print(f"Count of tasks: {str(tasksCnt)}")

    meanTimeDbQuery = await __getDatabaseStatistics()
    global timeMeasurementsCurrTest

    for measurement in timeMeasurementsCurrTest:
        measurement -= meanTimeDbQuery

    outputTimeStats(timeMeasurementsCurrTest, timeElapsedOnTest)

    test = MeasurementsOfTest()
    test.timeMeasurements = timeMeasurementsCurrTest
    test.elapsedTime = timeElapsedOnTest
    test.testcategory = testCat
    allTimeMeasurements.append(test)

    timeMeasurementsCurrTest = []
