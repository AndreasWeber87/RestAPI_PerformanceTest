# Sources:
# https://docs.python.org/3/library/asyncio-task.html
# https://docs.aiohttp.org/en/stable/client_reference.html
# https://docs.python.org/3/library/time.html#time.perf_counter_ns
# https://docs.python.org/3/library/statistics.html
# https://magicstack.github.io/asyncpg/current/index.html
# https://docs.python.org/3/library/subprocess.html

import asyncio
from datetime import datetime
import traceback
import data
import tests


def printWithTime(text: str):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}: {text}")


def askUserWhichApiToTest():
    while 1:
        print("On which API do you want to test the performance?")
        print("1 = GoAPI")
        print("2 = NodeJsAPI")
        print("3 = PythonAPI")
        inp = input()

        if inp == "1":
            return "http://192.168.0.3:7000/"
        elif inp == "2":
            return "http://192.168.0.4:8000/"
        elif inp == "3":
            return "http://192.168.0.5:9000/"


def askUserHowManyRecords():
    while 1:
        print("How many records do you want to use for the test?")
        inp = input()

        try:
            val = int(inp)
            if val < 1:
                continue
            return val
        except:
            pass


def askUserHowManyTasks():
    while 1:
        print("How many tasks do you want to use for the test?")
        inp = input()

        try:
            val = int(inp)
            if val < 1:
                continue
            return val
        except:
            pass


if __name__ == "__main__":
    try:
        #urlToTest = askUserWhichApiToTest()
        #recordsCnt = askUserHowManyRecords()
        #tasksCnt = askUserHowManyTasks()
        urlToTest = "http://localhost:7000/"
        recordsCnt = 10000
        tasksCnt = 5

        streets = data.getStreetsFromCSV("STRASSE.csv", recordsCnt)

        while 1:
            print("\nWhich test do you want to start?")
            print("1 = AddTest")
            print("2 = ChangeTest")
            print("3 = GetTest")
            print("4 = DeleteTest")
            inp = input()

            if inp == "1":
                asyncio.run(tests.runTest(tests.Testcategory.AddTest, urlToTest, streets, tasksCnt))
            elif inp == "2":
                asyncio.run(tests.runTest(tests.Testcategory.ChangeTest, urlToTest, streets, tasksCnt))
            elif inp == "3":
                asyncio.run(tests.runTest(tests.Testcategory.GetTest, urlToTest, streets, tasksCnt))
            elif inp == "4":
                asyncio.run(tests.runTest(tests.Testcategory.DeleteTest, urlToTest, streets, tasksCnt))
    except Exception:
        traceback.print_exc()
