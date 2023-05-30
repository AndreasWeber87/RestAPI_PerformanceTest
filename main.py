# Sources:
# https://docs.python.org/3/library/asyncio-task.html
# https://docs.aiohttp.org/en/stable/client_reference.html
# https://docs.python.org/3/library/time.html#time.perf_counter_ns
# https://docs.python.org/3/library/statistics.html
# https://magicstack.github.io/asyncpg/current/index.html

import asyncio
import sys
from datetime import datetime
import traceback
import data
import tests


def printWithTime(text: str):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}: {text}")


def __askUserWhichApiToTest():
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


def __askUserHowManyRecords():
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


def __askUserHowManyTasks():
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
        urlToTest = __askUserWhichApiToTest()
        recordsCnt = __askUserHowManyRecords()
        tasksCnt = __askUserHowManyTasks()
        #urlToTest = "http://localhost:7000/"
        #recordsCnt = 100
        #tasksCnt = 5

        streets = data.getStreetsFromCSV("STRASSE.csv", recordsCnt)

        while 1:
            print("\nWhich test do you want to start?")
            print("1 = AddTest")
            print("2 = ChangeTest")
            print("3 = GetTest")
            print("4 = DeleteTest")
            print("5 = All tests")
            print("6 = Exit")
            inp = input()

            if inp == "1" or inp == "5":
                asyncio.run(tests.runTest(tests.Testcategory.AddTest, urlToTest, streets, tasksCnt))
            if inp == "2" or inp == "5":
                asyncio.run(tests.runTest(tests.Testcategory.ChangeTest, urlToTest, streets, tasksCnt))
            if inp == "3" or inp == "5":
                asyncio.run(tests.runTest(tests.Testcategory.GetTest, urlToTest, streets, tasksCnt))
            if inp == "4" or inp == "5":
                asyncio.run(tests.runTest(tests.Testcategory.DeleteTest, urlToTest, streets, tasksCnt))
            if inp == "6":
                sys.exit()
    except Exception:
        traceback.print_exc()
